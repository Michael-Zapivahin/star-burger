
https://dvmn.org/encyclopedia/deploy/systemd/

## copy files ssh from client to server

'sql[db.sqlite3](db.sqlite3)' , media/*.*

``
scp media/*.* root@195.80.50.84:/opt/star-burger/media
``

#### install depended packadge
```
cd star-burger
npm ci --dev
```

# If you have a ploblem with versoin node js :

'''
npm i --package-lock-only
npm audit fix
'''

## Теперь запустите сборку фронтенда и не выключайте. Parcel будет работать в фоне и следить за изменениями в JS-коде:

```sh
./node_modules/.bin/parcel watch bundles-src/index.js --dist-dir bundles --public-url="./"
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























