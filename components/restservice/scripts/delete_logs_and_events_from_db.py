#!/usr/bin/env python

from datetime import datetime, timedelta
import psycopg2
from manager_rest.config import instance as conf

POSTGRESQL_DEFAULT_PORT = 5432
RESTSERVICE_CONFIG_PATH = '/opt/manager/cloudify-rest.conf'
DEFAULT_SAVE_PERIOD = 5
EVENTS_TABLE_NAME = 'events'
LOGS_TABLE_NAME = 'logs'


def _connect():
    # cloudify rest configuration is available as config.instance
    # config.instance.load_from_file(RESTSERVICE_CONFIG_PATH)
    try:
        conn = psycopg2.connect(
            database=conf.postgresql_db_name,
            user=conf.postgresql_username,
            password=conf.postgresql_password,
            host=conf.postgresql_host,
            port=str(POSTGRESQL_DEFAULT_PORT)
        )
        conn.autocommit = True
        return conn
    except psycopg2.DatabaseError as e:
        raise Exception('Error during connection to postgres: {0}'
                        .format(str(e)))


def delete_old_logs_and_events():
    _delete_rows_from_table(DEFAULT_SAVE_PERIOD, EVENTS_TABLE_NAME)
    _delete_rows_from_table(DEFAULT_SAVE_PERIOD, LOGS_TABLE_NAME)


def _delete_rows_from_table(save_period, table):
    print('save_period = ' + str(save_period))
    print('table_name = ' + str(table))
    last_date_to_keep = str(datetime.today() - timedelta(minutes=save_period))
    # last_date_to_keep = str(datetime.today() - timedelta(minutes=save_period))
    with _connect() as conn:
        with conn.cursor() as cur:
    # conn = _connect()
    # cur = conn.cursor()
            query = "DELETE FROM {0} WHERE reported_timestamp < '{1}'"\
                .format(table, last_date_to_keep)
            print('query = ' + query)
            cur.execute(query)
            conn.commit()
    # cur.close()
    # conn.close()

if __name__ == '__main__':
    conf.load_from_file(RESTSERVICE_CONFIG_PATH)
    delete_old_logs_and_events()
