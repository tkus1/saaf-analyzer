#!/bin/bash

API_URL="http://localhost:8000/load"
DATA_DIR="./data"

for file in "$DATA_DIR"/inspectSummary_*.csv; do
  # UUID部分を抽出（inspectSummary_ と .csv の間の部分）
  filename=$(basename "$file")
  uuid="${filename#inspectSummary_}"
  uuid="${uuid%.csv}"

  echo "Posting UUID: $uuid"
  curl -s -X POST "$API_URL?uuid=$uuid"
  echo ""  # 改行を追加
done
