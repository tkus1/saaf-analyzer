#!/bin/bash

# 既存の初期化処理
superset fab create-admin \
    --username admin \
    --firstname Superset \
    --lastname Admin \
    --email admin@example.com \
    --password admin

superset db upgrade
superset init

# DuckDB 接続先の自動登録
superset import-datasources -p /app/superset_home/predefined_duckdb.yaml

# Superset 起動
superset run -p 8088 --with-threads --reload --debugger --host 0.0.0.0
