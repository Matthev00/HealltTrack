SELECT mt.name AS meal_type_name,
    m.calories AS total_calories,
    m.proteins AS total_proteins,
    m.fats AS total_fats,
    m.carbohydrates AS total_carbs,
    m.meal_id
FROM meal_entry me
INNER JOIN meal m ON me.meal_meal_id = m.meal_id
INNER JOIN meal_type mt ON m.meal_type_meal_type_id = mt.meal_type_id
WHERE TRUNC(me.date_time) = TRUNC(TO_DATE(:query_date, 'DD-MM-YYYY'))
    AND me.user_user_id = :user_id