SELECT f.name,
    f.calories_per_100g,
    f.proteins_per_100g,
    f.fats_per_100g,
    f.carbohydrates_per_100g,
    f.water,
    mf.quantity
FROM meal_food mf
INNER JOIN food f ON mf.food_food_id = f.food_id
WHERE mf.meal_meal_id = :meal_id