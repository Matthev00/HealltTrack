import json
import pytest
from unittest.mock import patch, MagicMock
import sys

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


def setup_mock_cursor(mock_db_connector):
    mock_cursor = MagicMock()
    mock_db_connector.get_connection.return_value.cursor.return_value.__enter__.return_value = (
        mock_cursor
    )
    return mock_cursor


@pytest.mark.parametrize(
    "data,expected",
    [
        (
            [(1, "Apple", 52, 86)],
            json.dumps(
                [
                    {
                        "food_id": 1,
                        "name": "Apple",
                        "calories_per_100": 52,
                        "serving": 86,
                    }
                ],
                indent=4,
            ),
        ),
        ([], json.dumps([], indent=4)),
    ],
)
def test_get_food_list(data, expected, mock_db_connector, db_handler):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchall.return_value = data

    result = db_handler.get_food_list()

    assert result == expected
    mock_db_connector.get_connection.assert_called_once()


def test_get_food_list_db_error(mock_db_connector, db_handler):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchall.side_effect = Exception("DB error")

    with pytest.raises(Exception, match="DB error"):
        db_handler.get_food_list()

    mock_db_connector.get_connection.assert_called_once()


def test_find_meal_found(db_handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchone.return_value = [1]

    result = db_handler._find_meal("01-01-2022", 2, 10)
    assert result == 1


def test_find_meal_not_found(db_handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchone.return_value = None

    result = db_handler._find_meal("01-01-2022", 2, 10)
    assert result is None


def test_insert_empty_meal(db_handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    db_handler._find_next_id = MagicMock(return_value=1)

    result = db_handler._insert_empty_meal(2)
    assert result == 1
    mock_cursor.execute.assert_called_once()


def test_find_next_id_existing(db_handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchone.return_value = [10]

    result = db_handler._find_next_id("meal")
    assert result == 11


def test_find_next_id_none(db_handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchone.return_value = [None]

    result = db_handler._find_next_id("meal")
    assert result == 1


def test_insert_empty_meal_entry(db_handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    db_handler._find_next_id = MagicMock(return_value=1)

    db_handler._insert_empty_meal_entry(1, 10, "01-01-2022")
    mock_cursor.execute.assert_called_once()


def test_insert_meal_food(db_handler, mock_db_connector):
    mock_cursor = MagicMock()
    mock_db_connector.get_connection.return_value.cursor.return_value.__enter__.return_value = (
        mock_cursor
    )

    db_handler._insert_meal_food(1, 100, 150)
    mock_cursor.execute.assert_called_once()

