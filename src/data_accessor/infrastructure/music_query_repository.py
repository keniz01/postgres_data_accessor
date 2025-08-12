from collections import defaultdict
from contextlib import asynccontextmanager
from pydantic import Field
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection
from sqlalchemy import text
from typing import Annotated, AsyncGenerator
from src.data_accessor.domain.abstract_music_query_repository import AbstractMusicQueryRepository
        
class MusicQueryRepository(AbstractMusicQueryRepository):
    """
	Repository class for music queries.
	This class implements the methods to interact with the music query repository.
	"""
    def __init__(
            self, 
            schema_name: Annotated[ str, Field( description="The database schema name to connect to." )], 
            connection_string: Annotated[ str, Field( description="The database connection string" )]) -> None:
        """
        Initialize the MusicQueryRepository with a schema name.
        :param schema_name: The name of the schema to connect to.
        """
        self.schema_name = schema_name
        self.engine = create_async_engine(connection_string, echo=True, future=True)
        self.schema_name = schema_name

    @asynccontextmanager
    async def get_conn(self) -> AsyncGenerator[AsyncConnection, None]:
        async with self.engine.connect() as conn:
            await conn.execute(text(f"SET search_path TO {self.schema_name}"))
            yield conn

    async def execute_sql(self, sql: str, params: dict = None) -> list:
        """
        Execute a SQL query and return the results.

        :param sql: The SQL query to execute.
        :param params: Optional parameters for the query.
        :return: A list of results from the query.
        """
        try:
            if not sql.lower().startswith(("select", "insert", "update", "delete")):
                return "Only SELECT, INSERT, UPDATE, DELETE statements are allowed."

            async with self.get_conn() as conn:
                cursor_result = await conn.execute(text(sql))
                if cursor_result.returns_rows:
                    sql_response_context = await cursor_result.fetchall() 
                    return sql_response_context
        except Exception as e:
            return f"Error: {type(e).__name__}: {e}"

    async def fetch_database_schema(self, params: dict = None) -> list:
        """
        Fetch the database schema for a given schema name.

        :param schema_name: The name of the schema to fetch.
        :param params: Optional parameters for the query.
        :return: A list of tables and their columns in the schema.
        """
        query = text("""
            SELECT table_name, column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = :schema_name
            ORDER BY table_name, ordinal_position
        """)
        async with self.get_conn() as conn:
            result = await conn.execute(query, {"schema_name": self.schema_name})
            rows = await result.fetchall()

        grouped = defaultdict(list)
        for table, column, dtype in rows:
            grouped[table].append(f"  {column}: {dtype}")
        return "\n".join(f"{table}:\n" + "\n".join(cols) for table, cols in grouped.items())