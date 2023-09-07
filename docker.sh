#!/bin/bash
set -e

cd /opt/star-burger

git fetch
git pull
docker compose -f docker-compose.prod.yml --build up -d

echo star-burged was updated and started!
