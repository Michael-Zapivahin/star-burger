
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

Теперь запустите сборку фронтенда и не выключайте. Parcel будет работать в фоне и следить за изменениями в JS-коде:

```sh
./node_modules/.bin/parcel watch bundles-src/index.js --dist-dir bundles --public-url="./"
```
```
✨  Built in 10.89s
```
```
python manage.py runserver 195.80.50.84:8000
```

connect to server get folder with units
``
 cd /etc/systemd/system
 ``
make new file
```
nano star-burger.service

[Service]
ExecStart=/opt/star-burger/env/bin/python3 /opt/star-burger/python manage.py runserver 195.80.50.84:8000
Restart=always

[Install]
WantedBy=multi-user.target


```
for example my bot:
```
 [Service]
 ExecStart=/opt/echobot/env/bin/python3 /opt/echobot/bot.py
 Restart=always

 [Install]
 WantedBy=multi-user.target


```
run unit
``
```
systemctl daemon-reload

systemctl start star-burger

systemctl status star-burger
```

*******************************************************************
[Service]
User=root
ExecStart=/opt/star-burger/env/bin/python /opt/star-burger/manage.py runserver 195.80.50.84:8000

[Install]
WantedBy=multi-user.target

*******************************************************************

Чтобы автоматически запускать службу при загрузке системы, выполните команду
```
sudo systemctl enable star-burger
```




```
systemctl daemon-reload

systemctl start star-burger

systemctl status star-burger
```

















