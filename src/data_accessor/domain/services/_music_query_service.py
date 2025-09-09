# INTERNAL MODULE: Not for direct import outside data_accessor
if not __name__.startswith("data_accessor"): raise ImportError("_music_query_service is internal and cannot be imported directly.")

from data_accessor.domain.interfaces.abstract_music_query_repository import AbstractMusicQueryRepository
from data_accessor.domain.interfaces.abstract_music_query_service import AbstractMusicQueryService
import logging

class MusicQueryService(AbstractMusicQueryService):
    """
	Service class for music queries.
	This class implements the methods to interact with the music query repository.
	"""
    def __init__(self, repository: AbstractMusicQueryRepository) -> None:
        """
        Initialize the MusicQueryService with a repository (dependency injection).
        """
        self.repository = repository

    async def execute_sql(self, sql: str) -> list:
        try:
            result = await self.repository.execute_sql(sql)
            logging.info("Service: SQL executed successfully.")
            return result
        except Exception as e:
            logging.error(f"Service: Error executing SQL: {e}")
            raise

    async def fetch_database_schema(self, prompt_embeddings: list[float]) -> list:
        try:
            schema = await self.repository.fetch_database_schema(prompt_embeddings)
            logging.info("Service: Fetched database schema.")
            return schema
        except Exception as e:
            logging.error(f"Service: Error fetching schema: {e}")
            raise