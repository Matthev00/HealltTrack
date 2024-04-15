CREATE OR REPLACE VIEW food_info
AS 
SELECT f.food_id,
       mf.Meal_meal_id as meal_id,
      (mf.quantity * f.calories_per_100g / 100) as calories, 
      (mf.quantity * f.proteins_per_100g / 100) as proteins, 
      (mf.quantity * f.fats_per_100g / 100) as fats, 
      (mf.quantity * f.carbohydrates_per_100g / 100) as carbohydrates
FROM MEAL_FOOD mf
JOIN FOOD f ON mf.Food_food_id = f.food_id;

CREATE OR REPLACE PROCEDURE update_meal_data_proc(p_food_id IN NUMBER, p_meal_id IN NUMBER)
AS
  v_calories NUMBER(5, 1);
  v_proteins NUMBER(4, 1);
  v_fats NUMBER(4, 1);
  v_carbohydrates NUMBER(4, 1);
BEGIN
  BEGIN
      SELECT calories INTO v_calories FROM food_info WHERE food_id = p_food_id;
    EXCEPTION
      WHEN NO_DATA_FOUND THEN
      DBMS_OUTPUT.PUT_LINE('Food id: ' || p_food_id || ' Meal id: ' || p_meal_id);
  END;
      SELECT proteins INTO v_proteins FROM food_info WHERE food_id = p_food_id;
      SELECT fats INTO v_fats FROM food_info WHERE food_id = p_food_id;
      SELECT carbohydrates INTO v_carbohydrates FROM food_info WHERE food_id = p_food_id;
      

  UPDATE meal
  SET
    calories = calories + v_calories,
    proteins = proteins + v_proteins,
    fats = fats + v_fats,
    carbohydrates = carbohydrates + v_carbohydrates
  WHERE meal_id = p_meal_id;
END update_meal_data_proc;

CREATE OR REPLACE TRIGGER update_meal_data_tri
AFTER INSERT ON meal_food
FOR EACH ROW
DECLARE 
    pragma autonomous_transaction;
BEGIN
  update_meal_data_proc(:NEW.food_food_id, :NEW.meal_meal_id);
END;


SELECT * FROM food;
SELECT * FROM meal_food;
SELECT * FROM meal;

DESCRIBE meal;
DESCRIBE meal_food;

INSERT INTO meal_type (meal_type_id, name)
VALUES (1, 'Śniadanie');

INSERT INTO meal_type (meal_type_id, name)
VALUES (2, 'Obiad');

INSERT INTO "User" (user_id, name, surname, email, password, date_of_birth, gender, height)
VALUES (1, 'Jan', 'Kowalski', 'jan.kowalski@example.com', 'zaszyfrowane_haslo', TO_DATE('1990-01-01', 'YYYY-MM-DD'), 'M', 185.5);

INSERT INTO meal (meal_id, water_consumption, calories, proteins, fats, carbohydrates, meal_type_meal_type_id, is_drink)
VALUES (1, 250, 800, 25, 10, 100, 1, 0);

INSERT INTO meal_entry (meal_entry_id, user_user_id, date_time, meal_meal_id)
VALUES (1, 1, SYSDATE, 1); 

INSERT INTO food (food_id, name, calories_per_100g, proteins_per_100g, fats_per_100g, carbohydrates_per_100g, serving, is_drink)
VALUES (1, 'Jabłko', 52, 0.3, 0.2, 14, 100, 0);
INSERT INTO food (food_id, name, calories_per_100g, proteins_per_100g, fats_per_100g, carbohydrates_per_100g, serving, is_drink)
VALUES (2, 'Jajko', 52, 0.3, 0.2, 14, 100, 0);
INSERT INTO food (food_id, name, calories_per_100g, proteins_per_100g, fats_per_100g, carbohydrates_per_100g, serving, is_drink)
VALUES (3, 'gruszka', 52, 0.3, 0.2, 14, 100, 0);
INSERT INTO food (food_id, name, calories_per_100g, proteins_per_100g, fats_per_100g, carbohydrates_per_100g, serving, is_drink)
VALUES (4, 'gruszk', 52, 0.3, 0.2, 14, 100, 0);

INSERT INTO meal_food (quantity, meal_meal_id, food_food_id)
VALUES (150, 1, 4); 

