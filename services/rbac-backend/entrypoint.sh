#!/bin/bash
alembic upgrade head

exec python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
