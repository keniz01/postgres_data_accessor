import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from src.data_accessor.infrastructure.music_query_repository import MusicQueryRepository

@pytest.fixture
def mock_engine():
    with patch("src.data_accessor.infrastructure.music_query_repository.create_async_engine") as mock_create_engine:
        mock_engine = MagicMock()
        mock_conn = AsyncMock()
        mock_execute_result = AsyncMock()
        mock_execute_result.returns_rows = True
        mock_execute_result.fetchall = AsyncMock(return_value=[("table1", "col1", "text")])

        mock_conn.__aenter__.return_value = mock_conn
        mock_conn.execute.return_value = mock_execute_result
        mock_engine.connect.return_value = mock_conn

        mock_create_engine.return_value = mock_engine
        yield mock_engine

@pytest.fixture
def repo(mock_engine):
    return MusicQueryRepository(schema_name="public", connection_string="postgresql+asyncpg://user:pass@localhost/db")

@pytest.mark.asyncio
async def test_execute_sql_select(repo):
    result = await repo.execute_sql("SELECT * FROM test_table")
    assert result == [("table1", "col1", "text")]

@pytest.mark.asyncio
async def test_execute_sql_invalid_statement(repo):
    result = await repo.execute_sql("DROP TABLE users")
    assert result == "Only SELECT, INSERT, UPDATE, DELETE statements are allowed."

@pytest.mark.asyncio
async def test_fetch_database_schema(repo):
    expected = "table1:\n  col1: text"
    result = await repo.fetch_database_schema()
    assert result == expected
