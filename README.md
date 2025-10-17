# Text-to-SQL

A lightweight PoC that converts natural language questions into SQLite queries using **Gemini 2.5 Flash**.  
Data source: **Kaggle Smart Grid dataset**.  

---

### 📁 Repository Structure

| File | Description |
|------|--------------|
| `build_db.py` | Converts CSV to SQLite DB and generates schema JSON |
| `config_template.json` | Template config (safe to share) |
| `prompts.py` | Full and lite SQL generation prompts |
| `run_prompt.py` | Runs user questions through the LLM and logs results |
| `sql_tester.py` | For reviewing generated queries and running tests |
| `results_log.json` | Logged interactions (optional) |
| `schema.json` | Auto-generated schema |
| `desc.json` | Editable field descriptions |

---
