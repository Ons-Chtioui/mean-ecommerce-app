"""
Unit and integration tests for Product CRUD endpoints.
"""
import pytest


async def _create_category(client, name="TestCategory"):
    resp = await client.post("/api/categories", json={"name": name})
    return resp.json()["data"]["id"]


@pytest.mark.asyncio
async def test_create_product_success(client):
    cat_id = await _create_category(client)
    response = await client.post(
        "/api/products",
        json={
            "name": "Test Product",
            "description": "A test product",
            "price": 29.99,
            "category": cat_id,
            "stock": 10,
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    assert body["data"]["name"] == "Test Product"
    assert body["data"]["price"] == 29.99
    assert isinstance(body["data"]["category"], dict)
    assert body["data"]["category"]["id"] == cat_id


@pytest.mark.asyncio
async def test_create_product_missing_fields(client):
    response = await client.post("/api/products", json={"name": "Incomplete"})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_product_invalid_category(client):
    response = await client.post(
        "/api/products",
        json={
            "name": "Bad Product",
            "description": "desc",
            "price": 10.0,
            "category": "000000000000000000000000",
        },
    )
    assert response.status_code == 404
    assert "Category not found" in response.json()["detail"]


@pytest.mark.asyncio
async def test_create_product_negative_price(client):
    cat_id = await _create_category(client, "PriceCat")
    response = await client.post(
        "/api/products",
        json={"name": "Cheap", "description": "desc", "price": -1.0, "category": cat_id},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_product_negative_stock(client):
    cat_id = await _create_category(client, "StockCat")
    response = await client.post(
        "/api/products",
        json={
            "name": "NoStock",
            "description": "desc",
            "price": 5.0,
            "category": cat_id,
            "stock": -1,
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_all_products(client):
    cat_id = await _create_category(client, "AllCat")
    await client.post(
        "/api/products",
        json={"name": "P1", "description": "d", "price": 1.0, "category": cat_id},
    )
    await client.post(
        "/api/products",
        json={"name": "P2", "description": "d", "price": 2.0, "category": cat_id},
    )
    response = await client.get("/api/products")
    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 2
    assert len(body["data"]) == 2
    # Each product must have a populated category object
    for p in body["data"]:
        assert isinstance(p["category"], dict)
        assert "id" in p["category"]
        assert "name" in p["category"]


@pytest.mark.asyncio
async def test_get_product_by_id(client):
    cat_id = await _create_category(client, "GetCat")
    create_resp = await client.post(
        "/api/products",
        json={"name": "FindMe", "description": "d", "price": 5.0, "category": cat_id},
    )
    prod_id = create_resp.json()["data"]["id"]

    response = await client.get(f"/api/products/{prod_id}")
    assert response.status_code == 200
    assert response.json()["data"]["name"] == "FindMe"


@pytest.mark.asyncio
async def test_get_product_not_found(client):
    response = await client.get("/api/products/000000000000000000000000")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_products_by_category(client):
    cat1_id = await _create_category(client, "Cat1")
    cat2_id = await _create_category(client, "Cat2")
    await client.post(
        "/api/products",
        json={"name": "InCat1", "description": "d", "price": 1.0, "category": cat1_id},
    )
    await client.post(
        "/api/products",
        json={"name": "InCat2", "description": "d", "price": 2.0, "category": cat2_id},
    )

    response = await client.get(f"/api/products/category/{cat1_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 1
    assert body["data"][0]["name"] == "InCat1"


@pytest.mark.asyncio
async def test_update_product(client):
    cat_id = await _create_category(client, "UpdateCat")
    create_resp = await client.post(
        "/api/products",
        json={"name": "OldName", "description": "d", "price": 10.0, "category": cat_id},
    )
    prod_id = create_resp.json()["data"]["id"]

    response = await client.put(f"/api/products/{prod_id}", json={"name": "NewName", "price": 20.0})
    assert response.status_code == 200
    body = response.json()
    assert body["data"]["name"] == "NewName"
    assert body["data"]["price"] == 20.0


@pytest.mark.asyncio
async def test_delete_product(client):
    cat_id = await _create_category(client, "DelCat")
    create_resp = await client.post(
        "/api/products",
        json={"name": "ToDelete", "description": "d", "price": 5.0, "category": cat_id},
    )
    prod_id = create_resp.json()["data"]["id"]

    del_resp = await client.delete(f"/api/products/{prod_id}")
    assert del_resp.status_code == 200

    get_resp = await client.get(f"/api/products/{prod_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_product_not_found(client):
    response = await client.delete("/api/products/000000000000000000000000")
    assert response.status_code == 404
