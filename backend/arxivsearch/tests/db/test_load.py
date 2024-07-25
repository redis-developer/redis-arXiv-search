# import pytest
from unittest.mock import mock_open, patch

from arxivsearch.db.load import read_paper_json


# Test when the file exists locally
@patch("arxivsearch.db.load.os.path.join")
@patch(
    "arxivsearch.db.load.open",
    new_callable=mock_open,
    read_data='[{"id": "1234", "title": "Test Paper"}]',
)
@patch("arxivsearch.db.load.json.load")
def test_read_paper_json_local(mock_json_load, mock_file_open, mock_path_join):
    mock_path_join.return_value = "dummy_path"
    mock_json_load.return_value = [{"id": "1234", "title": "Test Paper"}]

    result = read_paper_json()

    mock_file_open.assert_called_once_with("dummy_path", "r")
    mock_json_load.assert_called_once()
    assert result == [{"id": "1234", "title": "Test Paper"}]


# Test when the file needs to be fetched from S3
@patch("arxivsearch.db.load.os.path.join")
@patch("arxivsearch.db.load.read_from_s3")
@patch("arxivsearch.db.load.json.load", side_effect=Exception("File not found"))
def test_read_paper_json_s3(
    mock_json_load,
    mock_read_from_s3,
    mock_path_join,
):
    mock_path_join.return_value = "dummy_path"
    mock_read_from_s3.return_value = [{"id": "5678", "title": "Test Paper from S3"}]

    result = read_paper_json()

    mock_read_from_s3.assert_called_once()
    mock_read_from_s3.assert_called_with("dummy_path")

    assert result == [{"id": "5678", "title": "Test Paper from S3"}]
