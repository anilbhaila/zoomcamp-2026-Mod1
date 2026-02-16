FROM ubuntu:latest
RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install dbt-duckdb --break-system-packages
VOLUME 
WORKDIR /app
