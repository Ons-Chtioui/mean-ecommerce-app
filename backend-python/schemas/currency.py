from typing import Dict
from pydantic import BaseModel, Field


class CurrencyRatesResponse(BaseModel):
    rates: Dict[str, float]
    base: str
    time_last_update_unix: int = Field(default=0)


class ConvertResponse(BaseModel):
    amount: float
    from_currency: str
    to_currency: str
    converted_amount: float  # rounded to 2 decimal places
