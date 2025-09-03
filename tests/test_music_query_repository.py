import unittest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock

from data_accessor.domain.exceptions.forbidden_sql_statement_exception import ForbiddenSqlStatementException
from data_accessor.infrastructure.repositories._music_query_repository import MusicQueryRepository

class TestMusicQueryRepository(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.mock_engine = MagicMock()
        self.mock_conn = AsyncMock()
        self.mock_result = MagicMock()
        self.mock_result.returns_rows = True
        self.mock_result.fetchall.return_value = [("table1", "col1", "text")]

        self.mock_conn.execute.return_value = self.mock_result
        self.mock_engine.connect = AsyncMock(return_value=self.mock_conn)

        with patch("data_accessor.infrastructure.repositories._music_query_repository.create_async_engine") as mock_create_engine:
            mock_create_engine.return_value = self.mock_engine
            self.repo = MusicQueryRepository(schema_name="public", engine=self.mock_engine)

    async def test_execute_sql_select(self):
        print("[TEST] Starting invalid statement test")
        result = await self.repo.execute_sql("SELECT * FROM test_table")
        self.assertEqual(result, [("table1", "col1", "text")])

    async def test_execute_sql_invalid_statement(self):
        with self.assertRaises(ForbiddenSqlStatementException):
            await self.repo.execute_sql("DROP TABLE users")

    async def test_fetch_database_schema(self):
        expected = "table1:\n  col1: text"
        result = await self.repo.fetch_database_schema()
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
