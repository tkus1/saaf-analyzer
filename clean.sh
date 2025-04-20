#!/bin/bash
set -e

echo "[INFO] Cleaning DuckDB database files..."
rm -f ./db/analysis.duckdb
rm -f ./db/analysis_superset.duckdb


echo "[INFO] Cleaning __pycache__ and temp files..."
find . -type d -name '__pycache__' -exec rm -r {} +

echo "[DONE] Local environment cleaned."
