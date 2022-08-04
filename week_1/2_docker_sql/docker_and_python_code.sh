
----------------------------------------------------------------------------------------------------
DOCKER POSTGRES AND PGADMIN
----------------------------------------------------------------------------------------------------

--Docker postgres database

docker run -it \
-e POSTGRES_USER="root" \
-e POSTGRES_PASSWORD="root" \
-e POSTGRES_DB="ny_taxi" \
-v /Users/sthakur/Desktop/sthakur\ 2/Documents/Office\ CBS\ Interactive/2022/zoomcamp/2_docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data \
-p 5432:5432 \
postgres:13


--Docker pgadmin

docker run -it \
-e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
-e PGADMIN_DEFAULT_PASSWORD="root" \
-p 8080:80 \
dpage/pgadmin4

----------------------------------------------------------------------------------------------------
DOCKER WITHIN NETWORK
----------------------------------------------------------------------------------------------------

-- Docker create network

docker create network pg-network


--Docker postgres database within network

docker run -it \
-e POSTGRES_USER="root" \
-e POSTGRES_PASSWORD="root" \
-e POSTGRES_DB="ny_taxi" \
-v /Users/sthakur/Desktop/sthakur\ 2/Documents/Office\ CBS\ Interactive/2022/zoomcamp/2_docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data \
-p 5432:5432 \
--network=pg-network \
--name pg-database \
postgres:13



--Docker pgadmin within network

docker run -it \
-e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
-e PGADMIN_DEFAULT_PASSWORD="root" \
-p 8080:80 \
--network=pg-network \
--name pgadmin \
dpage/pgadmin4



----------------------------------------------------------------------------------------------------
PYHTON DATA INGESTION SCRIPT
----------------------------------------------------------------------------------------------------

-- Python ingest data script

python ingest_data.py \
	--user=root \
	--password=root \
	--host=localhost \
	--port=5432 \
	--db=ny_taxi \
	--table_name=yellow_taxi_trips \
	--url="https://nyc-tlc.s3.amazonaws.com/trip+data/yellow_tripdata_2022-01.parquet"

-- Docker build for ingest_data.py

docker build -t taxi_ingest:v001 .


-- Docker script for for ingest_data.py

docker run -it \
	--network=pg-network \
	taxi_ingest:v001 \
	--user=root \
	--password=root \
	--host=pg-database \
	--port=5432 \
	--db=ny_taxi \
	--table_name=yellow_taxi_trips \
	--url="https://nyc-tlc.s3.amazonaws.com/trip+data/yellow_tripdata_2022-01.parquet"


----------------------------------------------------------------------------------------------------
GCP VM DATA INGESTION SCRIPT
----------------------------------------------------------------------------------------------------

-- Docker build for ingest_data.py

docker build -t taxi_ingest:v001 .


-- Docker script for for ingest_data.py

docker run -it \
	--network=2_docker_sql_default \
	taxi_ingest:v001 \
	--user=root \
	--password=root \
	--host=pgdatabase \
	--port=5432 \
	--db=ny_taxi \
	--table_name=yellow_taxi_trips \
	--url="https://nyc-tlc.s3.amazonaws.com/trip+data/yellow_tripdata_2021-01.parquet"

-- Docker script for for ingest_zones_data.py

docker run -it \
	--network=2_docker_sql_default \
	taxi_zones_ingest:v001 \
	--user=root \
	--password=root \
	--host=pgdatabase \
	--port=5432 \
	--db=ny_taxi \
	--table_name=taxi_zones \
	--url="https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv"

