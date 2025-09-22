import pymysql
from contextlib import contextmanager

from base.config import config


@contextmanager
def get_connection():
    conn = pymysql.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
        port=config.DB_PORT,
        autocommit=True
    )
    try:
        yield conn
    finally:
        conn.close()
