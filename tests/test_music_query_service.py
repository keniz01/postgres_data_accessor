import pytest
from unittest.mock import AsyncMock, MagicMock

from data_accessor.domain.interfaces.abstract_music_query_repository import AbstractMusicQueryRepository
from data_accessor.domain.services._music_query_service import MusicQueryService


@pytest.fixture
def mock_repository():
    repo = MagicMock(spec=AbstractMusicQueryRepository)
    repo.execute_sql = AsyncMock()
    repo.fetch_database_schema = AsyncMock()
    return repo

@pytest.fixture
def music_query_service(mock_repository):
    return MusicQueryService(repository=mock_repository)

async def test_execute_sql_calls_repository(music_query_service, mock_repository):
    # Arrange
    sql_query = "SELECT * FROM songs WHERE artist = :artist"
    params = {"artist": "Queen"}
    expected_result = [{"id": 1, "title": "Bohemian Rhapsody"}]
    mock_repository.execute_sql.return_value = expected_result

    # Act
    result = await music_query_service.execute_sql(sql_query, params)

    # Assert
    mock_repository.execute_sql.assert_awaited_once_with(sql_query, params)
    assert result == expected_result

async def test_fetch_database_schema_calls_repository(music_query_service, mock_repository):
    # Arrange
    params = {"schema": "public"}
    expected_schema = [
        {"table": "songs", "columns": ["id", "title", "artist"]},
        {"table": "albums", "columns": ["id", "name"]}
    ]
    mock_repository.fetch_database_schema.return_value = expected_schema

    # Act
    result = await music_query_service.fetch_database_schema(params)

    # Assert
    mock_repository.fetch_database_schema.assert_awaited_once_with(params)
    assert result == expected_schema

async def test_execute_sql_with_no_params(music_query_service, mock_repository):
    # Arrange
    sql_query = "SELECT * FROM songs"
    expected_result = [{"id": 1, "title": "Imagine"}]
    mock_repository.execute_sql.return_value = expected_result

    # Act
    result = await music_query_service.execute_sql(sql_query)

    # Assert
    mock_repository.execute_sql.assert_awaited_once_with(sql_query, None)
    assert result == expected_result

async def test_fetch_database_schema_with_no_params(music_query_service, mock_repository):
    # Arrange
    expected_schema = [{"table": "artists", "columns": ["id", "name"]}]
    mock_repository.fetch_database_schema.return_value = expected_schema

    # Act
    result = await music_query_service.fetch_database_schema()

    # Assert
    mock_repository.fetch_database_schema.assert_awaited_once_with(None)
    assert result == expected_schema
