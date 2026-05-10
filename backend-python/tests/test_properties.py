"""
Property-based tests using Hypothesis.
Feature: devnet-ecommerce-platform
"""
import json
import pytest
from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st
from unittest.mock import AsyncMock, patch

from schemas.product import ProductCreate
from schemas.category import CategoryCreate
from services.currency_service import convert_amount


# ── Strategies ────────────────────────────────────────────────────────────────

valid_name_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters=" -"),
    min_size=2,
    max_size=50,
).filter(lambda s: len(s.strip()) >= 2)

valid_product_name_strategy = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters=" -"),
    min_size=2,
    max_size=100,
).filter(lambda s: len(s.strip()) >= 2)

valid_description_strategy = st.text(min_size=1, max_size=200)

valid_price_strategy = st.floats(min_value=0.0, max_value=1e6, allow_nan=False, allow_infinity=False)

valid_stock_strategy = st.integers(min_value=0, max_value=10000)

valid_rating_strategy = st.floats(min_value=0.0, max_value=5.0, allow_nan=False, allow_infinity=False)

FAKE_CATEGORY_ID = "507f1f77bcf86cd799439011"


# ── Property 1: Product JSON Round-Trip ──────────────────────────────────────
# Feature: devnet-ecommerce-platform, Property 1: Product JSON Round-Trip

@given(
    name=valid_product_name_strategy,
    description=valid_description_strategy,
    price=valid_price_strategy,
    stock=valid_stock_strategy,
    rating=valid_rating_strategy,
)
@settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow])
def test_product_json_roundtrip(name, description, price, stock, rating):
    """Property 1: Serializing a ProductCreate to JSON and back produces an equal object."""
    product = ProductCreate(
        name=name,
        description=description,
        price=price,
        category=FAKE_CATEGORY_ID,
        stock=stock,
        rating=rating,
    )
    json_str = product.model_dump_json()
    restored = ProductCreate.model_validate_json(json_str)
    assert restored.name == product.name
    assert restored.description == product.description
    assert abs(restored.price - product.price) < 1e-9
    assert restored.stock == product.stock
    assert restored.category == product.category


# ── Property 4: Category Name Length Validation ───────────────────────────────
# Feature: devnet-ecommerce-platform, Property 4: Category Name Length Validation

@given(name=st.text(max_size=1))
@settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow])
def test_category_name_too_short_rejected(name):
    """Property 4a: Names shorter than 2 chars are rejected by Pydantic."""
    import pydantic
    with pytest.raises(pydantic.ValidationError):
        CategoryCreate(name=name)


@given(name=st.text(min_size=51))
@settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow])
def test_category_name_too_long_rejected(name):
    """Property 4b: Names longer than 50 chars are rejected by Pydantic."""
    import pydantic
    with pytest.raises(pydantic.ValidationError):
        CategoryCreate(name=name)


@given(name=valid_name_strategy)
@settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow])
def test_category_name_valid_accepted(name):
    """Property 4c: Names between 2 and 50 chars are accepted by Pydantic."""
    cat = CategoryCreate(name=name)
    assert 2 <= len(cat.name) <= 50


# ── Property 10: Product Price and Stock Non-Negativity ───────────────────────
# Feature: devnet-ecommerce-platform, Property 10: Product Price and Stock Non-Negativity

@given(price=st.floats(max_value=-0.01, allow_nan=False, allow_infinity=False))
@settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow])
def test_product_negative_price_rejected(price):
    """Property 10a: Negative price is rejected by Pydantic."""
    import pydantic
    with pytest.raises(pydantic.ValidationError):
        ProductCreate(
            name="Test",
            description="desc",
            price=price,
            category=FAKE_CATEGORY_ID,
        )


@given(stock=st.integers(max_value=-1))
@settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow])
def test_product_negative_stock_rejected(stock):
    """Property 10b: Negative stock is rejected by Pydantic."""
    import pydantic
    with pytest.raises(pydantic.ValidationError):
        ProductCreate(
            name="Test",
            description="desc",
            price=10.0,
            category=FAKE_CATEGORY_ID,
            stock=stock,
        )


# ── Property 11: Currency Conversion Mathematical Correctness ─────────────────
# Feature: devnet-ecommerce-platform, Property 11: Currency Conversion Mathematical Correctness

@given(amount=st.floats(min_value=0.01, max_value=1e6, allow_nan=False, allow_infinity=False))
@settings(max_examples=100, suppress_health_check=[HealthCheck.too_slow])
def test_currency_conversion_math(amount):
    """Property 11: converted_amount == round(amount * rate[to] / rate[from], 2)."""
    rates = {
        "base_code": "USD",
        "rates": {"USD": 1.0, "EUR": 0.92, "TND": 3.12, "GBP": 0.79},
    }
    result = convert_amount(amount, "USD", "EUR", rates)
    expected = round(amount * 0.92, 2)
    assert result == expected


@given(amount=st.floats(min_value=0.01, max_value=1e6, allow_nan=False, allow_infinity=False))
@settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow])
def test_currency_conversion_cross_math(amount):
    """Property 11b: Cross-currency conversion is mathematically correct."""
    rates = {
        "base_code": "USD",
        "rates": {"USD": 1.0, "EUR": 0.92, "TND": 3.12},
    }
    result = convert_amount(amount, "EUR", "TND", rates)
    expected = round((amount / 0.92) * 3.12, 2)
    assert result == expected
