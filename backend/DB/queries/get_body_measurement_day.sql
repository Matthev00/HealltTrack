SELECT TO_CHAR(bme.date_time, 'DD-MM-YYYY-HH24') AS date_time, bme.weight
FROM body_measurement_entry bme
WHERE bme.user_user_id = :user_id
AND TRUNC(bme.date_time) = TRUNC(TO_DATE(:query_date, 'DD-MM-YYYY'))