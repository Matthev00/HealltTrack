import json
import pytest
from unittest.mock import patch, MagicMock
import sys
from typing import Dict

sys.path.append("backend/DB")
from DBHandler import DBHandler
from DBConnector import DBConnector


@pytest.fixture(scope="module")
def mock_db_connector():
    with patch("DBConnector.DBConnector") as mock:
        instance = mock.return_value
        instance.get_connection.return_value = MagicMock()
        DBConnector._instance = instance
        yield instance


@pytest.fixture(scope="module")
def db_handler(mock_db_connector):
    credentials = {
        "user": "admin",
        "password": "password",
        "dsn": "dsn",
        "cdir": "config_dir",
        "wltloc": "wallet_location",
        "wltpsw": "wallet_password",
    }
    return DBHandler(wallet_credentials=credentials)


@pytest.mark.parametrize("data,expected", [
    ([(1, "Apple", 52, 86)], json.dumps([{"food_id": 1, "name": "Apple", "calories_per_100": 52, "serving": 86}], indent=4)),
    ([], json.dumps([], indent=4)),  # No data case
])
def test_get_food_list(data, expected, mock_db_connector, db_handler):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = data
    mock_db_connector.get_connection.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    result = db_handler.get_food_list()

    assert result == expected
    mock_db_connector.get_connection.assert_called_once()


def test_get_food_list_db_error(mock_db_connector, db_handler):
    mock_cursor = MagicMock()
    mock_cursor.fetchall.side_effect = Exception("DB error")
    mock_db_connector.get_connection.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    with pytest.raises(Exception, match="DB error"):
        db_handler.get_food_list()

    mock_db_connector.get_connection.assert_called_once()
