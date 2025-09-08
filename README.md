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

`postgres_data_accessor` is a Python package for safe, asynchronous SQL query execution and schema access on PostgreSQL databases. It provides a layered architecture (Repository, Service, Controller) for clean separation of concerns, dependency injection, and robust exception handling. The package includes comprehensive test coverage and supports both Windows and Unix-based systems.

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
Install from your local server:

```sh
uv add --find-links http://localhost:8080 --index https://pypi.org/simple data_accessor
```

### Remove the Installed Package
Uninstall if needed:

```sh
uv remove data_accessor
```

## Configuration

### Database Configuration
Configuration can be done via TOML file (`secrets.toml`):

```toml
[database]
host = "localhost"
port = 5432
database = "your_database"
user = "your_user"
password = "your_password"
schema = "public"  # default schema
```

Or programmatically:

```python
from data_accessor.infrastructure.database_config import DatabaseConfig

config = DatabaseConfig(
    host="localhost",
    port=5432,
    database="your_database",
    user="your_user",
    password="your_password",
    schema="public"
)
```

### Error Handling
The package provides several custom exceptions:

```python
try:
    result = await controller.execute_sql("SELECT * FROM table")
except ForbiddenSqlStatementException:
    # Handle non-SELECT statements
    logger.error("Only SELECT statements are allowed")
except SqlStatementExecutionException as e:
    # Handle execution errors
    logger.error(f"Query execution failed: {e}")
except Exception as e:
    # Handle other errors
    logger.error(f"Unexpected error: {e}")
```


## Running Unit Tests
The project uses Python's built-in unittest framework with async support and includes code coverage metrics.

### Setting Up the Environment
Create and activate a virtual environment:

```sh
# On Windows:
python -m venv .venv
.venv\Scripts\activate

# On macOS/Linux:
python -m venv .venv
source .venv/bin/activate
```

Install the package in development mode:
```sh
uv pip install -e .
```

### Running Tests

There are several ways to run the tests:

1. Using the test runner script (with coverage):
```sh
python tests/run_tests.py
```

2. Using unittest directly:
```sh
PYTHONPATH=src python -m unittest discover tests/ -v
```

3. Using coverage manually:
```sh
coverage run -m unittest discover tests/
coverage report
coverage html  # generates HTML report
```

### Code Coverage

The project includes code coverage metrics using coverage.py. The current coverage report shows:

- Total coverage: 58%
- Coverage by component:
  - Application Layer: ~71%
  - Domain Layer: ~85%
  - Infrastructure Layer: ~41%

A detailed HTML coverage report is generated in the `coverage_html_report` directory after running tests with coverage.


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

The package supports semantic schema retrieval using vector embeddings. When fetching the database schema, you provide an embeddings vector that represents your schema query, and the system returns the most relevant schema information based on vector similarity.

```python
async def fetch_schema():
    # The embeddings vector represents your schema query
    embeddings = "[-0.5179322957992554, 0.654964804649353, ...]"  # 384-dimensional vector
    schema = await controller.fetch_database_schema(embeddings)
    print("Database Schema:\n", schema)

asyncio.run(fetch_schema())
```

The schema information is returned in a readable format showing tables, columns, and their descriptions. Example output:

```
album:
  title: The title column contains the name of the album
  album_id: The album_id column contains the primary key for the album table
  duration: The duration column contains the time it takes an album to complete playing
  genre_id: The genre_id column maintains a reference to the genre.genre_id column
  ...

track:
  title: The title column contains the name of the track
  track_id: The track_id column contains the primary key for the track table
  ...
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

## Technical Details

### Dependencies
- Python >=3.12
- Core dependencies:
  - asyncpg>=0.30.0 - Asynchronous PostgreSQL driver
  - SQLAlchemy>=2.0.42 [asyncio] - SQL toolkit and ORM with async support
  - Pydantic>=2.11.7 - Data validation using Python type annotations
  - sqlparse>=0.5.3 - SQL parsing and formatting
  - toml>=0.10.2 - Configuration file parsing

### Package Structure
```
src/data_accessor/
├── application/           # Application layer
│   ├── __init__.py
│   └── music_query_controller.py
├── domain/               # Domain layer
│   ├── exceptions/       # Custom exceptions
│   ├── interfaces/       # Abstract base classes
│   ├── models/          # Domain models
│   └── services/        # Business logic
└── infrastructure/       # Infrastructure layer
    ├── database_config.py
    └── repositories/     # Data access
```

### Key Features
1. **Asynchronous Operations**
   - All database operations are async/await compatible
   - Connection pooling for efficient resource utilization
   - Proper connection cleanup and resource management

2. **SQL Safety**
   - Only SELECT statements are allowed by default
   - SQL injection prevention through parameterized queries
   - SQL statement validation and sanitization

3. **Error Handling**
   - Custom exception hierarchy
   - Detailed error messages with context
   - Proper async context management

4. **Type Safety**
   - Pydantic models for request/response validation
   - Strong typing throughout the codebase
   - Runtime type checking

### Performance Considerations
- Connection pooling via asyncpg
- Prepared statement caching
- Lazy loading of database schemas
- Efficient query parsing using sqlparse

### Security
1. **Query Validation**
   - SQL statement type checking
   - Prevention of data modification statements
   - Schema-based access control

2. **Configuration Security**
   - Secure credential management
   - Environment-based configuration
   - Connection string validation

### Logging and Monitoring
- Built-in logging with configurable levels
- SQL statement logging for debugging
- Performance metrics logging
- Exception tracking and reporting

### Best Practices
1. **Usage Guidelines**
   - Always use the public API (`MusicQueryController`)
   - Implement proper error handling
   - Use connection pooling for better performance
   - Configure logging appropriately

2. **Development Guidelines**
   - Follow the layered architecture pattern
   - Use dependency injection for testing
   - Maintain async/await consistency
   - Add tests for new features

3. **SQL Guidelines**
   - Use parameterized queries
   - Keep queries simple and readable
   - Validate schema names
   - Use proper SQL formatting

### Known Limitations
- Only supports PostgreSQL databases
- SELECT statements only (by design)
- Python 3.12+ required
- Async execution model required

## Note: Only MusicQueryController is public API. Service and repository are internal.
