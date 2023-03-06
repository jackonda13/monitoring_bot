from ping3 import ping
from time import sleep
import telebot
from datetime import datetime
import configparser


def append_log(text, filename):  # Пишем логи
    with open(filename, 'a+') as log1:  # Открываем файл, если его нет - создаем (нужны права на запись)
        log1.write(f'{text} \n')  # Добавляем строку с указанным текстом (передается во время входа в функцию)


config = configparser.ConfigParser()  # Парсим конфиг-файл
config.read('config.cfg')  # Считываем конфиг-файл
ips_cfg = config.defaults()  # Переносим список IP в словарь
chat_id = config['tlgrm']['chat_id']  # Берем chat-id из конфиг-файла
bot = telebot.TeleBot(config['tlgrm']['tlg_bot'])  # Идентификатор бота из конфига
ips = {}  # Создаем пустой словарь
for ip in ips_cfg:  # Добавляем в пустой словарь значения из конфига + состояние последнего опроса, во избежание флуда
    ips[ip] = [ips_cfg[ip], 0]  # Значение ключа в виде списка, IP + состояние последнего опроса

state = True  # Пока True - скрипт работает.
while state:
    for i in ips:  # Перебираем словарь ips. 1 итерация - 1 хост
        response = ping(ips[i][0])  # Проверяем, есть ли пинг до ресурса
        if isinstance(response, float) and ips[i][1] == 1:  # Если хост до этого не пинговался и ожил:
            bot.send_message(chat_id, f'Связь с хостом {i} восстановилась')  # Пишем в телегу
            append_log(f'{datetime.now()}: Связь с хостом {i} восстановилась', config['other']['log_file'])  # Пишем лог
            ips[i][1] = 0  # Ставим признак живого хоста
        if (response is None or response is False) and ips[i][1] == 0:  # Если хост до этого пинговался но перестал:
            response2 = ping(ips[i][0])  # Проверяем еще раз, на всякий
            if response2 is None or response2 is False:  # Если и во второй раз не ответил:
                response3 = ping(ips[i][0])  # Проверяем в последний раз, для верности
                if response3 is None or response3 is False:  # Если и в 3 раз не ответил:
                    ips[i][1] = 1  # Добавляем признак отвала хоста
                    bot.send_message(chat_id, f'Связь с хостом {i} пропала')  # Пишем в телегу
                    append_log(f'{datetime.now()}: Связь с хостом {i} пропала', config['other']['log_file'])  # В лог
    sleep(int(config['other']['delay']))  # Делаем паузу (в секундах, из конфига)
