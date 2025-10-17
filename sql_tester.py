import json
import sqlite3
import pandas as pd
from pathlib import Path

CONFIG_PATH = "config.json"

# ---- Load config ----
with open(CONFIG_PATH) as f:
    config = json.load(f)

DB_PATH = "smartgrid.db"
LOG_FILE = config["files"]["log"]


def get_all_queries():
    """
    Retrieve all user questions and SQL results from the Gemini logs.
    Sorted descending (latest first).
    """
    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No valid log data found.")
        return []

    if not isinstance(logs, list):
        logs = [logs]

    logs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return logs


def run_sql_query(sql_query: str):
    """
    Execute a SQL query directly against the configured SQLite DB.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(sql_query, conn)
        conn.close()
        print(df)
        return df
    except Exception as e:
        print(f"Error executing query: {e}")
        return None


logs = get_all_queries()
print(logs[0]['sql_output'])
run_sql_query(logs[0]['sql_output'])
