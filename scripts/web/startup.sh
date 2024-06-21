#!/usr/bin/env bash

echo "Start service"

# migrate database
python scripts/migrate.py

# load fixtures
python scripts/load_data.py fixture/calendar/calendar.user.json


exec uvicorn src.main:create_app --host=$BIND_IP --port=$BIND_PORT
