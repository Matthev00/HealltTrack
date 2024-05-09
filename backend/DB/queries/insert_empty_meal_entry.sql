INSERT INTO meal_entry (meal_entry_id, user_user_id, meal_meal_id, date_time)
VALUES (:meal_entry_id, :user_id, :meal_id, TO_DATE(:date_time, 'DD-MM-YYYY'))