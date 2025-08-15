import pytest
from unittest.mock import AsyncMock, create_autospec

from data_accessor.domain.abstract_music_query_service import AbstractMusicQueryService
from data_accessor.application.music_query_controller import MusicQueryController

@pytest.fixture
def mock_music_query_service():
    mock_service = create_autospec(AbstractMusicQueryService, instance=True)
    mock_service.fetch_database_schema = AsyncMock()
    mock_service.execute_sql = AsyncMock()
    return mock_service

@pytest.fixture
def controller(mock_music_query_service):
    return MusicQueryController(mock_music_query_service)

@pytest.mark.asyncio
async def test_fetch_database_schema(controller, mock_music_query_service):
    mock_response = [{"table": "songs"}, {"table": "artists"}]
    mock_music_query_service.fetch_database_schema.return_value = mock_response

    result = await controller.fetch_database_schema(params={"include_views": True})

    mock_music_query_service.fetch_database_schema.assert_awaited_once_with({"include_views": True})
    assert result == mock_response

@pytest.mark.asyncio
async def test_execute_sql(controller, mock_music_query_service):
    sql = "SELECT * FROM songs"
    mock_response = [{"id": 1, "title": "Imagine"}]
    mock_music_query_service.execute_sql.return_value = mock_response

    result = await controller.execute_sql(sql, params=None)

    mock_music_query_service.execute_sql.assert_awaited_once_with(sql, None)
    assert result == mock_response
