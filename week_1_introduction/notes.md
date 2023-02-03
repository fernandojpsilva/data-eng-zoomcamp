# Steps
1. cd to directory
2. 'docker-compose up' where the Dockerfile is
3. Open Python server 'winpty python -m http.server'
4. Ingest using your Python script

```
winpty python ingest_data.py \
      --user=root \
      --password=root \
      --host=localhost \
      --port=5431 \
      --db=ny_taxi \
      --table_name=yellow_taxi_trips \
      --url="http://<IP>:8000/yellow_tripdata_2021-01.csv"
```


# HW - Start docker containers and ingest data to db
1. docker-compose up

2. winpty python ingest_data.py \
      --user=root \
      --password=root \
      --host=localhost \
      --port=5431 \
      --db=ny_taxi \
      --table_name=green_taxi_trips \
      --table_name_2=taxi_zones

***********************************************************
## Not so important notes
### Git Bash db
docker run -it \
      -e POSTGRES_USER=root \
      -e POSTGRES_PASSWORD=root \
      -e POSTGRES_DB=ny_taxi \
      -v //c/Users/Fernando/PycharmProjects/data-eng-zoomcamp/week_1_introduction/docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data \
      -p 5431:5432 \
      postgres:13

***********************************************************

### CMD
pgcli -h localhost -p 5431 -u root -d ny_taxi

***********************************************************

### pgadmin
docker run -it \
      -e PGADMIN_DEFAULT_EMAIL=admin@admin.com \
      -e PGADMIN_DEFAULT_PASSWORD=root \
      -p 8080:80 \
      dpage/pgadmin4

***********************************************************

### Network
cd PycharmProjects/data-eng-zoomcamp/week_1_introduction/docker_sql/

docker network create pg-network

docker run -it \
      -e POSTGRES_USER=root \
      -e POSTGRES_PASSWORD=root \
      -e POSTGRES_DB=ny_taxi \
      -v //c/Users/Fernando/PycharmProjects/data-eng-zoomcamp/week_1_introduction/docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data \
      -p 5431:5432 \
      --network=pg-network \
      --name pg-database \
      postgres:13

docker run -it \
      -e PGADMIN_DEFAULT_EMAIL=admin@admin.com \
      -e PGADMIN_DEFAULT_PASSWORD=root \
      -p 8080:80 \
      --network=pg-network \
      --name pgadmin \
      dpage/pgadmin4

URL (remote) = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

URL2 (local) = "http://<IP>/yellow_tripdata_2021-01.csv"

winpty python ingest_data.py \
      --user=root \
      --password=root \
      --host=localhost \
      --port=5431 \
      --db=ny_taxi \
      --table_name=yellow_taxi_trips \
      --url="http://<IP>/yellow_tripdata_2021-01.csv"

python ingest_data.py --user=root --password=root --host=localhost --port=5431 --db=ny_taxi --table_name=yellow_taxi_trips --url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

docker build -t taxi_ingest:v001 .

winpty docker run -it --network=pg-network taxi_ingest:v001 \
      --user=root \
      --password=root \
      --host=pg-database \
      --port=5432 \
      --db=ny_taxi \
      --table_name=yellow_taxi_trips \
      --url="http://<IP>/yellow_tripdata_2021-01.csv"

***********************************************************

### Docker-Compose
1. docker-compose up

or

1. docker-compose up -d 

2. docker compose down

