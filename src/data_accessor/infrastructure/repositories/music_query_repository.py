import sqlparse
from collections import defaultdict
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, List, Optional, Tuple, Union
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection, AsyncEngine
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio.result import AsyncResult
from sqlalchemy import text
from pydantic import Field
from typing_extensions import Annotated
from data_accessor.domain.interfaces.abstract_music_query_repository import AbstractMusicQueryRepository
from data_accessor.domain.exceptions.forbidden_sql_statement_exception import ForbiddenSqlStatementException
from data_accessor.domain.exceptions.sql_statement_execution_exception import SqlStatementExecutionException


class MusicQueryRepository(AbstractMusicQueryRepository):
    """
    Repository class for music queries.
    """

    def __init__(
        self,
        schema_name: Annotated[str, Field(description="The database schema name to connect to.")],
        connection_string: Annotated[str, Field(description="The database connection string")]
    ) -> None:
        self.schema_name: str = schema_name
        self.engine: AsyncEngine = create_async_engine(connection_string, echo=True)

    @asynccontextmanager
    async def get_conn(self) -> AsyncGenerator[AsyncConnection, None]:
        async with self.engine.connect() as conn:
            await conn.execute(text(f"SET search_path TO {self.schema_name}"))
            yield conn

    async def execute_sql(self, sql: str, params: Optional[dict] = None) -> Union[List[Tuple[Any, ...]], str]:
        """
        Execute a SQL query and return the results or a success message.
        Only SELECT statements are allowed.
        """
        import logging
        try:
            if not self.is_safe_select_query(sql):
                raise ForbiddenSqlStatementException("Only SELECT statements are allowed.")

            async with self.get_conn() as conn:
                result: Union[AsyncResult, CursorResult] = await conn.execute(text(sql), params or {})
                if result.returns_rows:
                    return result.fetchall()
                return f"Query executed successfully, {result.rowcount} row(s) affected."
        except ForbiddenSqlStatementException as e:
            logging.warning(f"Forbidden SQL statement: {e.message}")
            raise e
        except Exception as e:
            logging.error(f"Error executing SQL statement: {e}")
            raise SqlStatementExecutionException(f"Error: {type(e).__name__}: {e}")

    async def fetch_database_schema(self, params: Optional[dict] = None) -> str:
        """
        Fetch the database schema: tables, columns, and data types.
        """
        query = text("""
            SELECT table_name, column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = :schema_name
            ORDER BY table_name, ordinal_position
        """)

        async with self.get_conn() as conn:
            result: AsyncResult = await conn.execute(query, {"schema_name": self.schema_name})
            rows = result.fetchall()

        grouped = defaultdict(list)
        for table, column, dtype in rows:
            grouped[table].append(f"  {column}: {dtype}")

        return "\n".join(f"{table}:\n" + "\n".join(cols) for table, cols in grouped.items())
        
    def is_safe_select_query(self, query: str) -> bool:
        """
        Enhanced SQL safety check:
        - Only single SELECT statements allowed
        - No semicolons, comments, or transaction control
        - No CTEs (WITH ...)
        """
        parsed = sqlparse.parse(query)
        if not parsed or len(parsed) != 1:
            return False

        stmt = parsed[0]
        stmt_type = stmt.get_type()
        if stmt_type != 'SELECT':
            return False

        # Disallow CTEs (WITH ...)
        if any(token.ttype is sqlparse.tokens.Keyword and token.value.upper() == "WITH" for token in stmt.tokens):
            return False

        # Disallow semicolons (multiple statements)
        if ";" in query:
            return False

        # Disallow comments
        if "--" in query or "/*" in query:
            return False

        # Disallow transaction control and DML/DDL
        forbidden = {"delete", "insert", "update", "drop", "create", "alter", "commit", "rollback"}
        tokens = [token for token in stmt.tokens if not token.is_whitespace]
        for token in tokens:
            if str(token).strip().lower() in forbidden:
                return False

        return True

        
