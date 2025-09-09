import asyncio
import unittest
from unittest.mock import AsyncMock, patch

from data_accessor.domain.exceptions.forbidden_sql_statement_exception import ForbiddenSqlStatementException
from data_accessor.domain.exceptions.sql_statement_execution_exception import SqlStatementExecutionException
from data_accessor.infrastructure.repositories._music_query_repository import DefaultSqlSafetyChecker, MusicQueryRepository

class TestDefaultSqlSafetyChecker(unittest.TestCase):
    def setUp(self):
        self.checker = DefaultSqlSafetyChecker()

    def test_valid_simple_select(self):
        query = "SELECT * FROM songs"
        self.assertTrue(self.checker.is_safe_select_query(query))

    def test_multiple_statements(self):
        query = "SELECT * FROM songs; DROP TABLE songs;"
        self.assertFalse(self.checker.is_safe_select_query(query))

    def test_non_select(self):
        query = "DROP TABLE songs"
        self.assertFalse(self.checker.is_safe_select_query(query))

    def test_cte_query(self):
        query = "WITH cte AS (SELECT 1) SELECT * FROM cte"
        self.assertFalse(self.checker.is_safe_select_query(query))

    def test_comments(self):
        query = "SELECT * FROM songs -- comment"
        self.assertFalse(self.checker.is_safe_select_query(query))

class TestMusicQueryRepository(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.mock_engine = AsyncMock()
        self.mock_conn = AsyncMock()
        self.mock_engine.connect.return_value = self.mock_conn

        self.mock_result = AsyncMock()
        self.mock_result.returns_rows = True
        self.mock_result.fetchall = AsyncMock(return_value=[("row1",), ("row2",)])

        self.mock_conn.execute.return_value = self.mock_result
        self.mock_conn.close = AsyncMock()

        self.repo = MusicQueryRepository(
            engine=self.mock_engine
        )

    async def test_execute_sql_valid(self):
        sql = "SELECT * FROM songs"
        result = await self.repo.execute_sql(sql)

        # Verify return result
        self.assertEqual(result, [("row1",), ("row2",)])

        # Assert execute was called twice: once for search_path, once for query
        self.assertEqual(self.mock_conn.execute.call_count, 2)

        # Optional: Check both calls
        call_args_list = self.mock_conn.execute.call_args_list

        # First call: SET search_path
        set_path_sql = str(call_args_list[0][0][0])
        self.assertIn("SET search_path TO music", set_path_sql)

        # Second call: SELECT
        select_sql = str(call_args_list[1][0][0])
        self.assertIn("SELECT * FROM songs", select_sql)

    async def test_execute_sql_forbidden(self):
        sql = "DROP TABLE songs"
        with self.assertRaises(ForbiddenSqlStatementException):
            await self.repo.execute_sql(sql)

    async def test_execute_sql_exception(self):
        sql = "SELECT * FROM songs"
        self.mock_conn.execute.side_effect = Exception("DB failure")

        with self.assertRaises(SqlStatementExecutionException):
            await self.repo.execute_sql(sql)

        # Reset side effect for other tests
            self.mock_conn.execute.side_effect = None            

    async def test_fetch_database_schema(self):
        mock_schema_json = '''{
            "album": {
                "columns": {
                    "title": {"column_description": "The album title"},
                    "artist_id": {"column_description": "Artist reference"}
                },
                "table_description": "Album table"
            }
        }'''

        self.mock_result.fetchall = AsyncMock(return_value=[(mock_schema_json,)])
        self.mock_conn.execute.return_value = self.mock_result

        result = await self.repo.fetch_database_schema([0.1, 0.2, 0.3])

        expected = (
            "album:\n"
            "  title: The album title\n"
            "  artist_id: Artist reference\n"
        )
        self.assertEqual(result, expected)

    def test_format_single_schema(self):
        repo = MusicQueryRepository(engine=AsyncMock())
        raw_json = {
            "songs": {
                "columns": {
                    "title": {"column_description": "The title of the song"},
                    "artist_id": {"column_description": "Reference to artist"}
                }
            }
        }

        result = repo._format_single_schema(raw_json)
        expected = [
            "songs:",
            "  title: The title of the song",
            "  artist_id: Reference to artist"
        ]

        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
