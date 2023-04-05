import psycopg2

from configurations.settings import POSTGRESQL_HOST, POSTGRESQL_NAME, POSTGRESQL_USERNAME, POSTGRESQL_PASSWORD, POSTGRESQL_PORT


def create_user(user_id, first_name, last_name, username):
    """create user in database"""
    connection = psycopg2.connect(
        database=POSTGRESQL_NAME,
        host=POSTGRESQL_HOST,
        user=POSTGRESQL_USERNAME,
        password=POSTGRESQL_PASSWORD,
        port=POSTGRESQL_PORT
    )
    cursor = connection.cursor()
    query = ("""
        INSERT INTO users (user_id, first_name, last_name, username) 
        VALUES (%s, %s, %s, %s)
        """)
    cursor.execute(query, (user_id, first_name, last_name, username))
    connection.commit()
    cursor.close()
    connection.close()
