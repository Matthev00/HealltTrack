SELECT
    SUM(m.calories) AS total_calories,
    SUM(m.proteins) AS total_proteins,
    SUM(m.fats) AS total_fats,
    SUM(m.carbohydrates) AS total_carbs,
    SUM(m.water_consumption) AS total_water
FROM meal_entry me
INNER JOIN meal m ON me.meal_meal_id = m.meal_id
WHERE TRUNC(me.date_time) = TRUNC(TO_DATE(:query_date, 'DD-MM-YYYY'))
    AND me.user_user_id = :user_id