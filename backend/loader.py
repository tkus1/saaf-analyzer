# loader.py
import os
import pandas as pd
import duckdb

DB_PATH = "./db/analysis.duckdb"
LOADTEST_TABLE = "loadtest_data"
EVENTTRACE_TABLE = "event_trace_data"


def load_csv_by_uuid(uuid: str, data_dir: str) -> tuple[bool, bool]:
    """Loads loadtest_data (inspectSummary_{uuid}.csv)"""
    filename = f"inspectSummary_{uuid}.csv"
    filepath = os.path.join(data_dir, filename)

    if not os.path.isfile(filepath):
        return False, False

    df = pd.read_csv(filepath)
    df['source_uuid'] = uuid

    con = duckdb.connect(DB_PATH)
    con.register("tmp_df", df)

    con.execute(f"""
        CREATE TABLE IF NOT EXISTS {LOADTEST_TABLE} AS 
        SELECT * FROM tmp_df LIMIT 0
    """)

    existing = con.execute(f"""
        SELECT COUNT(*) FROM {LOADTEST_TABLE} WHERE source_uuid = '{uuid}'
    """).fetchone()[0]

    if existing == 0:
        con.execute(f"INSERT INTO {LOADTEST_TABLE} SELECT * FROM tmp_df")
        con.close()
        return False, True
    else:
        con.close()
        return True, True


def load_event_trace_by_uuid(uuid: str, data_dir: str) -> tuple[bool, bool]:
    """Loads event_trace_data (event_trace_report_{uuid}.csv)"""
    filename = f"event_trace_report_{uuid}.csv"
    filepath = os.path.join(data_dir, filename)

    if not os.path.isfile(filepath):
        return False, False

    df = pd.read_csv(filepath)
    df['source_uuid'] = uuid

    con = duckdb.connect(DB_PATH)
    con.register("tmp_df", df)

    con.execute(f"""
        CREATE TABLE IF NOT EXISTS {EVENTTRACE_TABLE} AS 
        SELECT * FROM tmp_df LIMIT 0
    """)

    existing = con.execute(f"""
        SELECT COUNT(*) FROM {EVENTTRACE_TABLE} WHERE source_uuid = '{uuid}'
    """).fetchone()[0]

    if existing == 0:
        con.execute(f"INSERT INTO {EVENTTRACE_TABLE} SELECT * FROM tmp_df")
        con.close()
        return False, True
    else:
        con.close()
        return True, True
