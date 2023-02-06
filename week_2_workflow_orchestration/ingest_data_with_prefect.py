#!/usr/bin/env python
# coding: utf-8
import os
import argparse

import pandas as pd
from sqlalchemy import create_engine
from time import time
from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta


@flow(name='Ingest flow')
def main_flow():
    user = 'root'
    password = 'root'
    host = 'localhost'
    port = 5432
    db = 'ny_taxi'
    table_name = 'yellow_taxi_trips'
    zones_table_name = 'zones'
    url_data = 'http://localhost:8000/week_1_basic_n_setup/1_docker_sql/yellow_tripdata_2021-01.csv'
    url_zones = 'http://localhost:8000/week_1_basic_n_setup/1_docker_sql/taxi_zone_lookup.csv'

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    load_data(engine, url_data, table_name)
    load_data(engine, url_zones, zones_table_name)


@task(log_prints=True, retries=1, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def load_data(engine, url, table_name):
    os.system(f"wget {url} -O {table_name}.csv")

    df = pd.read_csv(f'{table_name}.csv')
    t_start = time()
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='append', chunksize=100000)
    t_end = time()
    print('Data ingested, took %.3f seconds' % (t_end - t_start))


if __name__ == '__main__':
    main_flow()
