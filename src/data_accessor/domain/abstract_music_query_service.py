from abc import ABC, abstractmethod

class AbstractMusicQueryService(ABC):
    """
    Abstract base class for music query services.
    This class defines the interface for executing SQL queries and fetching database schema.
    """
    @abstractmethod
    def execute_sql(self, sql: str, params: dict = None) -> list:
        """
        Execute a SQL query and return the results.

        :param sql: The SQL query to execute.
        :param params: Optional parameters for the query.
        :return: A list of results from the query.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    @abstractmethod
    def fetch_database_schema(self, params: dict = None) -> list:
        """
        Fetch the database schema for a given schema name.

        :param params: Optional parameters for the query.
        :return: A list of tables and their columns in the schema.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")