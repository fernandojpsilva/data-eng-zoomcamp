## Docker basics concepts

To run a docker image in interactive mode (-it) and be able to interact via terminal, we use the following command where 'bash' is a parameter to our image 'ubuntu':

`docker run -it ubuntu bash`

This docker container will be stateless.: any changes done inside a container will NOT be saved when the container is killed and started again. This is an advantage because it allows us to restore any container to its initial state in a reproducible manner, but we will have to store data elsewhere if we need to do so; a common way to do so is with volumes.

To build a docker image from a 'Dockerfile', we use the command:

`docker build -t test:pandas .` 

and run it with:

`docker run -it test:pandas 2021-01-15`

where '2021-01-15' is an argument taken by our pipeline.py script.

## Dockerfile

A Dockerfile instantiates our docker image. We created it using the file:

```dockerfile
FROM python:3.9

RUN pip install pandas
RUN pip install pyarrow

WORKDIR /app
COPY pipeline.py pipeline.py

ENTRYPOINT [ "python", "pipeline.py" ]
```

where 'FROM' specifies the base docker image we will build on, 'RUN' sets up our image by installing prerequisites, 'WORKDIR' creates/specifies the working directory inside the container, 'COPY' copies the script to the container (first is source name, second is destination name) and 'ENTRYPOINT' defines what to do when the container runs.


## Basic pipeline

Our first pipeline will simply import the needed packages for our task, take an argument (as seen above) and print it. It is a very basic Python script to make sure everything is working.

```python
import sys
import pandas as pd

print(sys.argv)

day = sys.argv[1]

print(f"job finished successfully for day = {day}")
```

## Postgres in a container

To run our DB with pgAdmin, we need to create a network to connect our DB to pgAdmin:

```docker
docker network create pg-network

docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="ny_taxi" \
    -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
    -p 5432:5432 \
    --network=pg-network \
    --name pg-database \
    postgres:13
    
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pgadmin2 \
  dpage/pgadmin4
```

We can also ingest the data to our DB via Python script (see ingest_data.py). The following command will execute our script that send the data for us to explore in pgAdmin.

```bash
python ingest_data.py \
  --user=root \
  --password=... \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=yellow_taxi_trips \
  --url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
```

## Dockerizing the script

Let's modify the Dockerfile we created before to include our ingest_data.py script and create a new image:

```dockerfile
FROM python:3.9.1

# We need to install wget to download the csv file
RUN apt-get install wget
# psycopg2 is a postgres db adapter for python: sqlalchemy needs it
RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app
COPY ingest_data.py ingest_data.py 

ENTRYPOINT [ "python", "ingest_data.py" ]
```

Build the image:

```docker
docker build -t taxi_ingest:v001 .
```

And run it:

```docker
docker run -it \
    --network=pg-network \
    taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
```