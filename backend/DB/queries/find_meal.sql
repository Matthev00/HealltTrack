SELECT meal_meal_id
FROM meal_entry
JOIN meal ON meal_entry.meal_meal_id = meal.meal_id
JOIN meal_type ON meal.meal_type_meal_type_id = meal_type.meal_type_id
WHERE TRUNC(meal_entry.date_time) = TRUNC(TO_DATE(:date_time, 'DD-MM-YYYY'))
    AND meal_type.name = :meal_type
    AND meal_entry.user_user_id = :user_id