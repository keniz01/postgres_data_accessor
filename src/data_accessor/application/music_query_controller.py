from src.data_accessor.domain.abstract_music_query_service import AbstractMusicQueryService

class MusicQueryController:
    def __init__(self, music_query_service: AbstractMusicQueryService):
        self.music_query_service = music_query_service

    async def fetch_database_schema(self, params: dict = None) -> list:
        schema = await self.music_query_service.fetch_database_schema(params)
        return schema

    async def execute_sql(self, sql: str, params: dict = None) -> list:
        response = await self.music_query_service.execute_sql(sql, params)
        return response