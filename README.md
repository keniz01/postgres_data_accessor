# postgres_data_accessor

## Overview

`postgres_data_accessor` is a Python package for safe, async SQL query execution and schema access on PostgreSQL databases. It provides a layered architecture (Repository, Service, Controller) for clean separation of concerns, dependency injection, and robust exception handling.

---

## Package Distribution & Setup

### Build the Package
Build the package using [uv](https://github.com/astral-sh/uv):

```sh
uv build
```

### Serve the Package Locally
Start a local HTTP server to distribute the built package:

```sh
cd dist && python -m http.server 8080
```

### Install the Package on a Client
Install from your local server (or PyPI):

```sh
uv add --find-links http://localhost:8080 --index https://pypi.org/simple data_accessor
```

### Remove the Installed Package
Uninstall if needed:

```sh
uv remove data_accessor
```


## Running Unit Tests (pytest)

### Run Tests in a Single File

```sh
uv run hatch run dev:test tests/test_music_query_controller.py
```


```sh
uv run hatch run dev:test
```


## Example Usage

Below is a minimal example of how to use the package in your code:

```python
from data_accessor.infrastructure.repositories.music_query_repository import MusicQueryRepository
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine("postgresql+asyncpg://user:password@localhost/dbname")
repo = MusicQueryRepository(schema_name="public", engine=engine)

# Example async usage
import asyncio

async def main():
	result = await repo.execute_sql("SELECT * FROM music_table")
	print(result)

asyncio.run(main())
```

---

## Advanced Usage

### Using the Service and Controller Layers

```python
from data_accessor.infrastructure.repositories.music_query_repository import MusicQueryRepository
from data_accessor.domain.services.music_query_service import MusicQueryService
from data_accessor.application.music_query_controller import MusicQueryController
from sqlalchemy.ext.asyncio import create_async_engine
import asyncio

engine = create_async_engine("postgresql+asyncpg://user:password@localhost/dbname")
repo = MusicQueryRepository(schema_name="public", engine=engine)
service = MusicQueryService(repository=repo)
controller = MusicQueryController(music_query_service=service)

async def run_query():
	try:
		# Run a safe SELECT query
		results = await controller.execute_sql("SELECT * FROM music_table")
		print("Query Results:", results)
	except Exception as e:
		print("Error executing query:", e)

asyncio.run(run_query())
```

### Fetching Database Schema

```python
async def fetch_schema():
	try:
		schema = await controller.fetch_database_schema()
		print("Database Schema:\n", schema)
	except Exception as e:
		print("Error fetching schema:", e)

asyncio.run(fetch_schema())
```

### Custom Dependency Injection

You can inject custom repository or service implementations for testing or extension:

```python
class CustomRepository(MusicQueryRepository):
	# Override methods for custom behavior
	pass

custom_repo = CustomRepository(schema_name="public", engine=engine)
custom_service = MusicQueryService(repository=custom_repo)
custom_controller = MusicQueryController(music_query_service=custom_service)
```

### Exception Handling Example

```python
async def safe_query():
	try:
		# This will raise ForbiddenSqlStatementException for non-SELECT
		await controller.execute_sql("DROP TABLE music_table")
	except Exception as e:
		print("Expected error:", e)

asyncio.run(safe_query())
```

---

## Tips

- All queries must be safe SELECT statements.
- Use dependency injection for testing and extension.
- Logging is built-in for traceability and debugging.
