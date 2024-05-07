import json
import pytest
from unittest.mock import patch, MagicMock
import sys

sys.path.append("backend/DB")
from MealHandler import MealHandler as Handler
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
def test_get_food_list(data, expected, mock_db_connector, handler):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchall.return_value = data

    result = handler.get_food_list()

    assert result == expected
    mock_db_connector.get_connection.assert_called_once()


def test_get_food_list_db_error(mock_db_connector, handler):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchall.side_effect = Exception("DB error")

    with pytest.raises(Exception, match="DB error"):
        handler.get_food_list()

    mock_db_connector.get_connection.assert_called_once()


def test_find_meal_found(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchone.return_value = [1]

    result = handler._find_meal("01-01-2022", 2, 10)
    assert result == 1


def test_find_meal_not_found(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchone.return_value = None

    result = handler._find_meal("01-01-2022", 2, 10)
    assert result is None


def test_insert_empty_meal(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    handler._find_next_id = MagicMock(return_value=1)

    result = handler._insert_empty_meal(2)
    assert result == 1
    mock_cursor.execute.assert_called_once()


def test_find_next_id_existing(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchone.return_value = [10]

    result = handler._find_next_id("meal")
    assert result == 11


def test_find_next_id_none(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchone.return_value = [None]

    result = handler._find_next_id("meal")
    assert result == 1


def test_insert_empty_meal_entry(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    handler._find_next_id = MagicMock(return_value=1)

    handler._insert_empty_meal_entry(1, 10, "01-01-2022")
    mock_cursor.execute.assert_called_once()


def test_insert_meal_food(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)

    handler._insert_meal_food(1, 100, 150)
    mock_cursor.execute.assert_called_once()


def test_get_foods_for_meal_with_data(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchall.return_value = [("Apple", 52, 0.3, 0.2, 14, 85, 100)]
    foods = handler._get_foods_for_meal(1)

    assert len(foods) == 1
    assert foods[0]["name"] == "Apple"
    assert foods[0]["calories_per_100g"] == 52


def test_get_foods_for_meal_no_data(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchall.return_value = []
    foods = handler._get_foods_for_meal(1)
    assert foods == []


def test_get_foods_for_meal_with_multiple_foods(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchall.return_value = [
        ("Apple", 52, 0.3, 0.2, 14, 85, 100),
        ("Banana", 89, 1.1, 0.3, 23, 75, 150),
        ("Chicken Breast", 165, 31, 3.6, 0, 65, 200),
    ]
    foods = handler._get_foods_for_meal(1)

    assert len(foods) == 3
    assert foods[0]["name"] == "Apple" and foods[0]["calories_per_100g"] == 52
    assert foods[1]["name"] == "Banana" and foods[1]["calories_per_100g"] == 89
    assert foods[2]["name"] == "Chicken Breast" and foods[2]["calories_per_100g"] == 165


def test_get_day_history_with_data(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchall.return_value = [
        ("Breakfast", 200, 10, 20, 30, 1),
        ("Lunch", 500, 25, 50, 75, 2),
    ]
    handler._get_foods_for_meal = MagicMock(return_value=[{"name": "Apple"}])

    day_dict = {"date": "01-01-2022", "user_id": 1}
    result = handler.get_day_history(day_dict)
    result_data = json.loads(result)

    assert result_data["Breakfast"]["kcal"] == 200
    assert result_data["Lunch"]["kcal"] == 500
    assert result_data["Breakfast"]["foods"] == [{"name": "Apple"}]


def test_get_day_history_no_data(handler, mock_db_connector):
    handler._get_foods_for_meal = MagicMock(return_value=[])

    day_dict = {"date": "01-01-2022", "user_id": 1}
    result = handler.get_day_history(day_dict)
    result_data = json.loads(result)

    assert all(meal_info["kcal"] == 0 for meal_info in result_data.values())
    assert all(meal_info["foods"] == [] for meal_info in result_data.values())


def test_get_day_history_full_day(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchall.return_value = [
        ("Breakfast", 300, 15, 5, 45, 1),
        ("Second breakfast", 150, 8, 3, 20, 2),
        ("Lunch", 500, 30, 20, 60, 3),
        ("Afternoon snack", 200, 10, 5, 25, 4),
        ("Dinner", 400, 20, 10, 40, 5),
    ]
    handler._get_foods_for_meal = MagicMock(
        return_value=[{"name": "Food Item", "calories_per_100g": 100}]
    )

    day_dict = {"date": "01-01-2022", "user_id": 1}
    result = handler.get_day_history(day_dict)
    result_data = json.loads(result)

    assert result_data["Breakfast"]["kcal"] == 300
    assert result_data["Lunch"]["kcal"] == 500
    assert result_data["Dinner"]["kcal"] == 400
    assert all(
        meal["foods"] == [{"name": "Food Item", "calories_per_100g": 100}]
        for meal in result_data.values()
    )


def test_find_food_id_found(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchone.return_value = [100]
    result = handler._find_food_id("Apple")
    assert result == 100


def test_find_food_id_not_found(handler, mock_db_connector):
    mock_cursor = setup_mock_cursor(mock_db_connector)
    mock_cursor.fetchone.return_value = None
    result = handler._find_food_id("Nonexistent Food")
    assert result is None


def test_delete_food_from_meal_successful(handler, mock_db_connector):
    handler._find_meal = MagicMock(return_value=1)
    handler._find_food_id = MagicMock(return_value=100)

    meal_data = {
        "date_time": "01-01-2022 12:00",
        "food_name": "Apple",
        "meal_type": 1,
        "user_id": 1,
    }

    result = handler.delete_food_from_meal(meal_data)

    assert result is True
    handler._find_meal.assert_called_once_with("01-01-2022 12:00", 1, 1)
    handler._find_food_id.assert_called_once_with("Apple")


def test_delete_food_from_meal_no_meal_found(handler, mock_db_connector):
    handler._find_meal = MagicMock(return_value=None)
    handler._find_food_id = MagicMock(return_value=100)

    meal_data = {
        "date_time": "01-01-2022 12:00",
        "food_name": "Apple",
        "meal_type": 1,
        "user_id": 1,
    }

    result = handler.delete_food_from_meal(meal_data)

    assert result is False
    handler._find_meal.assert_called_once()
    handler._find_food_id.assert_called_once()


def test_delete_food_from_meal_no_food_found(handler, mock_db_connector):
    handler._find_meal = MagicMock(return_value=1)
    handler._find_food_id = MagicMock(return_value=None)

    meal_data = {
        "date_time": "01-01-2022 12:00",
        "food_name": "Apple",
        "meal_type": 1,
        "user_id": 1,
    }

    result = handler.delete_food_from_meal(meal_data)

    assert result is False
    handler._find_meal.assert_called_once()
    handler._find_food_id.assert_called_once_with("Apple")
