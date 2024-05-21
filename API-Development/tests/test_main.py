import pytest
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from main import app, DATABASE_URL, Base, AsyncSessionLocal
import httpx
from starlette.testclient import TestClient
from fastapi.testclient import TestClient

# Set up an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest.fixture(scope="session")
def anyio_backend():
    return 'asyncio'

@pytest.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture(scope="function")
async def async_session(test_engine):
    async_session = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session

@pytest.fixture(scope="module")
def test_app():
    return TestClient(app)

@pytest.fixture(scope="function", autouse=True)
async def override_get_session(test_app, async_session):
    app.dependency_overrides[AsyncSessionLocal] = lambda: async_session

@pytest.mark.anyio
async def test_create_log_entry(anyio_backend):
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        payload = {
            "message": "Test log entry",
            "level": "INFO"
        }
        response = await client.post("/log", json=payload)
        assert response.status_code == 200
        assert response.json() == {"message": "Log entry created"}
