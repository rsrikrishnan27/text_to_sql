import json, time, re
from datetime import datetime
from google import genai
from prompts import sql_prompt_full, sql_prompt_lite, examples_section
from datetime import datetime, UTC


# ---- load config ----
with open("config.json") as f:
    config = json.load(f)

MODEL = config["model"]["name"]
API_KEY = config["model"]["api_key"]
LOG_FILE = config["files"]["log"]

client = genai.Client(api_key=API_KEY)


def run_prompt(user_question: str):
    """Generate SQL query and log results."""
    schema_path = list(config["database"]["tables"].values())[0]
    with open(schema_path) as f:
        schema_json = json.dumps(json.load(f), indent=2)

    examples = examples_section if config["prompt"]["examples_enabled"] else ""
    prompt = sql_prompt_full.format(
        schema_json=schema_json,
        examples=examples,
        user_question=user_question,
    )

    start = time.time()
    response = client.models.generate_content(model=MODEL, contents=prompt)
    elapsed = round(time.time() - start, 2)

    match = re.search(r"<SQL>(.*?)</SQL>", response.text, re.DOTALL)
    sql_query = match.group(1).strip() if match else response.text.strip()

    print(f"\n[Generated in {elapsed}s]\n{sql_query}\n")

    # ---- logging ----
    log_cfg = config["logging"]
    if log_cfg.get("enabled", True):
        entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "elapsed_seconds": elapsed,
            "user_query": user_question,
            "model_name": MODEL,
            "examples_enabled": config["prompt"]["examples_enabled"],
            "sql_output": sql_query,
        }
        if log_cfg.get("include_prompt"):
            entry["prompt_used"] = prompt

        # Load, append, and write back in pretty JSON format
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)

        logs.append(entry)

        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)

    return sql_query


user_question = "Is there evidence that electricity consumption decreases when prices are high? Compare consumption across different price brackets."

if __name__ == "__main__":
    run_prompt(user_question)
