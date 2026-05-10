"""
Unit and integration tests for Category CRUD endpoints.
"""
import pytest


@pytest.mark.asyncio
async def test_create_category_success(client):
    response = await client.post("/api/categories", json={"name": "Electronics", "description": "Electronic items"})
    assert response.status_code == 201
    body = response.json()
    assert body["success"] is True
    assert body["data"]["name"] == "Electronics"
    assert body["data"]["description"] == "Electronic items"
    assert "id" in body["data"]


@pytest.mark.asyncio
async def test_create_category_missing_name(client):
    response = await client.post("/api/categories", json={"description": "No name"})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_category_name_too_short(client):
    response = await client.post("/api/categories", json={"name": "A"})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_category_name_too_long(client):
    response = await client.post("/api/categories", json={"name": "A" * 51})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_all_categories_empty(client):
    response = await client.get("/api/categories")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["count"] == 0
    assert body["data"] == []


@pytest.mark.asyncio
async def test_get_all_categories(client):
    await client.post("/api/categories", json={"name": "Books"})
    await client.post("/api/categories", json={"name": "Clothing"})
    response = await client.get("/api/categories")
    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 2
    assert len(body["data"]) == 2


@pytest.mark.asyncio
async def test_get_category_by_id(client):
    create_resp = await client.post("/api/categories", json={"name": "Sports"})
    cat_id = create_resp.json()["data"]["id"]

    response = await client.get(f"/api/categories/{cat_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["data"]["name"] == "Sports"


@pytest.mark.asyncio
async def test_get_category_not_found(client):
    response = await client.get("/api/categories/000000000000000000000000")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_category_invalid_id(client):
    response = await client.get("/api/categories/invalid-id")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_category(client):
    create_resp = await client.post("/api/categories", json={"name": "Toys"})
    cat_id = create_resp.json()["data"]["id"]

    response = await client.put(f"/api/categories/{cat_id}", json={"name": "Toys & Games"})
    assert response.status_code == 200
    body = response.json()
    assert body["data"]["name"] == "Toys & Games"


@pytest.mark.asyncio
async def test_update_category_not_found(client):
    response = await client.put(
        "/api/categories/000000000000000000000000", json={"name": "Updated"}
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_category(client):
    create_resp = await client.post("/api/categories", json={"name": "ToDelete"})
    cat_id = create_resp.json()["data"]["id"]

    del_resp = await client.delete(f"/api/categories/{cat_id}")
    assert del_resp.status_code == 200
    assert del_resp.json()["success"] is True

    get_resp = await client.get(f"/api/categories/{cat_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_category_not_found(client):
    response = await client.delete("/api/categories/000000000000000000000000")
    assert response.status_code == 404
