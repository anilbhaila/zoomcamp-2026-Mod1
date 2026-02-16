Welcome to your new dbt project!

### Using the starter project

Try running the following commands:
- dbt run
- dbt test


### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices



# /home/codespace/.dbt/profiles.yml
# Two targets are defined. dev for bigquery and duckdb_target for duckdb
taxi_rides_ny:
  target: dev
  outputs:
    dev:
      dataset: zoomcamp_kestra
      job_execution_timeout_seconds: 600
      job_retries: 1
      keyfile: /workspaces/zoomcamp-2026-Mod1/04-analytics-engineering/keys/my-creds.json
      location: us-south1
      method: service-account
      priority: interactive
      project: kestra-sandbox-486219
      threads: 2
      type: bigquery
      settings:
        memory_limit: '2GB'
        preserve_insertion_order: false
    
    #local DockDB Profile
    duckdb_target:
      type: duckdb
      path: taxi_rides_ny.duckdb
      schema: prod
      threads: 1
      extensions:
        - parquet
      settings:
        memory_limit: '2GB'
        preserve_insertion_order: false
  

# Run below command for bigquery target.
dbt debug
dbt debug --target dev

# Run below command for duckdb target
dbt debug --target duckdb_target

All check passed! (That means you are ready!!)

# To look inside duckdb, use DuckDB CLI if installed.
duckdb taxi_rides.duckdb

# If no CLI installed, use dbt CLI
dbt run --target duckdb_target
dbt show --select stg_green_tripdata --limit 10 --target duckdb_target