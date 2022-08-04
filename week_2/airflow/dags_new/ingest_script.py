
import pandas as pd
import os

from time import time

from sqlalchemy import create_engine

def ingest_callable(user, password, host, port, db, table_name, csv_file, URL_TEMPLATE):

    print("URL TEMPLATE")
    print(URL_TEMPLATE)

    print("TABLE NAME AND CSV")
    print(table_name, csv_file)
    # user = params.user
    # password = params.password
    # host = params.host
    # port = params.port
    # db = params.db
    # table_name = params.table_name
    # parquet_name = 'output.parquet'
    # print("accepted params")

    # ### SQLAlchemy to generate DDL schema for dataframe which works with postgres:

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    print("created engine")

    engine.connect()

    print('connection established successfully, inserting data...')

    t_start = time()
    df_iter = pd.read_csv(csv_file, iterator=True, chunksize=100000)

    print('successfully read csv_file')

    df = next(df_iter)

    print('successfully fetched df_iter')

    print(table_name)
    print(csv_file)

    print(df.head(5))

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    print('past tpep_pickup_datetime')
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')

    t_end = time()
    print('inserted the first chunk, took %.3f second' % (t_end - t_start))

    while True: 
        t_start = time()

        try:
            df = next(df_iter)
        except StopIteration:
            print("completed")
            break

        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        df.to_sql(name=table_name, con=engine, if_exists='append')

        t_end = time()

        print('inserted another chunk, took %.3f second' % (t_end - t_start))