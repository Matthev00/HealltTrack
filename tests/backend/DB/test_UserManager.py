import pytest
import sys
from unittest.mock import MagicMock, patch
import json
import bcrypt
import oracledb

sys.path.append("backend/DB")
from UserManager import UserManager as Handler  # noqa 5501
from DBConnector import DBConnector  # noqa 5501


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
    mock_db_connector.get_connection.return_value.cursor.return_value.__enter__.return_value = (  # noqa 5501
        mock_cursor
    )
    return mock_cursor


@pytest.fixture(scope="module")
def mock_bcrypt():
    with patch("bcrypt.hashpw") as mock_hashpw:
        mock_hashpw.side_effect = lambda pwd, salt: pwd + b"salt"
        with patch("bcrypt.gensalt") as mock_gensalt:
            mock_gensalt.return_value = b"salt"
            with patch("bcrypt.checkpw") as mock_checkpw:
                mock_checkpw.side_effect = (
                    lambda pwd, hashed: pwd + b"salt" == hashed
                )  #
                yield


def test_register_user_successful(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchone.return_value = [None]

    user_dict = {
        "name": "John",
        "surname": "Doe",
        "email": "john.doe@example.com",
        "password": "securepassword123",
        "date_of_birth": "01-01-1990",
        "gender": "M",
        "height": 180,
    }
    result = handler.register_user(user_dict)
    assert result is True


def test_register_user_email_exists(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.execute.side_effect = [
        None,
        oracledb.IntegrityError(),
    ]

    user_dict = {
        "name": "Jane",
        "surname": "Doe",
        "email": "john.doe@example.com",
        "password": "anotherpassword",
        "date_of_birth": "01-01-1991",
        "gender": "F",
        "height": 165,
    }
    result = handler.register_user(user_dict)
    assert result is False


def test_login_user_successful(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    password = "securepassword123"
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    hashed_password_hex = hashed_password.hex()

    mock_cursor.fetchone.side_effect = [
        [hashed_password_hex],
        (1, "John", "Doe", "01-01-1990", "M", 180),
    ]

    login_dict = {
        "email": "john.doe@example.com",
        "password": "securepassword123",
    }
    result = handler.login_user(login_dict)

    assert json.loads(result) == {
        "user_id": 1,
        "name": "John",
        "surname": "Doe",
        "date_of_birth": "01-01-1990",
        "gender": "M",
        "height": 180,
    }


def test_login_user_invalid_password(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    password = "securepassword123"
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    hashed_password_hex = hashed_password.hex()
    mock_cursor.fetchone.side_effect = [[hashed_password_hex]]

    login_dict = {"email": "unknown@example.com", "password": "password"}
    result = handler.login_user(login_dict)
    assert result is False


def test_login_user_invalid_email(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchone.return_value = []

    login_dict = {"email": "unknown@example.com", "password": "password"}
    result = handler.login_user(login_dict)
    assert result is False


def test_check_password_correctness(handler):
    stored_pass = bcrypt.hashpw(b"validpassword", bcrypt.gensalt())
    provided_pass = "validpassword"
    result = handler.check_password(stored_pass, provided_pass)
    assert result is True

    provided_pass = "invalidpassword"
    result = handler.check_password(stored_pass, provided_pass)
    assert result is False


def test_get_user_data(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchone.return_value = (
        1,
        "John",
        "Doe",
        "01-01-1990",
        "M",
        180,
    )

    result = handler.get_user_data("john.doe@example.com")

    expected_result = json.dumps(
        {
            "user_id": 1,
            "name": "John",
            "surname": "Doe",
            "date_of_birth": "01-01-1990",
            "gender": "M",
            "height": 180,
        },
        indent=4,
    )

    assert result == expected_result
