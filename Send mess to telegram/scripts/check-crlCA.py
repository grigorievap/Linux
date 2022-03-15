#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests, re, subprocess, configparser, socket
from dateutil.parser import parse
from datetime import datetime

# Переменные
workpath = '/opt/scripts/'
conf = workpath + 'config.ini'
#crlfile = r"/etc/openvpn/crl.pem"
# Настройка конфига приложение + получение данных из конфиг-файла (config.ini)
config = configparser.ConfigParser()
config.read(conf, encoding = 'utf-8-sig')
crlfile = str(config.get('Vars', 'crl'))
# аргументы
args = ["openssl", "crl", "-inform", "PEM", "-in", crlfile, "-text", "-noout"]
# Получаем инфу из списка отзыва
output = subprocess.check_output(args)
# Поиск даты, до которой действует файлик
q = re.findall('Next Update[a-zA-Z0-9\:\s]+ GMT', output)
dt = parse('\n'.join(q).replace('Next Update:', '')).replace(tzinfo=None)
now = datetime.now().replace(tzinfo=None)
nucrlday = (dt - now).days

def format_txt():
    if nucrlday%10 == 1 and (not nucrlday%100 == 11):
        txt = 'день'
    elif (nucrlday%10 == 2 or nucrlday%10 == 3 or nucrlday%10 == 4) and (not nucrlday%100 == $
        txt = 'дня'
    else:
        txt = 'дней'
    return txt

def send_mess_tg(emotxt):
    txt = format_txt()
    emo = (config.get('Emoji', emotxt)).encode('utf-8')
    token = str(config.get('Telegram', 'tg_token_mytestit_bot'))
    chat_id = str(config.get('Telegram', 'tg_chat_id_my'))
    fqdn = socket.getfqdn()
    ip_address = socket.gethostbyname(fqdn)
    message = """
{0} {1}: Скоро истекает файл отзыва сертефикатов *crl.pem*
Осталось: *{2}* {3}
Server name: *{4}*
IP server: *{5}*
""".format(emo, emotxt, nucrlday, txt, fqdn, ip_address)
    URLFull = "https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}&parse_mode=ma$
    req = requests.get(URLFull, timeout=(3, 3))

if nucrlday < 5:
    emotxt = 'DISASTER'
    send_mess_tg(emotxt)
elif nucrlday < 30:
    emotxt = 'WARNING'
    send_mess_tg(emotxt)
elif nucrlday < 180:
    emotxt = 'INFORMATION'
    send_mess_tg(emotxt)
