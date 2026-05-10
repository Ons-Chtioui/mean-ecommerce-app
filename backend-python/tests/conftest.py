import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from mongomock_motor import AsyncMongoMockClient

# Override the database dependency before importing the app
import database as db_module


@pytest_asyncio.fixture
async def mock_db():
    """Provide an in-memory MongoDB database using mongomock-motor."""
    client = AsyncMongoMockClient()
    mock_database = client["test_ecommerce"]
    # Create indexes
    await mock_database["categories"].create_index("name", unique=True)
    await mock_database["products"].create_index("category")
    yield mock_database
    client.close()


@pytest_asyncio.fixture
async def client(mock_db):
    """Provide an async HTTP test client with the mock database injected."""
    from main import app
    from database import get_database

    app.dependency_overrides[get_database] = lambda: mock_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
