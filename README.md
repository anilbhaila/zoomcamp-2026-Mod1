# zoomcamp-2026-Mod1
# Stop docker container
docker stop <container_id_or_name>

# If container unresponsive
docker kill <container_id_or_name>

# Stop All Running Containers
docker-compose down

# Remove Specific Containers
# List all containers
docker ps -a

# Remove specific container
docker rm <container_id>

# Remove all stopped containers
docker container prune

# Remove Docker Images
# List all images
docker images

# Remove specific image
docker rmi taxi_ingest:v001

# Remove all unused images
docker image prune -a

# Remove Docker Volumes
# List volumes
docker volume ls

# Remove specific volumes
docker volume rm ny_taxi_postgres_data
docker volume rm pgadmin_data

# Remove all unused volumes
docker volume prune

# Remove Docker Networks
# List networks
docker network ls

# Remove specific network
docker network rm pg-network

# Remove all unused networks
docker network prune

# Complete Cleanup
# Remove ALL Docker resources - use with caution!
# ⚠️ Warning: This removes ALL Docker resources!
docker system prune -a --volumes

# Clean Up Local Files
# Remove parquet files
rm *.parquet

# Remove Python cache
rm -rf __pycache__ .pytest_cache

# Remove virtual environment (if using venv)
rm -rf .venv


# Terraform from Docker Containers. GCP Creds should be placed in $(pwd)/keys/my-creds.json
docker run -- rm -it -v $(pwd):/app -w /app hashicorp/terraform:latest init
docker run -- rm -it -v $(pwd):/app -w /app hashicorp/terraform:latest plan
docker run --rm -it -v $(pwd):/app -w /app hashicorp/terraform:latest apply
docker run --rm -it -v $(pwd):/app -w /app hashicorp/terraform:latest destroy

# command to upload flows to Kestra.
curl -X POST -u 'admin@kestra.io:Admin1234!' http://localhost:8080/api/v1/flows/import -F fileUpload=@flows/02_python.yaml

# Run gcloud in docker image instead of installing in local machine. TO DEPLOY your ML Model in docker
We are in 03-data-warehouse folder
mkdir -p app/tmp (Creates tmp/model directory to store extrected ML Model from gcs)

docker run --rm -it -v $(pwd):/app gcr.io/google.com/cloudsdktool/google-cloud-cli:stable /bin/bash
bq --project_id kestra-sandbox-486219 extract -m zoomcamp_kestra.tip_model gs://kestra-sandbox-486219-gcs/tip_model

gsutil cp -r gs://kestra-sandbox-486219-gcs/tip_model app/tmp/model  (This will copy model from gs to docker container.)
mkdir -p app/serving_dir/tip_model/1
cp -r app/tmp/model/tip_model/* app/serving_dir/tip_model/1
exit  (Exit from gcloud CLI Docker Container)

docker pull tensorflow/serving (Downloads the official TensorFlow Serving image from Docker Hub)
docker run -p 8501:8501 --mount type=bind,source=$(pwd)/serving_dir/tip_model,target=/models/tip_model -e MODEL_NAME=tip_model -t tensorflow/serving &

OR Similar command
docker run -p 8501:8501 \
  -v $(pwd)/serving_dir/tip_model:/models/tip_model \
  -e MODEL_NAME=tip_model \
  -t tensorflow/serving &


curl -d '{"instances": [{"passenger_count":1, "trip_distance":12.2, "PULocationID":"193", "DOLocationID":"264", "payment_type":"2","fare_amount":20.4,"tolls_amount":0.0}]}' -X POST http://localhost:8501/v1/models/tip_model:predict

# We can use POST Man tool as well.
http://localhost:8501/v1/models/tip_model


# MOD4 - analytics engineering

# Instead of installing duckDB in your machine, run it in ubuntu docker container
# Create a Dockerfile which will help to create a my-ubuntu-duckdb docker image
docker run --rm -it -v $(pwd):/app my-ubuntu-duckdb

/workspaces/zoomcamp-2026-Mod1/04-analytics-engineering/keys/my-creds.json
/home/codespace/.dbt/profiles.yml

dbt init
dbt run
dbt show --select stg_yellow_tripdata --limit 100


git reset  "will unset the staged changes"




    database: |
      {% if target.type == 'duckdb' %}
        taxi_rides_ny
      {% else %}
        zoomcamp_kestra_dev
        {{env_var('GCP_PROJECT_ID', 'kestra-sandbox-486219')}}
      {% endif %}
    schema: |
      {% if target.type == 'duckdb' %}
        prod  
      {% else %}
        zoomcamp_kestra
      {% endif %}

dbt run --target duckdb_target
dbt run --target dev     



# GitHub Code space is running out of space
du -h -d 1 | sort -h  (To see which folder is consuming most space)

du -h (Checks overal Disk Space)
du -h -d 1 | sort -h (Finds large Folder & Files in depth 1)
du -h -d 2 | sort -h (Finds large Folder & Files in depth 2)
du -h -d 3 | sort -h (Finds large Folder & Files in depth 3)

Found .venv in pipeline is consuming lots of size.
You can clean according.