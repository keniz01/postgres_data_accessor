import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from data_accessor.domain.exceptions.forbidden_sql_statement_exception import ForbiddenSqlStatementException
from data_accessor.infrastructure.repositories._music_query_repository import MusicQueryRepository

@pytest.fixture
def mock_engine():
    with patch("data_accessor.infrastructure.repositories._music_query_repository.create_async_engine") as mock_create_engine:
        mock_engine = MagicMock()
        mock_conn = AsyncMock()
        mock_result = MagicMock()
        mock_result.returns_rows = True
        mock_result.fetchall.return_value = [("table1", "col1", "text")]

        mock_conn.execute.return_value = mock_result
        mock_engine.connect = AsyncMock(return_value=mock_conn)

        mock_create_engine.return_value = mock_engine
        yield mock_engine

@pytest.fixture
def repo(mock_engine):
    return MusicQueryRepository(schema_name="public", engine=mock_engine)

async def test_execute_sql_select(repo):
    print("[TEST] Starting invalid statement test")
    result = await repo.execute_sql("SELECT * FROM test_table")
    assert result == [("table1", "col1", "text")]

async def test_execute_sql_invalid_statement(repo):
    with pytest.raises(ForbiddenSqlStatementException):
        await repo.execute_sql("DROP TABLE users")

async def test_fetch_database_schema(repo):
    expected = "table1:\n  col1: text"
    result = await repo.fetch_database_schema()
    assert result == expected
