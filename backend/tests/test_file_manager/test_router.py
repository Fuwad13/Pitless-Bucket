from fastapi import HTTPException, status
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from pathlib import Path
import uuid
from backend.file_manager.router import fm_service

MOCK_USER = {"uid": str(uuid.uuid4())}
MOCK_FILE_INFO = {
    "uid": uuid.uuid4(),
    "firebase_id": uuid.uuid4(),
    "file_name": "test.txt",
    "content_type": "text/plain",
    "extension": "txt",
    "size": 1024,
    "created_at": "2025-03-22T04:44:11+06:00",
    "updated_at": "2025-03-22T04:44:11+06:00",
}


class TestFileManagerRouter:
    def test_upload_file_success(self, mock_fm_service, test_client: TestClient):
        test_file = Path(__file__).parent / "test.txt"
        assert test_file.exists(), f"Test file {test_file} does not exist"
        mock_fm_service.upload_file.return_value = MOCK_FILE_INFO
        with open(test_file, "rb") as f:
            response = test_client.post(
                "/api/v1/file_manager/upload_file",
                files={"file": ("test.txt", f, "text/plain")},
            )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["file_name"] == "test.txt"
        mock_fm_service.upload_file.assert_called_once()

    def test_upload_file_no_storage_provider(
        self, mock_fm_service, test_client: TestClient
    ):
        mock_fm_service.upload_file.side_effect = HTTPException(
            status_code=400, detail="No storage providers linked"
        )

        test_file = Path(__file__).parent / "test.txt"
        with open(test_file, "rb") as f:
            response = test_client.post(
                "/api/v1/file_manager/upload_file",
                files={"file": ("test.txt", f, "text/plain")},
            )

        assert response.status_code == 400
        assert response.json()["detail"] == "No storage providers linked"
        mock_fm_service.upload_file.assert_called_once()

    def test_list_files_success(self, mock_fm_service, test_client: TestClient):
        mock_fm_service.list_files.return_value = [MOCK_FILE_INFO]

        response = test_client.get("/api/v1/file_manager/list_files")

        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["file_name"] == "test.txt"
        mock_fm_service.list_files.assert_called_once()
