"""
Connectivity test — requires live internet access.
Skip in offline CI with: pytest -m "not connectivity"
"""
import pytest
import httpx


@pytest.mark.connectivity
@pytest.mark.asyncio
async def test_exchange_rate_api_reachable():
    """Verify the ExchangeRate API is reachable and returns HTTP 200."""
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.get("https://open.er-api.com/v6/latest/USD")
    assert response.status_code == 200
    data = response.json()
    assert "rates" in data
    assert "USD" in data["rates"]
