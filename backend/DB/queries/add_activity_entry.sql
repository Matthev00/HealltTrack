INSERT INTO activity_entry (activity_entry_id, date_time, duration, calories_burned, user_user_id, activity_activity_id)
VALUES (:activity_entry_id, TO_DATE(:date_time, 'DD-MM-YYYY-HH24-MI'), :duration, :calories_burned, :user_id, :activity_id)
