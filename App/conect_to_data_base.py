import oracledb

from wallet_credential import (
    user, password, dsn,
    cdir, wltloc, wltpsw
)


def connect_to_db():
    """
    Creates a connection to the Oracle database using the provided credentials.

    Returns:
        The established Oracle connection object, or None if connection fails.
    """

    try:
        connection = oracledb.connect(
            user=user,
            password=password,
            dsn=dsn,
            config_dir=cdir,
            wallet_location=wltloc,
            wallet_password=wltpsw
        )
        return connection

    except oracledb.Error as err:
        print(f"Error connecting to Oracle database: {err}")
        return None
