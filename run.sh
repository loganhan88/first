#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [[ ! -d .venv ]]; then
  python -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install -r requirements.txt || {
  echo "[WARN] 依赖安装失败，尝试继续运行（若缺失关键依赖会报错）。"
}

python main.py --once
