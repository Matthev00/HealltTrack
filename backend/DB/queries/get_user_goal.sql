SELECT gt.name, target_weight, TO_CHAR(start_date, 'DD-MM-YYYY'), TO_CHAR(end_date, 'DD-MM-YYYY')
FROM goal g
JOIN goal_type gt ON g.goal_type_goal_type_id = gt.goal_type_id
WHERE user_user_id = :user_id
    AND start_date <= TO_DATE(:date_time, 'DD-MM-YYYY')
    AND end_date >= TO_DATE(:date_time, 'DD-MM-YYYY')
ORDER BY end_date ASC
FETCH FIRST 1 ROW ONLY