Скрипт для мониторинга хостов (настройки берет из конфиг-файла, о нем чуть ниже). Список хостов может быть любой, вводить необходимо IP-адрес хоста. Если в процессе опроса хост не отвечает 3 раза подряд - срипт выставляет ему признак отвала и присылает уведомление в телеграм. Если связь восстановилась - также уведомляет об этом в Телеграм. Также пишет лог-файл, путь которого Вы можете указать в конфиге. Конфиг файл должен лежать рядом со скриптом, имя файла config.cfg.

Вот пример конфиг файла:

[DEFAULT]# Список хостов, может быть любым, просто меняете или добавляете новые. Имена должны быть уникальны!

host_name0 = 127.0.0.1

host_name1 = 192.168.0.1

host_name2 = 192.168.0.1

[tlgrm]

tlg_bot = сюда пишем ID бота, который вы получили от fatherBot

chat_id = Chat-ID, куда писать сообщения (у бота должен быть доступ к чату)

[other]

delay = 3 # в секундах, время между опросами хостов (цикличность опроса)

log_file = ./monitoring.log # путь, куда выкладывать лог. Если файла нет - создаст, но должны быть права на запись.
