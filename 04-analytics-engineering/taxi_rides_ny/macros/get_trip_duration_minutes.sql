{#
    Calculate trip duration in minutes from prickup and dropoff timestamps.

    Uses dbts built-in cross-database datediff macro.
    This works seamlessly across DuckDB, BigQuery, Snowflake, Redshift, PostgreSQL, dbt_utils.test_equal_rowcount

    Returns: Trip duration as a numeric value in minutes.

#}

{% macro get_trip_duration_minutes(pickup_datetime, dropoff_datetime) %}
    {{ dbt.datediff( pickup_datetime, dropoff_datetime, 'minute')}}
{% endmacro %}