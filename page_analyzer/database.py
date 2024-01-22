import os
import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def add_url_record(url_fields_dct):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as curs:
        url_insert_query = 'INSERT INTO urls \
                               (name, created_at) \
                               VALUES (%(url)s, %(created_at)s) \
                               RETURNING id'
        curs.execute(url_insert_query, url_fields_dct)
    conn.commit()
    conn.close()


def add_check_record(url_fields_dct):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as curs:
        check_insert_query = 'INSERT INTO url_checks\
                                  (url_id,\
                                  status_code,\
                                  h1, title,\
                                  description,\
                                  created_at)\
                             VALUES\
                                 (%(url_id)s,\
                                 %(status_code)s,\
                                 %(h1)s, %(title)s,\
                                 %(description)s,\
                                 %(created_at)s)'
        curs.execute(check_insert_query, url_fields_dct)
    conn.commit()
    conn.close()


def get_url_by_name(name):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=DictCursor) as curs:
        url_select_query = 'SELECT * FROM urls\
                            where name = (%s)'
        curs.execute(url_select_query, [name])
        url_dct = curs.fetchone()
    conn.close()
    return url_dct


def get_url_by_id(id):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=DictCursor) as curs:
        url_select_query = 'SELECT * FROM urls\
                            where id = (%s)'
        curs.execute(url_select_query, [id])
        url_dct = curs.fetchone()
    conn.close()
    return url_dct


def get_all_url_records():
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=DictCursor) as curs:
        url_select_query = 'SELECT * FROM urls'
        curs.execute(url_select_query)
        all_urls_dct = curs.fetchall()
    conn.close()
    return all_urls_dct


def get_checks_url_by_id(id):
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor(cursor_factory=DictCursor) as curs:
        check_select_query = 'SELECT * FROM url_checks\
                              where url_id = (%s)'
        curs.execute(check_select_query, [id])
        check_dct = curs.fetchall()
    conn.close()
    return check_dct


def urls_with_last_check_info():
    conn = psycopg2.connect(DATABASE_URL)
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
    conn.close()
    return check_dct
