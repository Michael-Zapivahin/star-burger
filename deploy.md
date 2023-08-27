
https://dvmn.org/encyclopedia/deploy/systemd/

## copy files ssh from client to server

'sql[db.sqlite3](db.sqlite3)' , media/*.*

``
scp media/*.* root@195.80.50.84:/opt/star-burger/media
``

# If you have a ploblem with versoin node js :

'''
npm i --package-lock-only
npm audit fix
'''

### install parcel
```commandline
npm install --save-dev parcel
```
#### install depended packadge
```
cd star-burger
npm ci --dev
```

## Теперь запустите сборку фронтенда и не выключайте. Parcel будет работать в фоне и следить за изменениями в JS-коде:
#### Rebuild frontend
```sh

./node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"

```
```
✨  Built in 10.89s

```
```
python manage.py runserver 195.80.50.84:8000
```

## connect to server get folder with units
``
 cd /etc/systemd/system
 ``
#### make new file
```
nano star-burger.service

[Service]
ExecStart=/opt/star-burger/env/bin/python3 /opt/star-burger/python manage.py runserver 195.80.50.84:8000
Restart=always

[Install]
WantedBy=multi-user.target


```
## for example my bot:
```
 [Service]
 ExecStart=/opt/echobot/env/bin/python3 /opt/echobot/bot.py
 Restart=always

 [Install]
 WantedBy=multi-user.target


```
## run unit
``
```
systemctl daemon-reload

systemctl start star-burger

systemctl status star-burger
```
#### star-burger.service
*******************************************************************
```
[Service]
User=root
ExecStart=/opt/star-burger/env/bin/python /opt/star-burger/manage.py runserver 195.80.50.84:8000

[Install]
WantedBy=multi-user.target
```
*******************************************************************

## Чтобы автоматически запускать службу при загрузке системы, выполните команду
```
sudo systemctl enable star-burger

sudo systemctl disable star-burger

sudo systemctl start star-burger

sudo systemctl stop star-burger

sudo systemctl status star-burger

```

## Help

```commandline
https://4te.me/post/shpargalka-systemd/
```

## WSGI — это стандарт взаимодействия между Python-скриптом и веб-сервером

## Gunicorn — это веб-сервер с поддержкой стандарта WSGI
```commandline
pip install gunicorn
```

(env) root@1497089-zapivahin:/opt/star-burger# nano server.py

 gunicorn -b 195.80.50.84:8080 server:process_http_request

server — название вашего скрипта без .py, а process_http_request — название функции.
Так вы укажете Gunicorn, где искать функцию,

## create file
```getip.service

[Unit]
Description=GetIP site

[Service]
Type=simple
WorkingDirectory=/opt/star-burger
ExecStart=gunicorn -b 195.80.50.84:8080 server:process_http_request
Restart=always

[Install]
WantedBy=multi-user.target

```
## N воркеров = Количество ядер x 2 + 1
```commandline
nproc
```
#### настройка производительности
колво ядер * 2 + 1
[Service]
Type=simple
WorkingDirectory=/opt/star-burger
ExecStart=gunicorn -w 3 -b 195.80.50.84:8080 server:process_http_request
Restart=always

## server — название вашего скрипта без .py, а process_http_request — название функции.
#### server.py - def process_http_request(environ, start_response):


## запуск проекта на джанго
## star-burger.service

[Unit]
Description=StarBurger site

[Service]
Type=simple
WorkingDirectory=/opt/star-burger
ExecStart=/opt/star-burger/env/bin/gunicorn -w 3 -b 195.80.50.84:8080 star_burger.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target

## nginx default nano /etc/nginx/sites-enabled/default

server {
    listen 195.80.50.84:80;
  location / {
    include '/etc/nginx/proxy_params';
    proxy_pass http://127.0.0.1:8000/;
  }
  location /static/ {
    root '/opt/star-burger/';
  }
  location /media/ {
    root '/opt/star-burger/';
  }

server {
    listen 195.80.50.84:80;
  location / {
    include '/etc/nginx/proxy_params';
    proxy_pass http://127.0.0.1:8000/;
  }
  location /static/ {
    root '/opt/star-burger/';
  }
  location /media/ {
    root '/opt/star-burger/';
  }



##  star-burger.service nano /etc/systemd/system/star-burger.service
[Unit]
Description=StarBurger site

[Service]
Type=simple
WorkingDirectory=/opt/star-burger
ExecStart=/opt/star-burger/env/bin/gunicorn -w 3 -b 127.0.0.1:8000 star_burger.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target

## https://app.rollbar.com/a/zapivahin/projects

## Postgres SQL
DROP DATABASE starburger;

\l

sudo apt update
sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib
sudo -u postgres psql
CREATE DATABASE starburger;
CREATE USER admin WITH PASSWORD 'qazwsx';
ALTER ROLE admin SET client_encoding TO 'utf8';
ALTER ROLE admin SET default_transaction_isolation TO 'read committed';
ALTER ROLE admin SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE starburger TO admin;
\q
source env/bin/activate

#### settings.py

# Database
## 1 upload data from db sql - python manage.py dumpdata > db.json
## ./manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json
####
```commandline
python manage.py dumpdata --natural-primary --exclude auth.permission --exclude contenttypes --indent 4 > db.json

python manage.py loaddata db.json

```

## 2 change setting
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:////{0}'.format(os.path.join(BASE_DIR, 'db.sqlite3'))
    )
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'starburger',
        'USER': 'admin',
        'PASSWORD': 'qazwsx',
        'HOST': 'localhost',
        'PORT': '',
    }
}


## 3
#### migrate , if you have errors - del all migrations and made new one.

## load data - python manage.py loaddata db.json

## cd /etc/nginx/sites-available/

https://www.8host.com/blog/poluchenie-ssl-sertifikatov-s-pomoshhyu-certbot/

https://certbot.eff.org/instructions?ws=nginx&os=ubuntufocal

nano 1497089-zapivahin.tw1.ru

sudo snap install --classic certbot

sudo ln -s /snap/bin/certbot /usr/bin/certbot

sudo certbot --nginx

server {
  listen 80;
  server_name 1497089-zapivahin.tw1.ru;
  add_header X-Frame-Options “Star Burger”;
  location / {
    include '/etc/nginx/proxy_params';
    proxy_pass http://127.0.0.1:8000/;
  }
  location /static/ {
    root '/opt/star-burger/';
  }
  location /media/ {
    root '/opt/star-burger/';
  }
## http 80 it is work
server {
  listen 80;
  server_name 1497089-zapivahin.tw1.ru;
  add_header X-Frame-Options “Star Burger”;
  location / {
    include '/etc/nginx/proxy_params';
    proxy_pass http://127.0.0.1:8000/;
  }
  location /static/ {
    root '/opt/star-burger/';
  }
  location /media/ {
    root '/opt/star-burger/';
  }
## HTTPS ssl 443 2 files
#### nano /etc/nginx/sites-available/1497089-zapivahin.tw1.ru
#### nano /etc/nginx/sites-enabled/1497089-zapivahin.tw1.ru

upstream website {
    server web:8000;
}

server {
    listen 80;
    server_tokens off;
    server_name *.1497089-zapivahin.tw1.ru 1497089-zapivahin.tw1.ru;
    charset     utf8;
    autoindex   off;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}


server {
  listen 443 ssl;
  server_name 1497089-zapivahin.tw1.ru;
  server_tokens off;
  add_header X-Frame-Options “Star Burger”;

  ssl_certificate /etc/letsencrypt/live/1497089-zapivahin.tw1.ru/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/1497089-zapivahin.tw1.ru/privkey.pem;
  include /etc/letsencrypt/options-ssl-nginx.conf;
  ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

  location / {
    include '/etc/nginx/proxy_params';
    proxy_pass http://127.0.0.1:8000/;
  }
  location /static/ {
    root '/opt/star-burger/';
  }
  location /media/ {
    root '/opt/star-burger/';
  }







## bash

https://selectel.ru/blog/tutorials/linux-bash-scripting-guide/

https://linuxcookbook.ru/articles/komanda-curl-linux

https://docs.rollbar.com/docs/bash

curl -H "X-Rollbar-Access-Token: 11e6490dd241478dbda78a15a874db0a" -H "Content-Type: application/json" -X POST 'https://api.rollbar.com/api/1/deploy' -d '{"environment": "Star_burger", "revision": "dc1f74dee5", "rollbar_name": "zapivahin", "local_username": "circle-ci", "comment": "test deployment", "status": "succeeded"}'

last_commit=$(git rev-parse HEAD);


## python manage.py  clearsessions
#### clearsessions-burger.service
*******************************************************************
```
[Service]
User=root
ExecStart=/opt/star-burger/env/bin/python /opt/star-burger/manage.py clearsessions

[Install]
WantedBy=multi-user.target
```
*******************************************************************

## systemd-run --on-active="24h 00m" --unit star-burger-clear.service


## install Postrege



1 check or install    https://brew.sh/index_ru

#		/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

2 install server DB https://formulae.brew.sh/formula/postgresql@14

#		brew install postgresql@14

3 start server - restart `restart`

#		brew services restart postgresql@14

4 look at brew

#		brew info postgresql@14

44 Create db burger owner mihailzapivahin
	1 psql -d template1
	2 CREATE DATABASE burger WITH OWNER mihailzapivahin ENCODING 'UTF8';

5 look at list of databases

#		psql -l
                                      List of databases
   Name    |      Owner      | Encoding | Collate | Ctype |          Access privileges
-----------+-----------------+----------+---------+-------+-------------------------------------
 dbtest    | mihailzapivahin | UTF8     | C       | C     |
 postgres  | mihailzapivahin | UTF8     | C       | C     |
 template0 | mihailzapivahin | UTF8     | C       | C     | =c/mihailzapivahin                 +
           |                 |          |         |       | mihailzapivahin=CTc/mihailzapivahin
 template1 | mihailzapivahin | UTF8     | C       | C     | =c/mihailzapivahin                 +
           |                 |          |         |       | mihailzapivahin=CTc/mihailzapivahin

6 connect to db `dbtest`  (result: `dbtest=# `)

#		sudo psql -U mihailzapivahin -d dbtest


7 list tables of database

#		\dt+

                                         List of relations
 Schema |  Name   | Type  |      Owner      | Persistence | Access method |    Size    | Description
--------+---------+-------+-----------------+-------------+---------------+------------+-------------
 public | cities  | table | mihailzapivahin | permanent   | heap          | 8192 bytes |
 public | weather | table | mihailzapivahin | permanent   | heap          | 8192 bytes |
(2 rows)


8 query:  `SELECT * FROM weather;`

     city      | temp_lo | temp_hi | prcp |    date
---------------+---------+---------+------+------------
 San Francisco |      46 |      50 | 0.25 | 1994-11-27
 San Francisco |      43 |      57 |    0 | 1994-11-29
(2 rows)

Insert `INSERT INTO weather (city, temp_lo, temp_hi, prcp, date)
    VALUES ('San Francisco', 43, 57, 0.0, '1994-11-29');

































