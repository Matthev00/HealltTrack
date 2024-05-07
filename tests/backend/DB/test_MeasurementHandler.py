import pytest
from unittest.mock import patch, MagicMock
import sys
import json

sys.path.append("backend/DB")
from MeasurementHandler import MeasurementHandler as Handler
from DBConnector import DBConnector


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
    mock_db_connector.get_connection.return_value.cursor.return_value.__enter__.return_value = (
        mock_cursor
    )
    return mock_cursor


def test_add_body_measurement_entry_success(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchone.return_value = [10]

    valid_entry_dict = {
        "user_id": 1,
        "date": "01-01-2022-12",
        "weight": 70
    }

    handler.add_body_measurement_entry(valid_entry_dict)

    mock_cursor.execute.call_count == 2


def test_get_body_measurement_history(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchall.return_value = [("01-01-2022-12", 70), ("02-01-2022-12", 72)]

    user_id = 1
    result = handler.get_body_measurement_history(user_id)
    expected_result = json.dumps(
        [
            {"date_time": "01-01-2022-12", "weight": 70},
            {"date_time": "02-01-2022-12", "weight": 72},
        ],
        indent=4,
    )

    assert result == expected_result
    mock_cursor.execute.assert_called_once_with(
        """
        SELECT TO_CHAR(bme.date_time, 'DD-MM-YYYY-HH24') AS date_time, bme.weight
        FROM body_measurement_entry bme
        WHERE bme.user_user_id = :user_id
        ORDER BY bme.date_time
        """,
        {"user_id": user_id},
    )
