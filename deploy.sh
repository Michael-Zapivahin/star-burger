#!/bin/bash
echo "Start, deploy Star Burger!"
deploy_complete=true
cp -r /opt/star-burger /opt/star-burger_bak
git commit -m "deploy star burger"
git pull
if [ $? -eq 0 ]
then
  echo "Successfully copy files"
else
  deploy_complete=false
  echo "Could not copy files"
  exit
fi

python manage.py migrate
source env/bin/activate

if [ $? -eq 0 ]
then echo "activate env"
else
  deploy_complete=false
  echo "Could not activate env"
  exit
fi

pip install -r requirements.txt
python manage.py collectstatic

deactivate

sudo systemctl restart star-burger
sudo systemctl restart nginx

last_commit=$(git rev-parse HEAD);
if $deploy_complete
then
  curl -H "X-Rollbar-Access-Token: 11e6490dd241478dbda78a15a874db0a" -H "Content-Type: application/json" -X POST 'https://api.rollbar.com/api/1/deploy' -d '{"environment": "Star_burger", "revision": "{$last_commit}", "rollbar_name": "zapivahin", "local_username": "circle-ci", "comment": "star burger deployment", "status": "succeeded"}'
else
  echo "Could not deploy"
fi




