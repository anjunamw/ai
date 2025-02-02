#!/bin/sh
# entrypoint.sh
set -e

# Convert .env to config.json (if needed) by calling the config_loader
python config_loader.py

# Execute the command passed as arguments (for example, uvicorn)
exec "$@"