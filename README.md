```markdown
# SAAF Analyzer

This project provides a portable, local analysis environment for performance trace data using:

- **FastAPI** for backend ingestion and data processing  
- **DuckDB** as the embedded database  
- **Apache Superset** for interactive dashboards and visualization  

---

## Project Structure

```
saaf-analyzer/
├── backend/                 # FastAPI app
│   ├── main.py
│   ├── loader.py
│   └── ...
├── data/                    # CSV files to be loaded
├── db/                      # DuckDB database files
│   ├── analysis.duckdb
│   └── analysis_superset.duckdb
├── superset/                # Superset setup
│   ├── Dockerfile
│   └── docker-init.sh
├── superset_home/           # Superset config and metadata (persistent)
│   └── superset_config.py
├── scripts/                 # Utility scripts
│   ├── load_all.sh
│   └── clean.sh
└── docker-compose.yml
```

---

## Getting Started

### 1. Clone and enter the directory

```bash
git clone <your-repo-url>
cd saaf-analyzer
```

### 2. Start the system

```bash
docker compose up --build
```

This will:
- Launch the FastAPI server at [http://localhost:8000](http://localhost:8000)
- Launch the Superset UI at [http://localhost:8088](http://localhost:8088)

> First-time Superset users may be prompted to create an admin account on first visit.

---

## Loading Data

Ensure your data files follow this format:  
`data/inspectSummary_<UUID>.csv`

To load a specific file into DuckDB:

```bash
curl -X POST "http://localhost:8000/load?uuid=<UUID>"
```

To load all files automatically:

```bash
bash scripts/load_all.sh
```

---

## Using Superset

1. Open [http://localhost:8088](http://localhost:8088)
2. Log in or create your admin user
3. Connect to the embedded DuckDB:
   - Database: `analysis_superset.duckdb`
   - Path: `/app/db/analysis_superset.duckdb`
   - ✅ Set as **read-only**
4. Explore the `loadtest_data_binned` and `loadtest_data_binned_aggregated` datasets
5. Build dashboards with charts (e.g., line charts, filters)

---

## Cleanup

To delete all local data and metadata:

```bash
bash scripts/clean.sh
```

This will delete:
- DuckDB data files
- Python bytecode and cache files

---

## Notes

- **Data replication**: Each `/load` triggers a copy of `analysis.duckdb` to `analysis_superset.duckdb` to avoid write locks.
- **Views**: The system auto-generates binned views for 10ms and 1s resolution on data load.
- **Native Filters**: Superset’s native filters are supported and persisted in the dashboard state.
- **Superset metadata persistence**: All dashboards, filters, and configurations are stored in `./superset_home/superset.db`.

---

## Requirements

- Docker Desktop (tested on macOS)
- Python and FastAPI are used internally (no local install needed)

---
