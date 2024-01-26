import os
import psycopg2
from psycopg2.extras import DictCursor
from psycopg2 import sql
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def add_url_record(url_fields_dct):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as curs:
            url_insert_query = 'INSERT INTO urls \
                                (name, created_at) \
                                VALUES (%(url)s, %(created_at)s) \
                                RETURNING id'
            curs.execute(url_insert_query, url_fields_dct)
            new_url_id = curs.fetchone()[0]
    return new_url_id


def add_check_record(url_fields_dct):
    with psycopg2.connect(DATABASE_URL) as conn:
        insert_query = sql.SQL("""
            INSERT INTO url_checks
            (url_id, status_code, h1, title, description, created_at)
            VALUES
            (%(url_id)s, %(status_code)s, %(h1)s, %(title)s, %(description)s, \
            %(created_at)s)
        """)
        with conn.cursor() as curs:
            curs.execute(insert_query, url_fields_dct)


def get_url_by_name(name):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            url_select_query = 'SELECT * FROM urls WHERE name = (%s)'
            curs.execute(url_select_query, [name])
            url_dct = curs.fetchone()
    return url_dct


def get_url_by_id(id):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            url_select_query = 'SELECT * FROM urls WHERE id = (%s)'
            curs.execute(url_select_query, [id])
            url_dct = curs.fetchone()
    return url_dct


def get_checks_url_by_id(id):
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            check_select_query = 'SELECT * FROM url_checks WHERE url_id = (%s)'
            curs.execute(check_select_query, [id])
            check_dct = curs.fetchall()
    return check_dct


def urls_with_last_check_info():
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor(cursor_factory=DictCursor) as curs:
            check_select_query = 'SELECT\
                                  urls.id,\
                                  urls.name,\
                                  url_checks.status_code,\
                                  url_checks.created_at\
                             FROM urls\
                             LEFT JOIN url_checks ON urls.id = url_id\
                             AND url_checks.id = (SELECT MAX(url_checks.id)\
                                                  FROM url_checks\
                                                  WHERE url_id = urls.id)\
                             ORDER BY url_checks.created_at DESC'
            curs.execute(check_select_query)
            check_dct = curs.fetchall()
    return check_dct
