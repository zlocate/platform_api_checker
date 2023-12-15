#!/bin/sh
PORT="${PORT:-8080}"
exec uvicorn app.main:app --proxy-headers --host 0.0.0.0 --port "$PORT"