import os
from io import StringIO
from time import time
from functools import wraps

import pandas as pd
import yaml
import psycopg2
from psycopg2 import extras

from python.logging_module import get_logger

logger = get_logger("utils logger")
CURRENT_DIR = ""


def get_yaml_conf(settings_filename):
    with open(settings_filename, "r") as file:
        settings = yaml.load(file, Loader=yaml.FullLoader)
    return settings


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print("func: {} took: {} sec".format(f.__name__, round(te - ts)))
        return result

    return wrap


class Configuration(object):
    """
    Класс - Синглтон
    Он нужен для хранения всех настроек и доступа к ним из любой части пакета

    Доступ к элементам осуществляется через []
    Источники параметров - конфигурационный файл и аргументы командной строки. Они передаются словарями
    Этому контейнеру можно задавать результаты и напрямую, через []
    """

    _instance = None
    _d = {}

    def __new__(class_, *args, **kwargs):
        """Реализация синглтона"""
        if not isinstance(class_._instance, class_):
            Configuration._instance = object.__new__(Configuration, *args, **kwargs)
            settings = get_yaml_conf(os.environ['CONFIG_PATH'])
            Configuration._instance.store_dict(settings)
            if "POSTGRES" in settings.keys():
                if "CREDENTIALS_PATH" in settings["POSTGRES"]:
                    account_settings = get_yaml_conf(CURRENT_DIR + settings["POSTGRES"]["CREDENTIALS_PATH"])
                    Configuration._instance._d["POSTGRES"].update(account_settings)
        return class_._instance

    def store_dict(self, d):
        """
        Сохранение параметров из словаря
        Args:
            d: dict
        """
        for key, value in d.items():
            # Если значение уже есть, а новое None, то None записан не будет
            if not (key in self._d and value is None):
                self._d[key] = value

    def __setitem__(self, key, value):
        self._d[key] = value

    def __getitem__(self, key):
        return self._d[key]

    def __contains__(self, key):
        return key in self._d


def get_postgres_connection():
    """Return POSTGRES connection from settings.yml credentials"""
    postgres_conf = Configuration()["POSTGRES"]

    hostname = postgres_conf['host']
    login = postgres_conf['login']
    database = postgres_conf['database']
    password = postgres_conf['password']

    logger.info(
        "Postgres connection: HOSTNAME {}, LOGIN {}, DATABASE {}".format(hostname, login, database))

    try:
        conn = psycopg2.connect(
            dbname=database,
            user=login,
            host=hostname,
            password=password,
        )
    except Exception as e:
        logger.exception("Something gone wrong", e)
        raise
    return conn


@timing
def load_from_postgres_filename(filename, conn):
    with open(filename, "r") as file:
        sql = file.read()
    ans = pd.read_sql(sql, conn)
    return ans


@timing
def load_from_postgres_query(query):
    conn = get_postgres_connection()
    try:
        ans = pd.read_sql(query, conn)
    except pd.io.sql.DatabaseError as e:
         logger.exception(e)
    return ans


@timing
def load_to_postgres(conn, df, table):
    logger.info("start copy dataframe to Postgres {}".format(table))
    buffer = StringIO()
    df.to_csv(buffer, header=False)
    buffer.seek(0)

    cur = conn.cursor()
    try:
        df_columns = list(df)
        # create (col1,col2,...)
        columns = ",".join(df_columns)

        # create VALUES('%s', '%s",...) one '%s' per column
        values = "VALUES({})".format(",".join(["%s" for _ in df_columns]))

        # create INSERT INTO table (columns) VALUES('%s',...)
        insert_stmt = "INSERT INTO {} ({}) {}".format(table, columns, values)

        cur = conn.cursor()
        psycopg2.extras.execute_batch(cur, insert_stmt, df.values)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as e:
        logger.exception("Something gone wrong", e)
        conn.rollback()
        cur.close()
    logger.info("finish copy dataframe to Postgres {}".format(table))
    cur.close()


def is_table_exists(tablename: str):
    """expected tablename with structure: schema.table"""
    conn = get_postgres_connection()
    query = f"""
        SELECT * FROM {tablename} LIMIT 1;
    """
    try:
        pd.read_sql(query, conn)
    except pd.io.sql.DatabaseError as e:
         logger.exception(e)
         return False
    finally:
        conn.close()
    return True