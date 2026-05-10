from typing import Any
from fastapi import APIRouter, HTTPException, Query
from services.currency_service import get_rates, convert_amount

router = APIRouter(prefix="/currency", tags=["currency"])


@router.get("/rates")
async def get_exchange_rates(base: str = Query(default="USD")) -> Any:
    """Return current exchange rates from ExchangeRate API."""
    try:
        data = await get_rates(base.upper())
        return {
            "success": True,
            "data": {
                "base": data.get("base_code", data.get("base", base.upper())),
                "rates": data.get("rates", {}),
                "time_last_update_unix": data.get("time_last_update_unix", 0),
            },
        }
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail="Currency service temporarily unavailable")


@router.get("/convert")
async def convert_currency(
    amount: float = Query(..., description="Amount to convert"),
    from_: str = Query(..., alias="from", description="Source currency code"),
    to: str = Query(..., description="Target currency code"),
) -> Any:
    """Convert an amount from one currency to another."""
    if amount <= 0:
        raise HTTPException(status_code=422, detail="Amount must be greater than 0")

    try:
        rates_data = await get_rates(from_.upper())
    except ConnectionError:
        raise HTTPException(status_code=503, detail="Currency service temporarily unavailable")

    try:
        converted = convert_amount(amount, from_, to, rates_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Unsupported currency code")

    return {
        "success": True,
        "data": {
            "amount": amount,
            "from": from_.upper(),
            "to": to.upper(),
            "converted_amount": converted,
        },
    }
