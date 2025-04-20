#!/bin/bash
# 対象のディレクトリ（適宜変更してください）
DIR="."

# 検索する UUID のリスト
UUIDS=(
"c1328506-e8e9-43a2-993d-6e765d21ceff"
"3bb2087a-5409-4bda-aaaf-e872b07a2b19"
"1d6442b5-0bcc-40a4-b233-c46132042c98"
"f9dfd25a-13a3-4dfc-a4d5-506a21e2b7c8"
"74510dfc-8086-4c71-a4fe-43bd12b29537"
"c21234b0-8739-4f24-8342-4b7bac4ec581"
"356ede4d-7693-4383-9654-f18c85d4c5ed"
"0d1aa2c9-80c2-4451-8ed3-b288a577438e"
"43909863-b38a-47a3-93a3-015e04558dd5"
"dcafed2b-1686-455e-8808-5b397dea66e9"
"8846bfe3-6b85-4a77-ac34-c907ac1bfec1"
"26477386-b8a7-4396-a1a3-13ec17c251bb"
"58cc5281-15bc-4dfe-b0d7-4be34f18d83c"
)

# 見つからなかった UUID を格納する配列
not_found_uuids=()

# 対象ディレクトリ直下のファイル名一覧を取得
files=$(ls "$DIR")

# 各 UUID について、ファイル名に含まれているかチェック
for uuid in "${UUIDS[@]}"; do
  echo "Searching for ${uuid} in file names in ${DIR}..."
  if echo "$files" | grep -q "$uuid"; then
    echo "Found ${uuid} in the following file(s):"
    echo "$files" | grep "$uuid"
  else
    echo "Not found: ${uuid}"
    not_found_uuids+=("$uuid")
  fi
  echo "------------------------"
done

# 見つからなかった UUID のみまとめて表示
echo "=== Not found UUIDs ==="
if [ ${#not_found_uuids[@]} -eq 0 ]; then
  echo "All UUIDs were found."
else
  for uuid in "${not_found_uuids[@]}"; do
    echo "$uuid"
  done
fi
