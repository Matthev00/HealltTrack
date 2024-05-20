import pytest
from unittest.mock import patch, MagicMock
import sys
import oracledb
import json

sys.path.append("backend/DB")
from ActivityHandler import ActivityHandler as Handler  # noqa5501
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


def test_add_activity_entry_success(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchone.return_value = [1]
    entry_dict = {
        "user_id": 1,
        "date": "01-01-2022-15-30",
        "activity_id": 101,
        "duration": 60,
        "calories_burned": 500,
    }

    handler.add_activity_entry(entry_dict)

    mock_cursor.execute.call_count == 2


def test_add_activity_entry_db_error(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchone.return_value = [1]
    mock_cursor.execute.side_effect = oracledb.DatabaseError("Database error")

    entry_dict = {
        "user_id": 1,
        "date": "01-01-2022-15-30",
        "activity_id": 101,
        "duration": 60,
        "calories_burned": 500,
    }

    with pytest.raises(oracledb.DatabaseError):
        handler.add_activity_entry(entry_dict)


def test_get_activity_history(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchall.return_value = [
        ("01-01-2022-15-30", "Running", 1800, 300),
        ("01-01-2022-16-30", "Swimming", 3600, 600),
    ]

    result = handler.get_activity_history(1)
    expected_result = json.dumps(
        [
            {
                "date_time": "01-01-2022-15-30",
                "activity_name": "Running",
                "duration": 30,
                "calories_burned": 300,
            },
            {
                "date_time": "01-01-2022-16-30",
                "activity_name": "Swimming",
                "duration": 60,
                "calories_burned": 600,
            },
        ],
        indent=4,
    )

    assert result == expected_result
    mock_cursor.execute.assert_called_once()


def test_get_activity_history_empty(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchall.return_value = []

    result = handler.get_activity_history(1)
    expected_result = json.dumps(
        [],
        indent=4,
    )

    assert result == expected_result
    mock_cursor.execute.assert_called_once()


def test_get_activity_day_history(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchall.return_value = [
        ("15.30", "Running", 1800, 300),
        ("16.30", "Swimming", 3600, 600),
    ]

    result = handler.get_activity_day_history(1, "01-01-2022")
    expected_result = json.dumps(
        [
            {
                "time": "15.30",
                "activity_name": "Running",
                "duration": 30,
                "calories_burned": 300,
            },
            {
                "time": "16.30",
                "activity_name": "Swimming",
                "duration": 60,
                "calories_burned": 600,
            },
        ],
        indent=4,
    )

    assert result == expected_result
    mock_cursor.execute.assert_called_once()


def test_get_activity_day_history_empty(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchall.return_value = []

    result = handler.get_activity_day_history(1, "01-01-2022")
    expected_result = json.dumps(
        [],
        indent=4,
    )

    assert result == expected_result
    mock_cursor.execute.assert_called_once()


def test_get_activity_list(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchall.return_value = [
        (101, "Running", 300),
        (102, "Swimming", 500),
    ]

    result = handler.get_activity_list()
    expected_result = json.dumps(
        [
            {
                "activity_id": 101,
                "name": "Running",
                "calories_burned_per_hour": 300,
            },
            {
                "activity_id": 102,
                "name": "Swimming",
                "calories_burned_per_hour": 500,
            },
        ],
        indent=4,
    )

    assert result == expected_result
    mock_cursor.execute.assert_called_once()


def test_get_activity_list_empty(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchall.return_value = []

    result = handler.get_activity_list()
    expected_result = json.dumps([], indent=4)

    assert result == expected_result
    mock_cursor.execute.assert_called_once()
