#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import os
from sqlalchemy import create_engine
import argparse
import pyarrow.parquet as pq

def main(params):

    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    parquet_name = 'output.parquet'
    print("accepted params")

    # ### SQLAlchemy to generate DDL schema for dataframe which works with postgres:

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    print("created engine")
    # ### Read NYC taxi data

     #"yellow_tripdata_2022-01.parquet"

    os.system(f"curl {url} -o {parquet_name}")
    print("downloaded file")

    parquet_table = pq.read_table(parquet_name)
    df = parquet_table.to_pandas()

    print("saved data to dataframe")

    print("creating a table if it does not exist")
    df.head(n=0).to_sql(name="yellow_taxi_trips", con=engine, if_exists='replace')

    print("attempting to insert data")
    df.to_sql(name="yellow_taxi_trips", con=engine, if_exists='append', chunksize=10000)

    print("loaded data to server .. DONE")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    # user, password, host, port, databasename, tablename, url of the csv

    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table where we will write the results to in postgres')
    parser.add_argument('--url', help='url of the csv file')

    args = parser.parse_args()

    main(args)


