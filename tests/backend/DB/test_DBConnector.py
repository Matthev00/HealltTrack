import pytest
from unittest.mock import patch, MagicMock
import json
from backend.DB.DBConnector import DBConnector


@pytest.fixture(scope="module")
def wallet_credentials():
    with open("backend/DB/wallet_credentials.json") as f:
        return json.load(f)


def test_dbconnector_singleton(wallet_credentials):
    db1 = DBConnector(wallet_credentials)
    db2 = DBConnector(wallet_credentials)

    assert db1 is db2


@patch("oracledb.connect")
def test_dbconnector_connection(mock_connect, wallet_credentials):
    mock_connect.return_value = MagicMock()

    db = DBConnector(wallet_credentials)

    assert db.get_connection() is not None


@patch("oracledb.connect")
def test_dbconnector_read_credentials(mock_connect):
    mock_connect.return_value = MagicMock()

    wallet_credentials = {
        "user": "test",
        "password": "test",
        "dsn": "test",
        "cdir": "test",
        "wltloc": "test",
        "wltpsw": "test",
    }

    db = DBConnector(wallet_credentials)

    assert db.user == "test"
    assert db.password == "test"
    assert db.dsn == "test"
    assert db.config_dir == "test"
    assert db.wallet_location == "test"
    assert db.wallet_password == "test"


@patch("oracledb.connect")
def test_dbconnector_read_credentials_keyerror(mock_connect):
    mock_connect.return_value = MagicMock()

    wallet_credentials = {
        "user": "test",
        "password": "test",
        "dsn": "test",
        "cdir": "test",
        "wltloc": "test",
    }

    with pytest.raises(KeyError):
        DBConnector(wallet_credentials)
