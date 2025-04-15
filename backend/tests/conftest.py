import uuid
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest
from fastapi.testclient import TestClient

from backend import app
from backend.auth.dependencies import get_current_user
from backend.db.main import get_session
from backend.file_manager.router import fm_service

mock_user_service = Mock()


MOCK_USER = {"uid": str(uuid.uuid4())}


@pytest.fixture
def mock_auth():
    with patch("backend.auth.dependencies.get_current_user") as mock:
        mock.return_value = MOCK_USER
        yield mock


@pytest.fixture
def mock_fm_service():
    mock = MagicMock()
    mock.upload_file = AsyncMock()
    mock.list_files = AsyncMock()
    with patch("backend.file_manager.router.fm_service", new=mock):
        yield mock


@pytest.fixture
def test_client(mock_auth):
    async def mock_get_session():
        session = MagicMock()
        session.exec = AsyncMock(return_value=[("mock_provider_id", "test")])
        return session

    app.dependency_overrides[get_session] = mock_get_session
    app.dependency_overrides[get_current_user] = lambda: MOCK_USER
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def mock_file_service():
    with patch("backend.file_manager.service.FileManagerService") as mock:
        yield mock
