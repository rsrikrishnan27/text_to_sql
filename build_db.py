import pandas as pd
import sqlite3
import json
import numpy as np

# === CONFIG ===
DB_FILE = "smartgrid.db"
TABLE_NAME = "smartgrid"
SCHEMA_FILE = "schema.json"
DESC_FILE = "desc.json"

TABLE_NAME = "smartgrid"
DB_FILE = "smartgrid.db"

# === LOAD DATA ===
df = pd.read_csv("smart_grid_dataset.csv")

df.columns = (df.columns.str.strip().str.replace('[^A-Za-z0-9_]+', '_', regex=True))

# === CREATE SQLITE DB ===
with sqlite3.connect(DB_FILE) as conn:
    df.to_sql(TABLE_NAME, conn, if_exists="replace", index=False)
print(f"✅ Database '{DB_FILE}' created with table '{TABLE_NAME}' ({len(df)} rows).")

# === LOAD DESCRIPTIONS ===
# Load descriptions from the JSON file
with open("desc.json", "r") as f:
    descriptions = json.load(f)

# === BUILD SCHEMA JSON ===
schema = {
    "table_name": TABLE_NAME,
    "columns": []
}

for col in df.columns:
    col_data = df[col].dropna()
    col_type = str(df[col].dtype)
    entry = {
        "name": col,
        "type": col_type,
        "description": descriptions.get(col, "No description available.")
    }

    # numeric or datetime → add range
    if np.issubdtype(df[col].dtype, np.number):
        entry["range"] = {"min": float(col_data.min()), "max": float(col_data.max())}
    elif np.issubdtype(df[col].dtype, np.datetime64) or col == "Timestamp":
        # Special handling for Timestamp column, whether it's datetime type or not
        if col == "Timestamp":
            # Convert to datetime if it's not already
            if not np.issubdtype(df[col].dtype, np.datetime64):
                try:
                    timestamp_data = pd.to_datetime(col_data)
                    entry["range"] = {
                        "min": str(timestamp_data.min()),
                        "max": str(timestamp_data.max())
                    }
                except:
                    # If conversion fails, leave as is
                    if np.issubdtype(df[col].dtype, np.number):
                        entry["range"] = {"min": float(col_data.min()), "max": float(col_data.max())}
            else:
                entry["range"] = {"min": str(col_data.min()), "max": str(col_data.max())}
        else:
            entry["range"] = {"min": str(col_data.min()), "max": str(col_data.max())}

    schema["columns"].append(entry)

# === SAVE SCHEMA JSON ===
with open("schema.json", "w") as f:
    json.dump(schema, f, indent=2)

print(f"✅ Schema JSON created with {len(schema['columns'])} columns.")


