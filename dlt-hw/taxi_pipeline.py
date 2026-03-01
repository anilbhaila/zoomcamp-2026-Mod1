import dlt
from dlt.sources.rest_api import rest_api_resources
from dlt.sources.rest_api.typing import RESTAPIConfig


@dlt.source
def taxi_pipeline_rest_api_source(year: int = 2019, month: int = 1):
    """REST API source for NYC taxi trips served by the Zoomcamp demo API."""
    config: RESTAPIConfig = {
        "client": {
            # Cloud Function serving NYC taxi data
            "base_url": "https://us-central1-dlthub-analytics.cloudfunctions.net",
            # Paginate with `page` query parameter until an empty page is returned
            "paginator": {
                "type": "page_number",
                "base_page": 1,
                "page_param": "page",
                "total_path": None,  # API returns raw array, no total metadata
                "stop_after_empty_page": True,
            },
        },
        # Defaults applied to all resources
        "resource_defaults": {
            "endpoint": {
                # Constant query parameters for this run
                "params": {
                    "year": year,
                    "month": month,
                },
            },
        },
        "resources": [
            {
                "name": "nyc_taxi_trips",
                "endpoint": {
                    # Path part of the Cloud Function URL
                    "path": "data_engineering_zoomcamp_api",
                },
            },
        ],
    }

    yield from rest_api_resources(config)


pipeline = dlt.pipeline(
    pipeline_name="taxi_pipeline",
    destination='duckdb',
    # `refresh="drop_sources"` ensures the data and the state is cleaned
    # on each `pipeline.run()`; remove the argument once you have a
    # working pipeline.
    refresh="drop_sources",
    # show basic progress of resources extracted, normalized files and load-jobs on stdout
    progress="log",
)


if __name__ == "__main__":
    load_info = pipeline.run(taxi_pipeline_rest_api_source())
    print(load_info)  # noqa: T201
