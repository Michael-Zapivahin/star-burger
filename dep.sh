#!/bin/bash
# start with the parameter ROLLBAR_ACCESS_TOKEN
# bash dep.sh 123e6490dd24147example
echo "Start, deploy Star Burger!"
deploy_complete=true

set -e

git pull
python manage.py migrate --noinput
source env/bin/activate
npm ci --dev
pip install -r requirements.txt
python manage.py collectstatic --noinput
deactivate

sudo systemctl restart star-burger
sudo systemctl reload nginx

last_commit=$(git rev-parse HEAD);
# $1 ROLLBAR_ACCESS_TOKEN
if $deploy_complete
then
  echo "Deploy completed successfully"
  echo "Last commit {$last_commit}"
  curl -H "X-Rollbar-Access-Token: $1" -H "Content-Type: application/json" -X POST 'https://api.rollbar.com/api/1/deploy' -d '{"environment": "Star_burger", "revision": "{$last_commit}", "rollbar_name": "zapivahin", "local_username": "circle-ci", "comment": "star burger deployment", "status": "succeeded"}'
else
  echo "Could not deploy"
fi

