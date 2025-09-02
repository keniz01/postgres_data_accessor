from data_accessor.domain.interfaces.abstract_music_query_repository import AbstractMusicQueryRepository
from data_accessor.domain.interfaces.abstract_music_query_service import AbstractMusicQueryService
import logging

class MusicQueryService(AbstractMusicQueryService):
    """
	Service class for music queries.
	This class implements the methods to interact with the music query repository.
	"""
    def __init__(self, repository: AbstractMusicQueryRepository):
        """
        Initialize the MusicQueryService with a repository (dependency injection).
        """
        self.repository = repository

    async def execute_sql(self, sql: str, params: dict = None) -> list:
        try:
            result = await self.repository.execute_sql(sql, params)
            logging.info("Service: SQL executed successfully.")
            return result
        except Exception as e:
            logging.error(f"Service: Error executing SQL: {e}")
            raise

    async def fetch_database_schema(self, params: dict = None) -> list:
        try:
            schema = await self.repository.fetch_database_schema(params)
            logging.info("Service: Fetched database schema.")
            return schema
        except Exception as e:
            logging.error(f"Service: Error fetching schema: {e}")
            raise