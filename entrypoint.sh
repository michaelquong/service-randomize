#! /bin/sh
set -e

# Apply migrations
echo "applying database upgrades..."
make db_upgrade

exec make "$@"
