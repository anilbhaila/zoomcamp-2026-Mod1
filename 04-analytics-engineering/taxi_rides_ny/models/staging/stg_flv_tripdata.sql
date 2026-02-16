with source as(
    select * from {{ source('raw', 'fhv_tripdata') }}
),

renamed as (
    Select
        --Identifiers
        dispatching_base_num,
        cast(pickup_datetime as timestamp) as pickup_datetime,
        cast(dropoff_datetime as timestamp) as dropoff_datetime,
        cast(pulocationid as integer) as pickup_location_id,
        cast(dolocationid as integer) as dropoff_location_id,
        SR_FLAG as sr_flag,
        cast(affiliated_base_number as string) as affiliated_base_number
    from source
    where dispatching_base_num is not null
)

select count(*) from renamed
-- Sample records for dev environment using deterministic date filter