#!/usr/bin/env python
# coding: utf-8

import argparse
import os
import pandas as pd
import wget
from sqlalchemy import create_engine
from time import time


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    table_name_2 = params.table_name_2
    trips_url = 'http://172.23.176.1:8000/green_tripdata_2019-01.csv'
    zones_url = 'http://172.23.176.1:8000/taxi+_zone_lookup.csv'
    csv_trips = 'trips.csv'
    csv_zones = 'zones.csv'

    os.system(f"wget {trips_url} -O {csv_trips}")
    os.system(f"wget {zones_url} -O {csv_zones}")

    print('Files downloaded')

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # Insert Trips
    print('Inserting Trips')
    df_iter = pd.read_csv(csv_trips, iterator=True, chunksize=100000)
    df = next(df_iter)
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='append')

    while True:
        try:
            t_start = time()
            df = next(df_iter)
            df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
            df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
            df.to_sql(name=table_name, con=engine, if_exists='append')
            t_end = time()
            print('Inserted chunk... %.3f seconds' % (t_end - t_start))

        except StopIteration:
            print('Inserting Trips Complete')
            break

    # Insert Zones
    print('Inserting Zones')
    df = pd.read_csv(csv_zones)
    df.to_sql(name=table_name_2, con=engine, if_exists='append')
    print('Inserting Zones Complete')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='db name for postgres')
    parser.add_argument('--table_name', help='name of the table where we will write the trips data')
    parser.add_argument('--table_name_2', help='name of the table where we will write the zones data')
    #parser.add_argument('--trips_url', help='url of the trips csv file')
    #parser.add_argument('--zones_url', help='url of the zones csv file')

    args = parser.parse_args()

    main(args)


