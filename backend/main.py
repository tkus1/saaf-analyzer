# main.py
from fastapi import FastAPI, Query
from loader import load_csv_by_uuid, load_event_trace_by_uuid
from fastapi.responses import JSONResponse
import duckdb
import shutil
import os

DB_PATH = "./db/analysis.duckdb"
DB_REPLICA_PATH = "./db/analysis_superset.duckdb"

app = FastAPI()

def initialize_views():
    con = duckdb.connect(DB_PATH)
    tables = con.execute("SHOW TABLES").fetchall()
    table_names = {t[0] for t in tables}

    if "loadtest_data" in table_names:
        con.execute("""
            CREATE OR REPLACE VIEW loadtest_data_binned_10ms AS
            WITH uuid_min AS (
              SELECT source_uuid, MIN(startTime) AS min_start
              FROM loadtest_data
              GROUP BY source_uuid
            ),
            base AS (
              SELECT d.*, d.startTime - u.min_start AS start_offset
              FROM loadtest_data d
              JOIN uuid_min u ON d.source_uuid = u.source_uuid
            )
            SELECT *,
                   CAST(FLOOR(start_offset / 10) * 10 AS BIGINT) AS start_bin_10ms
            FROM base;
        """)

        con.execute("""
            CREATE OR REPLACE VIEW loadtest_data_binned_1s AS
            WITH uuid_min AS (
                SELECT source_uuid, MIN(startTime) AS min_start
                FROM loadtest_data
                GROUP BY source_uuid
            ),
            base AS (
                SELECT d.*, d.startTime - u.min_start AS start_offset
                FROM loadtest_data d
                JOIN uuid_min u ON d.source_uuid = u.source_uuid
            )
            SELECT *,
                CAST(FLOOR(start_offset / 1000) * 1000 AS BIGINT) AS start_bin_1s
            FROM base;
        """)

    if "event_trace_data" in table_names:
        con.execute("""
            CREATE OR REPLACE TABLE event_trace_data_augmented AS
            SELECT *,
                   requestTimeFromVM - targetStartTime AS dispatchLatency,
                   startTimeFromLambda - targetStartTime AS responseLatency
            FROM event_trace_data;
        """)

        con.execute("""
            CREATE OR REPLACE VIEW event_trace_data_binned_10ms AS
            SELECT *,
                   CAST(FLOOR(targetStartTime / 10) * 10 AS BIGINT) AS target_bin_10ms
            FROM event_trace_data_augmented;
        """)

        con.execute("""
            CREATE OR REPLACE VIEW event_trace_data_binned_1s AS
            SELECT *,
                   CAST(FLOOR(targetStartTime / 1000) * 1000 AS BIGINT) AS target_bin_1s
            FROM event_trace_data_augmented;
        """)

    con.close()

@app.on_event("startup")
def startup_event():
    initialize_views()

@app.post("/load")
def load_data(
    uuid: str = Query(..., description="UUID to search in filenames"),
    data_dir: str = Query("./data", description="Directory to search for CSV files")
):
    already_loaded1, success1 = load_csv_by_uuid(uuid, data_dir)
    already_loaded2, success2 = load_event_trace_by_uuid(uuid, data_dir)

    if success1 or success2:
        try:
            initialize_views()
            shutil.copy2(DB_PATH, DB_REPLICA_PATH)
        except Exception as e:
            return {
                "status": "ok_but_snapshot_failed",
                "uuid": uuid,
                "already_loaded": (already_loaded1, already_loaded2),
                "error": str(e)
            }

    return {
        "status": "ok" if (success1 or success2) else "not found",
        "uuid": uuid,
        "already_loaded": (already_loaded1, already_loaded2)
    }
