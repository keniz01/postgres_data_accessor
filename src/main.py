
import asyncio
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from data_accessor.application.music_query_controller import MusicQueryController
from data_accessor.domain.services._music_query_service import MusicQueryService
from data_accessor.infrastructure.repositories._music_query_repository import MusicQueryRepository
from data_accessor.infrastructure.database_config import DatabaseConfig

# Use DatabaseConfig to abstract credentials and connection string
db_config = DatabaseConfig()
engine = create_async_engine(db_config.connection_string)
repo = MusicQueryRepository(schema_name="analysis", engine=engine)
service = MusicQueryService(repository=repo)
controller = MusicQueryController(music_query_service=service)

async def main():
    result = await controller.fetch_database_schema()
    print(result)

asyncio.run(main())
