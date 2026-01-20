import psycopg2
from config import host, port, db_name, user, password

try:
    connection = psycopg2.connect(
        host=host,
        port=port,
        database=db_name,
        user=user,
        password=password
    )

    with connection.cursor() as cursor:
        cursor.execute(
            "select version();"
        )
        print(f"server version: {cursor.fetchone()}")

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)
finally:
    if connection:
        connection.close()
        print("[INFO] PostgreSQL connection closed")