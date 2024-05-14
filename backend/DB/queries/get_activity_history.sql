SELECT TO_CHAR(ae.date_time, 'DD-MM-YYYY-HH24-MI') AS date_time, a.name AS activity_name, ae.duration, ae.calories_burned
FROM activity_entry ae
JOIN activity a ON ae.activity_activity_id = a.activity_id
WHERE ae.user_user_id = :user_id
ORDER BY ae.date_time