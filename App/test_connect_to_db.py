import oracledb

from wallet_credential import (
    user, password, dsn,
    cdir, wltloc, wltpsw
)

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
