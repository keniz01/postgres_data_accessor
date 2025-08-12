from src.data_accessor.domain.abstract_music_query_repository import AbstractMusicQueryRepository
from src.data_accessor.domain.abstract_music_query_service import AbstractMusicQueryService

class MusicQueryService(AbstractMusicQueryService):
    """
	Service class for music queries.
	This class implements the methods to interact with the music query repository.
	"""
    def __init__(self, repository: AbstractMusicQueryRepository):
        """
        Initialize the MusicQueryService with a repository.
        """
        self.repository = repository

    async def execute_sql(self, sql: str, params: dict = None) -> list:
        """
        Execute a SQL query and return the results.

        :param sql: The SQL query to execute.
        :param params: Optional parameters for the query.
        :return: A list of results from the query.
        """
        return await self.repository.execute_sql(sql, params)

    async def fetch_database_schema(self, params: dict = None) -> list:
        """
        Fetch the database schema for a given schema name.

        :param params: Optional parameters for the query.
        :return: A list of tables and their columns in the schema.
        """
        return await self.repository.fetch_database_schema(params)