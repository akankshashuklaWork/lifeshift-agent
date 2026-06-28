#!/usr/bin/env bash
# Start LifeShift with the custom glassmorphic UI at http://127.0.0.1:8080/lifeshift/
set -euo pipefail
cd "$(dirname "$0")/.."
exec uv run uvicorn app.fast_api_app:app --host 127.0.0.1 --port 8080 --reload
