FROM python:3.8.5

RUN apt-get install curl
RUN pip install pandas sqlalchemy psycopg2 pyarrow

WORKDIR /app
COPY ingest_data.py ingest_data.py

# ENTRYPOINT [ "bash" ]

ENTRYPOINT [ "python", "ingest_data.py"]