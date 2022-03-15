# Отправка сообщения об истечении сертификата в телеграм

- Создаем папку и помещаем туда скрипты и конфиг:
--check-crlCA.py
--check-letsencript.py
--config.ini
```
mkdir /opt/scripts
```

- в /usr/lib/systemd/system создаем сервисы
--check-crlCA.service
--check-crlCA.timer
--check-letsencript.service
--check-letsencript.timer

- релоадим демонов
```
sudo systemctl daemon-reload
```
