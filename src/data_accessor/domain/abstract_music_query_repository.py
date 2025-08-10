from abc import ABC, abstractmethod

class AbstractMusicQueryRepository(ABC):
    """
    Abstract base class for database query repository.
    This class defines the interface for querying data from a database.
    """
    @abstractmethod
    def execute_sql(self, sql: str, params: dict = None) -> list:
        """
        Execute a query and return the results.

        :param query: The SQL query to execute.
        :param params: Optional parameters for the query.
        :return: A list of results from the query.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    @abstractmethod
    def fetch_database_schema(self, schema_name: str, params: dict = None) -> list:
        """
        Fetch the database schema for a given schema name.

        :param schema_name: The name of the schema to fetch.
        :param params: Optional parameters for the query.
        :return: A list of results from the query.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")