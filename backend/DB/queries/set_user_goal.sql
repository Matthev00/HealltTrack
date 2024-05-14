INSERT INTO goal (goal_id, target_weight, start_date, end_date, user_user_id, goal_type_goal_type_id)
VALUES (:goal_id, :target_weight, TO_DATE(:start_date, 'DD-MM-YYYY'), TO_DATE(:end_date, 'DD-MM-YYYY'), :user_id, :goal_type)
