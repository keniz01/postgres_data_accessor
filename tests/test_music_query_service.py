import unittest
import asyncio
from unittest.mock import AsyncMock, MagicMock

from data_accessor.domain.interfaces.abstract_music_query_repository import AbstractMusicQueryRepository
from data_accessor.domain.services._music_query_service import MusicQueryService

class TestMusicQueryService(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_repository = MagicMock(spec=AbstractMusicQueryRepository)
        self.mock_repository.execute_sql = AsyncMock()
        self.mock_repository.fetch_database_schema = AsyncMock()
        self.service = MusicQueryService(repository=self.mock_repository)

    async def test_execute_sql_calls_repository(self):
        # Arrange
        sql_query = "SELECT * FROM songs WHERE artist = :artist"
        params = {"artist": "Queen"}
        expected_result = [{"id": 1, "title": "Bohemian Rhapsody"}]
        self.mock_repository.execute_sql.return_value = expected_result

        # Act
        result = await self.service.execute_sql(sql_query, params)

        # Assert
        self.mock_repository.execute_sql.assert_awaited_once_with(sql_query, params)
        self.assertEqual(result, expected_result)

    async def test_fetch_database_schema_calls_repository(self):
        # Arrange
        params = {"schema": "public"}
        expected_schema = [
            {"table": "songs", "columns": ["id", "title", "artist"]},
            {"table": "albums", "columns": ["id", "name"]}
        ]
        self.mock_repository.fetch_database_schema.return_value = expected_schema

        # Act
        result = await self.service.fetch_database_schema(params)

        # Assert
        self.mock_repository.fetch_database_schema.assert_awaited_once_with(params)
        self.assertEqual(result, expected_schema)

    async def test_execute_sql_with_no_params(self):
        # Arrange
        sql_query = "SELECT * FROM songs"
        expected_result = [{"id": 1, "title": "Imagine"}]
        self.mock_repository.execute_sql.return_value = expected_result

        # Act
        result = await self.service.execute_sql(sql_query)

        # Assert
        self.mock_repository.execute_sql.assert_awaited_once_with(sql_query, None)
        self.assertEqual(result, expected_result)

    async def test_fetch_database_schema_with_no_params(self):
        # Arrange
        expected_schema = [{"table": "artists", "columns": ["id", "name"]}]
        self.mock_repository.fetch_database_schema.return_value = expected_schema

        # Act
        result = await self.service.fetch_database_schema()

        # Assert
        self.mock_repository.fetch_database_schema.assert_awaited_once_with(None)
        self.assertEqual(result, expected_schema)

if __name__ == '__main__':
    unittest.main()
