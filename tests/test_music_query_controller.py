import unittest

from src.data_accessor.application.music_query_controller import MusicQueryController
from src.data_accessor.domain.music_query_service import MusicQueryService
from src.data_accessor.infrastructure.music_query_repository import MusicQueryRepository

class TestMusicQueryController(unittest.TestCase):

    async def setUp(self):
        self.connection_string = "postgresql+asyncpg://postgres:postgres@localhost:5432/analysis"
        self.schema_name = "music"
        self.controller = MusicQueryController(
            music_query_service=MusicQueryService(MusicQueryRepository(self.schema_name, self.connection_string))
        )

    async def test_music_query_database_schema(self):

        # When
        schema_response = await self.controller.fetch_database_schema(self.schema_name)

        # Then
        self.assertIsNotNone(schema_response, "Schema response should not be None")
        self.assertIn('tables', schema_response, "Schema response should contain 'tables' key")
        self.assertGreater(len(schema_response['tables']), 0, "Schema should contain at least one table")

    async def test_music_query_can_execute_sql(self):

        # When
        sql_response = await self.controller.execute_sql("SELECT * FROM track LIMIT 10")

        # Then
        self.assertIsNotNone(sql_response, "SQL response should not be None")
        self.assertIn('rows', sql_response, "SQL response should contain 'rows' key")
        self.assertGreater(len(sql_response['rows']), 0, "SQL response should contain at least one row.")
