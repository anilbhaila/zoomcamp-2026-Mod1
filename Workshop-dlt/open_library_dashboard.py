"""
Open Library Books Dashboard - marimo app.
Uses dlt pipeline data (DuckDB) to show books per author and books over time.
See: https://dlthub.com/docs/general-usage/dataset-access/marimo
"""

import marimo as mo

app = mo.App(width="wide")


@app.cell
def __():
    import duckdb
    from plotly import graph_objects as go

    return duckdb, go


@app.cell
def __(duckdb):
    # Connect to pipeline DuckDB and find the schema with books data
    _conn = duckdb.connect("open_library_pipeline.duckdb", read_only=True)
    _schema_rows = _conn.execute("""
        SELECT table_schema
        FROM information_schema.tables
        WHERE table_name = 'books'
        ORDER BY table_schema DESC
        LIMIT 1
    """).fetchall()
    schema = _schema_rows[0][0] if _schema_rows else None
    _conn.close()
    return schema


@app.cell
def __(duckdb, schema):
    if schema:
        _conn = duckdb.connect("open_library_pipeline.duckdb", read_only=True)
        _rows = _conn.execute(f"""
            SELECT a.value AS author_name, COUNT(DISTINCT b._dlt_id) AS book_count
            FROM "{schema}".books b
            JOIN "{schema}".books__author_name a ON b._dlt_id = a._dlt_parent_id
            GROUP BY a.value
            ORDER BY book_count DESC
            LIMIT 25
        """).fetchall()
        _conn.close()
        books_per_author = {"authors": [r[0] for r in _rows], "counts": [r[1] for r in _rows]}
    else:
        books_per_author = None
    return books_per_author


@app.cell
def __(duckdb, schema):
    if schema:
        _conn = duckdb.connect("open_library_pipeline.duckdb", read_only=True)
        _rows = _conn.execute(f"""
            SELECT first_publish_year AS year, COUNT(*) AS book_count
            FROM "{schema}".books
            WHERE first_publish_year IS NOT NULL
            GROUP BY first_publish_year
            ORDER BY year
        """).fetchall()
        _conn.close()
        books_over_time = {"years": [r[0] for r in _rows], "counts": [r[1] for r in _rows]}
    else:
        books_over_time = None
    return books_over_time


@app.cell
def __(go, mo, books_per_author):
    # Bar chart: number of books per author
    if books_per_author and len(books_per_author["authors"]) > 0:
        _fig = go.Figure(
            data=[go.Bar(x=books_per_author["authors"], y=books_per_author["counts"])],
        )
        _fig.update_layout(
            title="Number of Books per Author (Top 25)",
            xaxis_title="Author",
            yaxis_title="Number of Books",
            xaxis_tickangle=-45,
        )
        bar_chart = _fig
    else:
        bar_chart = mo.md("*No book data available. Run the pipeline first.*")
    return bar_chart


@app.cell
def __(go, mo, books_over_time):
    # Line chart: books over time
    if books_over_time and len(books_over_time["years"]) > 0:
        _fig = go.Figure(
            data=[
                go.Scatter(
                    x=books_over_time["years"],
                    y=books_over_time["counts"],
                    mode="lines+markers",
                )
            ],
        )
        _fig.update_layout(
            title="Books Over Time (by First Publish Year)",
            xaxis_title="Year",
            yaxis_title="Number of Books",
        )
        line_chart = _fig
    else:
        line_chart = mo.md("*No book data available. Run the pipeline first.*")
    return line_chart


@app.cell
def __(bar_chart, line_chart, mo):
    return mo.vstack(
        [
            mo.md("# Open Library Books Dashboard"),
            mo.md("Data from `open_library_pipeline` (DuckDB)."),
            mo.md("## Books per Author"),
            bar_chart,
            mo.md("## Books Over Time"),
            line_chart,
        ]
    )


if __name__ == "__main__":
    app.run()
