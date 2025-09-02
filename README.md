# postgres_data_accessor


## Solution Architecture

Below is a high-level architecture diagram for the solution:

### Layered Architecture


```
 +---------------------------+
 |   Application Layer       |
 |   (Controller)            |
 +---------------------------+
          |
          v
 +---------------------------+
 |      Domain Layer         |
 |   (Service, Interfaces,   |
 |    Models, Exceptions)    |
 +---------------------------+
          |
          v
 +---------------------------+
 |  Infrastructure Layer     |
 |   (Repository, DB Config) |
 +---------------------------+
          |
          v
 +---------------------------+
 |   PostgreSQL Database     |
 +---------------------------+
```


**Description:**
- **Application Layer (Controller):** Handles incoming requests and delegates to the domain layer. Acts as the entry point for client/API interactions.
- **Domain Layer (Service, Interfaces, Models, Exceptions):** Contains business logic, domain models, interfaces, and exception handling. Responsible for core functionality and rules.
- **Infrastructure Layer (Repository, DB Config):** Implements data access, repository pattern, and configuration management. Interacts directly with the PostgreSQL database.
- **Dependency Injection:** Used between layers to promote testability, flexibility, and loose coupling.

---

> For a more detailed diagram, you can add an image:
> 
> ![Solution Architecture](docs/solution_architecture.png)

---
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


```sh
# On Windows:
uv run hatch run dev:test

# On macOS/Linux:
source .venv/bin/activate  # Activate virtual environment first
PYTHONPATH=src pytest tests/
```


## Example Usage

> **Note:** Only `MusicQueryController` is exposed as the public API. Service and repository layers are internal and not intended for direct use outside the package.

Below is a minimal example of how to use the package in your code:

```python
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine("postgresql+asyncpg://user:password@localhost/dbname")
repo = MusicQueryRepository(schema_name="public", engine=engine)
service = MusicQueryService(repository=repo)
controller = MusicQueryController(music_query_service=service)

async def main():
    result = await controller.execute_sql("SELECT * FROM music_table")
    print(result)

asyncio.run(main())
```
---

## Advanced Usage

### Fetching Database Schema

```python
async def fetch_schema():
    schema = await controller.fetch_database_schema()
    print("Database Schema:\n", schema)
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

---

## Internal API Restriction
- Only import `MusicQueryController` from the package root: `from data_accessor import MusicQueryController`
- Internal modules (`_music_query_service.py`, `_music_query_repository.py`) are not intended for direct use and will raise an ImportError if imported outside the package context.

---

## Tips

- All queries must be safe SELECT statements.
- Use dependency injection for testing and extension.
- Logging is built-in for traceability and debugging.

## Note: Only MusicQueryController is public API. Service and repository are internal.
