from ping3 import ping
from time import sleep
import telebot
from datetime import datetime
import configparser
import os.path


def append_log(text, filename):  # Пишем логи
    try:
        with open(filename, 'a+') as log1:  # Открываем файл, если его нет - создаем (нужны права на запись)
            log1.write(f'{text} \n')  # Добавляем строку с указанным текстом (передается во время входа в функцию)
    except:
        print('Не удается создать или открыть лог-файл. Проверьте права на чтение и запись, также проверьте '
              'корректность пути к лог-файлу в файле конфигурации')
        raise SystemExit


if os.path.isfile('config.cfg'):  # Проверяем, существует ли конфиг-файл
    pass  # Если есть - идем дальше
else:
    print('Не обнаружен файл конфигурации')
    raise SystemExit  # Если нет - выводим ошибку и закрываем программу

try:
    config = configparser.ConfigParser()  # Парсим конфиг-файл
    config.read('config.cfg')  # Считываем конфиг-файл
    ips_cfg = config.defaults()  # Переносим список IP в словарь
    chat_id = config['tlgrm']['chat_id']  # Берем chat-id из конфиг-файла
    bot = telebot.TeleBot(config['tlgrm']['tlg_bot'])  # Идентификатор бота из конфига
except:
    print('Невозможно прочитать файл конфигурации. Возможно нарушена структура.')
    raise SystemExit

ips = {}  # Создаем пустой словарь
for ip in ips_cfg:  # Добавляем в пустой словарь значения из конфига + состояние последнего опроса, во избежание флуда
    addr = ips_cfg[ip].split('.')  # Валидация IP
    for i in addr:
        if int(i) < 0 or int(i) > 255:
            print('В списке для опроса указан неверный IP-адрес')
            raise SystemExit  # Если IP кривой - ошибка и закрываемся
    ips[ip] = [ips_cfg[ip], 0]  # Значение ключа в виде списка, IP + состояние последнего опроса

state = True  # Пока True - скрипт работает.
while state:
    for i in ips:  # Перебираем словарь ips. 1 итерация - 1 хост
        response = ping(ips[i][0])  # Проверяем, есть ли пинг до ресурса
        if isinstance(response, float) and ips[i][1] == 1:  # Если хост до этого не пинговался и ожил:
            try:
                bot.send_message(chat_id, f'Связь с хостом {i} восстановилась')  # Пишем в телегу
            except:
                print('Не удается отправить сообщение в Telegram')
            append_log(f'{datetime.now()}: Связь с хостом {i} восстановилась', config['other']['log_file'])  # Лог
            ips[i][1] = 0  # Ставим признак живого хоста
        if (response is None or response is False) and ips[i][1] == 0:  # Если хост до этого пинговался но перестал:
            response2 = ping(ips[i][0])  # Проверяем еще раз, на всякий
            if response2 is None or response2 is False:  # Если и во второй раз не ответил:
                response3 = ping(ips[i][0])  # Проверяем в последний раз, для верности
                if response3 is None or response3 is False:  # Если и в 3 раз не ответил:
                    ips[i][1] = 1  # Добавляем признак отвала хоста
                    try:
                        bot.send_message(chat_id, f'Связь с хостом {i} пропала')  # Пишем в телегу
                    except:
                        print('Не удается отправить сообщение в Telegram')
                    append_log(f'{datetime.now()}: Связь с хостом {i} пропала', config['other']['log_file'])  # Лог
    try:
        sleep(int(config['other']['delay']))  # Делаем паузу (в секундах, из конфига)
    except ValueError:
        print('Указан некорректный параметр задержки между опросами в конфигурационном файле')
        raise SystemExit

