import sqlparse
from collections import defaultdict
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, List, Optional, Tuple, Union
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio.result import AsyncResult
from sqlalchemy import text
from data_accessor.domain.interfaces.abstract_music_query_repository import AbstractMusicQueryRepository
from data_accessor.domain.exceptions.forbidden_sql_statement_exception import ForbiddenSqlStatementException
from data_accessor.domain.exceptions.sql_statement_execution_exception import SqlStatementExecutionException
import logging

# INTERNAL MODULE: Not for direct import outside data_accessor
if not __name__.startswith("data_accessor"): raise ImportError("_music_query_repository is internal and cannot be imported directly.")

class MusicQueryRepository(AbstractMusicQueryRepository):
    """
    Repository class for music queries.
    """

    def __init__(
        self,
        engine: AsyncEngine
    ) -> None:
        self.engine: AsyncEngine = engine

    @asynccontextmanager
    async def get_conn(self, schema_name: str) -> AsyncGenerator[AsyncConnection, None]:
        conn = await self.engine.connect()
        try:
            await conn.execute(text(f"SET search_path TO {schema_name}"))
            yield conn
        finally:
            await conn.close()

    async def execute_sql(self, sql: str) -> Union[List[Tuple[Any, ...]], str]:
        try:
            if not self.is_safe_select_query(sql):
                logging.warning(f"Forbidden SQL statement attempted: {sql}")
                raise ForbiddenSqlStatementException("Only SELECT statements are allowed.")
            async with self.get_conn("music") as conn:
                result: Union[AsyncResult, CursorResult] = await conn.execute(text(sql))
                if result.returns_rows:
                    rows = result.fetchall()
                    logging.info(f"SQL executed successfully, returned {len(rows)} rows.")
                    return rows
                msg = f"Query executed successfully, {result.rowcount} row(s) affected."
                logging.info(msg)
                return msg
        except ForbiddenSqlStatementException as e:
            logging.warning(f"Forbidden SQL statement: {e.message}")
            raise e
        except Exception as e:
            logging.error(f"Error executing SQL statement: {e}")
            raise SqlStatementExecutionException(f"Error: {type(e).__name__}: {e}")

    async def fetch_database_schema(self, prompt_embeddings: str) -> str:
        query = text("""
            SELECT raw_json, (embeddings <#> CAST(:prompt_embeddings AS vector)) as cosine_similarity
            FROM schema_embeddings
            ORDER BY cosine_similarity DESC
            LIMIT 4
        """)
        try:
            async with self.get_conn("meta") as conn:
                result: AsyncResult = await conn.execute(query, {"prompt_embeddings": prompt_embeddings, "schema_name": "meta"})
                rows = result.fetchall()
            
            schema_str = ""
            for row in rows:
                raw_json_data = row[0]  # Get the raw_json column which is already a dictionary in PostgreSQL
                for table_name, table_info in raw_json_data.items():
                    schema_str += f"{table_name}:\n"
                    if isinstance(table_info, dict) and 'columns' in table_info:
                        for column_name, column_info in table_info['columns'].items():
                            description = column_info.get('column_description', '') if isinstance(column_info, dict) else str(column_info)
                            schema_str += f"  {column_name}: {description}\n"
                    schema_str += "\n"
            
            logging.info(f"Fetched database schema for meta")
            return schema_str
        except Exception as e:
            logging.error(f"Error fetching database schema: {e}")
            raise SqlStatementExecutionException(f"Error: {type(e).__name__}: {e}")
        
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


