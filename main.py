from src.data_accessor.application.music_query_controller import MusicQueryController
from src.data_accessor.domain.music_query_service import MusicQueryService
from src.data_accessor.infrastructure.music_query_repository import MusicQueryRepository
import toml

async def main():
    config = toml.load('config/database_config.toml')
    connection_string = config['database']['connection_string']
    schema_name = config['database']['schema_name']
    controller = MusicQueryController(music_query_service=MusicQueryService(MusicQueryRepository(schema_name, connection_string)))
    sql_response = await controller.execute_sql("SELECT * FROM track LIMIT 10")
    print("SQL REPSONSE: ", sql_response)
    schema_response = await controller.fetch_database_schema(schema_name)
    print("SCHEMA REPSONSE: ", schema_response)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
