"""
Unit tests for the currency service and router.
External API calls are mocked.
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock

MOCK_RATES = {
    "base_code": "USD",
    "rates": {
        "USD": 1.0,
        "EUR": 0.92,
        "TND": 3.12,
        "GBP": 0.79,
        "JPY": 154.5,
    },
    "time_last_update_unix": 1700000000,
}


@pytest.mark.asyncio
async def test_get_rates_success(client):
    with patch("routers.currency.get_rates", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = MOCK_RATES
        response = await client.get("/api/currency/rates")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert "rates" in body["data"]
    assert "USD" in body["data"]["rates"]


@pytest.mark.asyncio
async def test_get_rates_service_unavailable(client):
    with patch("routers.currency.get_rates", new_callable=AsyncMock) as mock_get:
        mock_get.side_effect = ConnectionError("Currency service temporarily unavailable")
        response = await client.get("/api/currency/rates")
    assert response.status_code == 503


@pytest.mark.asyncio
async def test_convert_success(client):
    with patch("routers.currency.get_rates", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = MOCK_RATES
        response = await client.get("/api/currency/convert?amount=100&from=USD&to=EUR")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["converted_amount"] == round(100 * 0.92, 2)


@pytest.mark.asyncio
async def test_convert_unsupported_currency(client):
    with patch("routers.currency.get_rates", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = MOCK_RATES
        response = await client.get("/api/currency/convert?amount=100&from=USD&to=XYZ")
    assert response.status_code == 400
    assert "Unsupported currency code" in response.json()["detail"]


@pytest.mark.asyncio
async def test_convert_zero_amount(client):
    response = await client.get("/api/currency/convert?amount=0&from=USD&to=EUR")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_convert_service_unavailable(client):
    with patch("routers.currency.get_rates", new_callable=AsyncMock) as mock_get:
        mock_get.side_effect = ConnectionError("unavailable")
        response = await client.get("/api/currency/convert?amount=10&from=USD&to=EUR")
    assert response.status_code == 503


def test_convert_amount_math():
    """Unit test for the conversion math function."""
    from services.currency_service import convert_amount
    rates = {
        "base_code": "USD",
        "rates": {"USD": 1.0, "EUR": 0.92, "TND": 3.12},
    }
    result = convert_amount(100.0, "USD", "EUR", rates)
    assert result == round(100.0 * 0.92, 2)


def test_convert_amount_cross_currency():
    """Test cross-currency conversion (neither is base)."""
    from services.currency_service import convert_amount
    rates = {
        "base_code": "USD",
        "rates": {"USD": 1.0, "EUR": 0.92, "TND": 3.12},
    }
    # EUR -> TND: 100 EUR / 0.92 * 3.12
    result = convert_amount(100.0, "EUR", "TND", rates)
    expected = round((100.0 / 0.92) * 3.12, 2)
    assert result == expected


def test_convert_amount_unsupported_raises():
    from services.currency_service import convert_amount
    rates = {"base_code": "USD", "rates": {"USD": 1.0}}
    with pytest.raises(ValueError):
        convert_amount(10.0, "USD", "XYZ", rates)
