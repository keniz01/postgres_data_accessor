from abc import ABC, abstractmethod

class AbstractMusicQueryService(ABC):
    """
    Abstract base class for music query services.
    This class defines the interface for executing SQL queries and fetching database schema.
    """
    @abstractmethod
    async def execute_sql(self, sql: str) -> list:
        """
        Execute a SQL query and return the results.

        :param sql: The SQL query to execute.
        :return: A list of results from the query.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    @abstractmethod
    async def fetch_database_schema(self, prompt_embeddings: list[float]) -> list:
        """
        Fetch the database schema for a given schema name.

        :param prompt_embeddings: Prompt embeddings.
        :return: A list of tables and their columns in the schema.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")