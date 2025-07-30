#!/bin/bash

# レーザーポインターのスクリプトパス（環境に合わせて調整）
LASER_SCRIPT="$HOME/.local/bin/laser_pointer_overlay.py"
PROCESS_NAME="laser_pointer_overlay.py"

# .odp または .pptx の、拡張子以外のファイル名を取得（拡張子を増やすならここ）
FILENAME_NOEXT=$(wmctrl -l | grep -E '\.(odp|pptx)' | sed -E 's/^.* ([^ ]+)\.(odp|pptx).*$/\1/' | head -n 1)

if [ -z "$FILENAME_NOEXT" ]; then
  echo "✗ スライドファイル（.odp または .pptx）が見つかりません"
  exit 1
fi

# 発表者ツール（コンソール）が存在するか確認
if ! wmctrl -l | grep -q "コンソール: $FILENAME_NOEXT"; then
  echo "✗ 発表者ツール（コンソール: $FILENAME_NOEXT）が見つかりません"
  exit 1
fi

# すでにレーザーポインターが動作中か確認
PID=$(pgrep -f "$PROCESS_NAME")

if [ -z "$PID" ]; then
  echo "✓ レーザーポインターを起動します"
  python3 "$LASER_SCRIPT" &
else
  echo "✓ レーザーポインターを終了します（PID: $PID）"
  kill "$PID"
fi
