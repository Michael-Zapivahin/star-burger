#!/bin/bash
# start with the parameter ROLLBAR_ACCESS_TOKEN
# bash dep.sh 123e6490dd24147example
echo "Start, deploy Star Burger!"
deploy_complete=true

python manage.py migrate --noinput
if [ $? -eq 0 ]
then
  echo "Successfully migrate"
else
  deploy_complete=false
  exit
fi

source env/bin/activate
if [ $? -eq 0 ]
then echo "activate env"
else
  deploy_complete=false
  exit
fi

npm ci --dev
if [ $? -eq 0 ]
then echo "ci -dev"
else
  deploy_complete=false
  exit
fi
pip install -r requirements.txt
if [ $? -eq 0 ]
then echo "install requirements"
else
  deploy_complete=false
  exit
fi
python manage.py collectstatic --noinput
if [ $? -eq 0 ]
then echo "collect static"
else
  deploy_complete=false
  exit
fi
deactivate

sudo systemctl restart star-burger
sudo systemctl reload nginx

last_commit=$(git rev-parse HEAD);
# $1 ROLLBAR_ACCESS_TOKEN
if $deploy_complete
then
  echo "Deploy completed successfully"
  curl -H "X-Rollbar-Access-Token: {$1}}" -H "Content-Type: application/json" -X POST 'https://api.rollbar.com/api/1/deploy' -d '{"environment": "Star_burger", "revision": "{$last_commit}", "rollbar_name": "zapivahin", "local_username": "circle-ci", "comment": "star burger deployment", "status": "succeeded"}'
else
  echo "Could not deploy"
fi




