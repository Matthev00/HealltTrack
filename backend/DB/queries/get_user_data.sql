SELECT user_id, name, surname, TO_CHAR(date_of_birth, 'DD-MM-YYYY'), gender , height
FROM "User" WHERE email = :email