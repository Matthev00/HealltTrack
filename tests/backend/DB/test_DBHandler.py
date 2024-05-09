import pytest
from unittest.mock import patch, MagicMock
import sys

sys.path.append("backend/DB")
from DBHandler import DBHandler as Handler  # noqa5501
from DBConnector import DBConnector  # noqa5501


@pytest.fixture(scope="module")
def mock_db_connector():
    with patch("DBConnector.DBConnector") as mock:
        instance = mock.return_value
        instance.get_connection.return_value = MagicMock()
        DBConnector._instance = instance
        yield instance


@pytest.fixture(scope="module")
def handler(mock_db_connector):
    credentials = {
        "user": "admin",
        "password": "password",
        "dsn": "dsn",
        "cdir": "config_dir",
        "wltloc": "wallet_location",
        "wltpsw": "wallet_password",
    }
    return Handler(wallet_credentials=credentials)


def setup_mock_cursor(mock_db_connector):
    mock_cursor = MagicMock()
    mock_db_connector.get_connection.return_value.cursor.return_value.__enter__.return_value = (  # noqa5501
        mock_cursor
    )
    return mock_cursor


def test_find_next_id_empty_table(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchone.return_value = [None]

    result = handler._find_next_id("test_table")

    assert result == 1
    mock_cursor.execute.assert_called_once_with(
        "SELECT MAX(test_table_id) FROM test_table"
    )


def test_find_next_id_non_empty_table(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchone.return_value = [10]

    result = handler._find_next_id("test_table")

    assert result == 11
    mock_cursor.execute.assert_called_once_with(
        "SELECT MAX(test_table_id) FROM test_table"
    )
