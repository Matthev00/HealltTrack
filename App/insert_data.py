import oracledb
# from conect_to_data_base import connect_to_db

from wallet_credential import (
    user, password, dsn,
    cdir, wltloc, wltpsw
)


def insert_data():
    data_to_add = """
    INSERT INTO Customers
    (customer_id, first_name, last_name, email, phone_number)
    VALUES (6, 'MI', 'Doe', 'johndoe@email.com', '123456789')"""

    with oracledb.connect(
        user=user,
        password=password,
        dsn=dsn,
        config_dir=cdir,
        wallet_location=wltloc,
        wallet_password=wltpsw
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(data_to_add)
            connection.commit()


def get_data():
    with oracledb.connect(
        user=user,
        password=password,
        dsn=dsn,
        config_dir=cdir,
        wallet_location=wltloc,
        wallet_password=wltpsw
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM customers")
            rows = cursor.fetchall()
            return rows


def display_data():
    with oracledb.connect(
        user=user,
        password=password,
        dsn=dsn,
        config_dir=cdir,
        wallet_location=wltloc,
        wallet_password=wltpsw
    ) as connection:
        with connection.cursor() as cursor:
            # cursor.execute("SELECT 'Hello, World!' FROM DUAL")
            # print(cursor.fetchone()[0])
            cursor.execute("SELECT * FROM customers")
            rows = cursor.fetchall()
            for row in rows:
                print(row)


def main():
    insert_data()
    display_data()


if __name__ == '__main__':
    main()
