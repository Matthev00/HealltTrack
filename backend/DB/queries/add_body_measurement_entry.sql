INSERT INTO body_measurement_entry (body_measurement_entry_id, date_time, weight, user_user_id)
VALUES (:bm_id, TO_DATE(:date_time, 'DD-MM-YYYY-HH24-MI-SS'), :weight, :user_id)