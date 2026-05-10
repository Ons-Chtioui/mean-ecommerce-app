import logging
from cachetools import TTLCache
import httpx
from config import settings

logger = logging.getLogger(__name__)

# Cache exchange rates for 60 minutes (3600 seconds)
_cache: TTLCache = TTLCache(maxsize=10, ttl=3600)

SUPPORTED_CURRENCIES = {"USD", "EUR", "TND", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "MAD"}


async def get_rates(base: str = "USD") -> dict:
    """Fetch exchange rates from ExchangeRate API with TTL caching."""
    base = base.upper()
    if base in _cache:
        logger.debug(f"Cache hit for base currency: {base}")
        return _cache[base]

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{settings.EXCHANGE_RATE_API_URL}/{base}")
            response.raise_for_status()
        data = response.json()
        _cache[base] = data
        logger.info(f"Fetched and cached exchange rates for base: {base}")
        return data
    except httpx.ConnectError as e:
        logger.error(f"Cannot connect to ExchangeRate API: {e}")
        raise ConnectionError("Currency service temporarily unavailable")
    except httpx.TimeoutException as e:
        logger.error(f"ExchangeRate API timeout: {e}")
        raise ConnectionError("Currency service temporarily unavailable")
    except httpx.HTTPStatusError as e:
        logger.error(f"ExchangeRate API HTTP error: {e}")
        raise ConnectionError("Currency service temporarily unavailable")


def convert_amount(amount: float, from_currency: str, to_currency: str, rates: dict) -> float:
    """Convert amount from one currency to another using provided rates."""
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    rate_map = rates.get("rates", {})

    if from_currency not in rate_map:
        raise ValueError(f"Unsupported currency code: {from_currency}")
    if to_currency not in rate_map:
        raise ValueError(f"Unsupported currency code: {to_currency}")

    # rates are relative to the base currency in the response
    base = rates.get("base_code", rates.get("base", "USD")).upper()

    if from_currency == base:
        converted = amount * rate_map[to_currency]
    elif to_currency == base:
        converted = amount / rate_map[from_currency]
    else:
        # Convert via base: amount -> base -> to_currency
        in_base = amount / rate_map[from_currency]
        converted = in_base * rate_map[to_currency]

    return round(converted, 2)


def clear_cache():
    """Clear the exchange rate cache (used in tests)."""
    _cache.clear()
