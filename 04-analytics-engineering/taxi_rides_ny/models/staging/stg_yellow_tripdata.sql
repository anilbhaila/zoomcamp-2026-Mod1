select 
    --Identifiers
    cast(vendorid as integer) as vendor_id,
    cast(ratecodeid as integer) as rate_code_id,
    cast(pulocationid as integer) as pickup_location_id,
    cast(dolocationid as integer) as dropoff_location_id,
    
    --Timestamps
    cast(tpep_pickup_datetime as timestamp) as pickup_datetime,
    cast(tpep_dropoff_datetime as timestamp) as dropoff_datetime,
    
    --Trip info
    cast(store_and_fwd_flag as string) as store_and_fwd_flag,
    cast(passenger_count as integer) as passenger_count,
    cast(trip_distance as numeric) as trip_distance,
    01 as trip_type, -- yellow taxi can only be Street-hail, so we can hardcode this value
    
    --Payment details
    cast(fare_amount as numeric) as fare_amount,
    cast(extra as numeric) as extra,
    cast(mta_tax as numeric) as mta_tax,
    cast(tip_amount as numeric) as tip_amount,
    cast(tolls_amount as numeric) as tolls_amount,
    cast(improvement_surcharge as numeric) as improvement_surcharge,
    0 as ehail_fee, -- yellow taxi does not have an e-hail fee, so we can hardcode this value
    cast(total_amount as numeric) as total_amount,
    cast(payment_type as integer) as payment_type

from {{ source('raw_data', 'yellow_tripdata') }}
where vendorid is not null