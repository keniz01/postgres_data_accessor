import unittest
import asyncio
from unittest.mock import AsyncMock, create_autospec    
from data_accessor.domain.interfaces.abstract_music_query_service import AbstractMusicQueryService
from data_accessor.application.music_query_controller import MusicQueryController

class TestMusicQueryController(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_service = create_autospec(AbstractMusicQueryService, instance=True)
        self.mock_service.fetch_database_schema = AsyncMock()
        self.mock_service.execute_sql = AsyncMock()
        self.controller = MusicQueryController(self.mock_service)

    async def test_fetch_database_schema(self):
        mock_response = [{"table": "songs"}, {"table": "artists"}]
        embeddings = [2132131]
        self.mock_service.fetch_database_schema.return_value = mock_response

        result = await self.controller.fetch_database_schema(embeddings)

        self.mock_service.fetch_database_schema.assert_awaited_once_with(embeddings)
        self.assertEqual(result, mock_response)

    async def test_execute_sql(self):
        sql = "SELECT * FROM songs"
        mock_response = [{"id": 1, "title": "Imagine"}]
        self.mock_service.execute_sql.return_value = mock_response

        result = await self.controller.execute_sql(sql)

        self.mock_service.execute_sql.assert_awaited_once_with(sql)
        self.assertEqual(result, mock_response)

if __name__ == '__main__':
    unittest.main()
