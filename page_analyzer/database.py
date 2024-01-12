import os
import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def execute_query(query, parameters=None, fetchall=False):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=DictCursor) as curs:
        curs.execute(query, parameters)
        if fetchall:
            results = curs.fetchall()
        else:
            results = curs.fetchone()
    conn.commit()
    conn.close()
    return results


def add_url_record(url_fields_dct):
    url_insert_query = 'INSERT INTO urls (name, created_at) VALUES (%(url)s, %(created_at)s)'
    execute_query(url_insert_query, url_fields_dct)


def add_check_record(check_fields_dct):
    check_insert_query = 'INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at) \
                          VALUES (%(url_id)s, %(status_code)s, %(h1)s, %(title)s, %(description)s, %(created_at)s)'
    execute_query(check_insert_query, check_fields_dct)


def get_url_by_name(name):
    url_select_query = 'SELECT * FROM urls WHERE name = %s'
    return execute_query(url_select_query, [name])


def get_url_by_id(id):
    url_select_query = 'SELECT * FROM urls WHERE id = %s'
    return execute_query(url_select_query, [id])


def get_all_url_records():
    url_select_query = 'SELECT * FROM urls'
    return execute_query(url_select_query, fetchall=True)


def get_checks_url_by_id(id):
    check_select_query = 'SELECT * FROM url_checks WHERE url_id = %s'
    return execute_query(check_select_query, [id], fetchall=True)


def get_last_check_url():
    check_select_query = 'SELECT urls.id, urls.name, url_checks.status_code, url_checks.created_at \
                          FROM urls \
                          LEFT JOIN url_checks ON urls.id = url_checks.url_id \
                          AND url_checks.id = (SELECT MAX(url_checks.id) FROM url_checks WHERE url_id = urls.id) \
                          ORDER BY url_checks.created_at DESC'
    return execute_query(check_select_query, fetchall=True)
