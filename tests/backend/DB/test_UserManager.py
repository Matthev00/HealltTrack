import pytest
import sys
from unittest.mock import MagicMock, patch
import bcrypt
import oracledb
import json

sys.path.append("backend/DB")
from UserManager import UserManager


@pytest.fixture
def user_manager(db_connector):
    return UserManager(db_connector)


@pytest.fixture
def db_connector():
    with patch("DBConnector.DBConnector") as mock:
        conn = mock.return_value.get_connection.return_value
        cursor = conn.cursor.return_value
        cursor.__enter__.return_value = cursor
        yield mock


@pytest.fixture(autouse=True)
def mock_bcrypt():
    with patch("bcrypt.hashpw") as mock_hashpw:
        mock_hashpw.side_effect = lambda pwd, salt: pwd + b"salt"
        with patch("bcrypt.gensalt") as mock_gensalt:
            mock_gensalt.return_value = b"salt"
            with patch("bcrypt.checkpw") as mock_checkpw:
                mock_checkpw.side_effect = lambda pwd, hashed: pwd + b"salt" == hashed
                yield


def test_register_user_successful(user_manager, db_connector):
    cursor = db_connector.return_value.get_connection.return_value.cursor.return_value
    cursor.fetchone.return_value = [None]  # Simulate _find_user_next_id

    user_dict = {
        "name": "John",
        "surname": "Doe",
        "email": "john.doe@example.com",
        "password": "securepassword123",
        "date_of_birth": "01-01-1990",
        "gender": "M",
        "height": 180,
    }
    assert user_manager.register_user(user_dict) == True


def test_get_user_data(user_manager, db_connector):
    cursor = (
        db_connector.return_value.get_connection.return_value.cursor.return_value.__enter__.return_value
    )
    cursor.fetchone.return_value = (1, "John", "Doe", "01-01-1990", "M", 180)

    result = json.loads(user_manager.get_user_data("john.doe@example.com"))
    assert result["name"] == "John"
    assert result["surname"] == "Doe"
