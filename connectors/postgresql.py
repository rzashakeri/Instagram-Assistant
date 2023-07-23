import psycopg2

from configurations.settings import POSTGRESQL_HOST
from configurations.settings import POSTGRESQL_NAME
from configurations.settings import POSTGRESQL_PASSWORD
from configurations.settings import POSTGRESQL_PORT
from configurations.settings import POSTGRESQL_USERNAME
from constants import DUPLICATE_KEY

db_name = POSTGRESQL_NAME
db_user = POSTGRESQL_USERNAME
db_password = POSTGRESQL_PASSWORD
db_host = POSTGRESQL_HOST
db_port = POSTGRESQL_PORT


def execute_query(query):
    """function for execute query"""
    connection = psycopg2.connect(
        database=db_name, user=db_user, password=db_password, host=db_host, port=db_port
    )
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result


def create_user(user_id, first_name, last_name, username):
    """create user in database"""
    connection = psycopg2.connect(
        database=POSTGRESQL_NAME,
        host=POSTGRESQL_HOST,
        user=POSTGRESQL_USERNAME,
        password=POSTGRESQL_PASSWORD,
        port=POSTGRESQL_PORT,
    )
    cursor = connection.cursor()
    query = """
        INSERT INTO users (user_id, first_name, last_name, username)
        VALUES (%s, %s, %s, %s)
        """
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
        port=POSTGRESQL_PORT,
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
        port=POSTGRESQL_PORT,
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
            INSERT INTO requests (request_id, request_user_id, request_type, request_created_at)
            VALUES (DEFAULT, %s, %s, DEFAULT)
        """
    cursor.execute(query, (user_id, request_type))
    connection.commit()
    cursor.close()
    connection.close()


def get_daily_user_signup_count():
    """get daily user signup count"""
    connection = psycopg2.connect(
        database=POSTGRESQL_NAME,
        host=POSTGRESQL_HOST,
        user=POSTGRESQL_USERNAME,
        password=POSTGRESQL_PASSWORD,
        port=POSTGRESQL_PORT,
    )
    query = """
        SELECT
            COUNT(*) AS count
        FROM
            users
        WHERE
            created_at >= CURRENT_DATE - INTERVAL '1 day'
            AND created_at < CURRENT_DATE;
    """
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    connection.commit()
    cursor.close()
    connection.close()
    return result[0]


def get_user_request_insight():
    """get user request insight"""
    last_day_query = """
        SELECT
            'Last Day' AS interval,
            COUNT(*) AS insight_count
        FROM
            requests
        WHERE
            request_created_at >= CURRENT_DATE - INTERVAL '1 day'
            AND request_created_at < CURRENT_DATE
    """

    last_month_query = """
        SELECT
            'Last Month' AS interval,
            COUNT(*) AS insight_count
        FROM
            requests
        WHERE
            request_created_at >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '1 month'
            AND request_created_at < DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month'
    """

    last_year_query = """
        SELECT
            'Last Year' AS interval,
            COUNT(*) AS insight_count
        FROM
            requests
        WHERE
            request_created_at >= DATE_TRUNC('year', CURRENT_DATE) - INTERVAL '1 year'
            AND request_created_at < DATE_TRUNC('year', CURRENT_DATE) + INTERVAL '1 year'
    """

    last_day_count = execute_query(last_day_query)
    last_month_count = execute_query(last_month_query)
    last_year_count = execute_query(last_year_query)

    return last_day_count, last_month_count, last_year_count


def get_user_signup_insight():
    """get user signup insight"""
    last_day_query = """
        SELECT
            'Last Day' AS interval,
            COUNT(*) AS insight_count
        FROM
            users
        WHERE
            created_at >= CURRENT_DATE - INTERVAL '1 day'
            AND created_at < CURRENT_DATE
    """

    last_month_query = """
        SELECT
            'Last Month' AS interval,
            COUNT(*) AS insight_count
        FROM
            users
        WHERE
            created_at >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '1 month'
            AND created_at < DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month'
    """

    last_year_query = """
        SELECT
            'Last Year' AS interval,
            COUNT(*) AS insight_count
        FROM
            users
        WHERE
            created_at >= DATE_TRUNC('year', CURRENT_DATE) - INTERVAL '1 year'
            AND created_at < DATE_TRUNC('year', CURRENT_DATE) + INTERVAL '1 year'
    """

    last_day_count = execute_query(last_day_query)
    last_month_count = execute_query(last_month_query)
    last_year_count = execute_query(last_year_query)

    return last_day_count, last_month_count, last_year_count


def get_request_count():
    """Get Request Count"""
    query = """
    SELECT
    COUNT(*)
    FROM
    requests
    """
    result = execute_query(query)
    return result
