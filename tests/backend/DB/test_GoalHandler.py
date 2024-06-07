import pytest
from unittest.mock import patch, MagicMock
import sys
import json
import oracledb

sys.path.append("backend/DB")
from GoalHandler import GoalHandler as Handler  # noqa5501
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


def test_get_goal_types_list_success(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchall.return_value = [("Weight Loss",), ("Muscle Gain",)]

    result = handler.get_goal_types_list()
    expected_result = json.dumps(["Weight Loss", "Muscle Gain"], indent=4)

    assert result == expected_result
    mock_cursor.execute.assert_called_once_with("SELECT name FROM goal_type")


def test_get_goal_types_list_empty(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchall.return_value = []

    result = handler.get_goal_types_list()
    expected_result = json.dumps([], indent=4)

    assert result == expected_result
    mock_cursor.execute.assert_called_once_with("SELECT name FROM goal_type")


def test_get_user_goal_found(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchone.return_value = (
        "Weight Loss",
        70,
        "01-01-2022",
        "31-12-2022",
    )

    goal_dict = {"user_id": 1, "date": "15-06-2022"}
    result = handler.get_user_goal(goal_dict)
    expected_result = json.dumps(
        {
            "target_weight": 70,
        },
        indent=4,
    )

    assert result == expected_result
    mock_cursor.execute.assert_called_once()


def test_get_user_goal_not_found(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchone.return_value = None

    goal_dict = {"user_id": 1, "date": "15-06-2022"}
    result = handler.get_user_goal(goal_dict)
    expected_result = json.dumps(
        {
            "target_weight": "No goal set",
        },
        indent=4,
    )

    assert result == expected_result
    mock_cursor.execute.assert_called_once()


def test_set_user_goal_success(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchone.return_value = [1]

    goal_dict = {
        "user_id": 1,
        "goal_type": 1,
        "target_weight": 70,
        "start_date": "01-01-2023",
        "end_date": "01-01-2024",
    }

    handler.set_user_goal(goal_dict)
    mock_cursor.execute.call_count == 2


def test_set_user_goal_db_error(handler, mock_db_connector, caplog):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchone.return_value = [1]
    mock_cursor.execute.side_effect = oracledb.DatabaseError("Database error")

    goal_dict = {
        "user_id": 1,
        "goal_type": 1,
        "target_weight": 70,
        "start_date": "01-01-2023",
        "end_date": "01-01-2024",
    }

    with pytest.raises(oracledb.DatabaseError):
        handler.set_user_goal(goal_dict)
