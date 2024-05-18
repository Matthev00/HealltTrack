INSERT INTO activity_entry (activity_entry_id, date_time, duration, user_user_id, activity_activity_id)
VALUES (:activity_entry_id, TO_DATE(:date_time, 'DD-MM-YYYY-HH24-MI'), :duration, :user_id, :activity_id)
