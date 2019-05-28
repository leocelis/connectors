import os

import pymysql

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')


def get_mysql_conn():
    c = pymysql.connect(host=DB_HOST,
                        port=int(DB_PORT),
                        user=DB_USER,
                        passwd=DB_PASSWORD,
                        db=DB_NAME,
                        connect_timeout=300,
                        use_unicode=True,
                        autocommit=True)
    return c


def dictfecth(cursor):
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]
