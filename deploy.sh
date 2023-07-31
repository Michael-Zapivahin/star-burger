#!/bin/bash
echo "Start, deploy Star Burger!"
cp -r /opt/star-burger /opt/star-burger_bak
git commit -m "deploy star burger"
# hash later commit:  'git rev-parse HEAD'
git pull
if [ $? -eq 0 ]
then echo "Successfully copy files"
else echo "Could not copy files" exit
fi
python manage.py migrate

source env/bin/activate
if [ $? -eq 0 ]
then echo "activate env"
else echo "Could not activate env" exit
fi
pip install -r requirements.txt
./node_modules/.bin/parcel watch bundles-src/index.js --dist-dir bundles --public-url="./"
python manage.py collectstatic
deactivate

sudo systemctl restart star-burger
sudo systemctl restart nginx

git rev-parse HEAD

if [ $? -eq 0 ]
then echo "activate env"
else echo "Could not activate env" exit
fi
