#!/bin/bash

set -e
mkdir -p /app/output
chown 1000:1000 /app/output
chmod 755 /app/output
exec su appuser -c "cd /app && python src/main.py"
