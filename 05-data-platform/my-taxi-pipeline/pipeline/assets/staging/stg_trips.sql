/* @bruin
name: staging.stg_trips
type: duckdb.sql

depends:
  - ingestion.raw_trips
  - ingestion.payment_lookup

materialization:
  type: table
  strategy: time_interval
  incremental_key: tpep_pickup_datetime
  time_granularity: timestamp

columns:
  - name: tpep_pickup_datetime
    type: timestamp
    primary_key: true
    checks:
      - name: not_null


@bruin */

SELECT
    t.tpep_pickup_datetime,
    t.tpep_dropoff_datetime,
    t.pulocationid,
    t.dolocationid,
    t.fare_amount,
    t.taxi_type,
    p.payment_type_name
FROM ingestion.raw_trips t
LEFT JOIN ingestion.payment_lookup p
    ON t.payment_type = p.payment_type_id
WHERE t.tpep_pickup_datetime >= '{{ start_datetime }}'
  AND t.tpep_pickup_datetime < '{{ end_datetime }}'
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY t.tpep_pickup_datetime, t.tpep_dropoff_datetime,
                 t.pulocationid, t.dolocationid, t.fare_amount
    ORDER BY t.tpep_pickup_datetime
) = 1