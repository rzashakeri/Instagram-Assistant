import psycopg2
from configurations.settings import POSTGRESQL_HOST, POSTGRESQL_NAME, POSTGRESQL_USERNAME, POSTGRESQL_PASSWORD, POSTGRESQL_PORT
from constants import DUPLICATE_KEY


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
    try:
        cursor.execute(query, (user_id, first_name, last_name, username))
    except psycopg2.Error as error:
        if DUPLICATE_KEY in str(error):
            pass
    connection.commit()
    cursor.close()
    connection.close()


def get_user_count():
    """get user count from the database"""
    connection = psycopg2.connect(
        database=POSTGRESQL_NAME,
        host=POSTGRESQL_HOST,
        user=POSTGRESQL_USERNAME,
        password=POSTGRESQL_PASSWORD,
        port=POSTGRESQL_PORT
    )
    query = """
    SELECT 
    COUNT(*) 
    FROM 
    users
    """
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return result[0]


def get_user_id():
    """get user ids from the database"""
    connection = psycopg2.connect(
        database=POSTGRESQL_NAME,
        host=POSTGRESQL_HOST,
        user=POSTGRESQL_USERNAME,
        password=POSTGRESQL_PASSWORD,
        port=POSTGRESQL_PORT
    )
    query = """
    SELECT user_id
    FROM users
    """
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.commit()
    cursor.close()
    connection.close()
    return result


def create_request(user_id, request_type):
    """create request in database This function says what
    the user has been requesting from the robot"""
    connection = psycopg2.connect(
        database=POSTGRESQL_NAME,
        host=POSTGRESQL_HOST,
        user=POSTGRESQL_USERNAME,
        password=POSTGRESQL_PASSWORD,
        port=POSTGRESQL_PORT,
    )
    cursor = connection.cursor()
    query = """
            INSERT INTO requests (request_id, user_id, request_type)
            VALUES (DEFAULT, %s, %s)
        """
    cursor.execute(query, (user_id, request_type))
    connection.commit()
    cursor.close()
    connection.close()
