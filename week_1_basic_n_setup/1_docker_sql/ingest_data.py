#!/usr/bin/env python
# coding: utf-8
import os
import argparse

import pandas as pd
from sqlalchemy import create_engine
from time import time


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    zones_table_name = params.zones_table_name
    url_data = params.url_data
    url_zones = params.url_zones

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    load_data(engine, url_data, table_name)
    load_zones(engine, url_zones, zones_table_name)


def load_data(engine, url, table_name):
    os.system(f"wget {url} -O {table_name}.parquet")

    df = pd.read_parquet(f'{table_name}.parquet', engine='pyarrow')
    t_start = time()
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='append', chunksize=100000)
    t_end = time()
    print('Data ingested, took %.3f seconds' % (t_end - t_start))


def load_zones(engine, url, table_name):
    os.system(f"wget {url} -O {table_name}.csv")

    df = pd.read_csv(f'{table_name}.csv')
    t_start = time()
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='append', chunksize=100000)
    t_end = time()
    print('Zones data ingested, took %.3f seconds' % (t_end - t_start))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='destination table name')
    parser.add_argument('--zones_table_name', help='destination table name for table with zones')
    parser.add_argument('--url_data', help='url of the parquet file with taxi data')
    parser.add_argument('--url_zones', help='url of the parquet file with taxi zones')

    args = parser.parse_args()

    main(args)
