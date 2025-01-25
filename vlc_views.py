import os
import subprocess
import streamlink
from proxy_tools import proxy
import time
# URL трансляции Twitch
url = "https://www.twitch.tv/chocomi15"
proxies = [
            '185.125.219.205:16036:JyYVjnvfsq:qFjogpe0Yz',
            '81.177.22.35:11481:C2Ty3mjfaq:4jWAJXE6x1',
            '194.67.202.6:17107:N0JWUaqTOz:DLGty4xVi9',
            '193.0.202.136:25588:XWIO0Ui5tP:9rZcxVBo7j',
            '185.5.251.38:17036:IYMG2eSolE:8mporgw0xn',
            '185.5.251.17:24662:xn4UPL9l3A:gA8mTh2c7C',
            '92.63.202.139:22420:zoUNTutFEm:cFeQOMSXfI',
            '185.5.251.111:16201:ZmvaU0dc9n:DFcfaQ4iPR',
            '185.156.75.119:23670:ebYZsX8gof:wnI20lNte9',
            '45.153.74.241:11104:zbhTPqNA2H:dHOqkDaYhB',
            '45.81.136.75:5500:tkZs1O:9EiPbuqDPq',
            '45.81.136.241:5500:tkZs1O:9EiPbuqDPq',
            '188.130.187.31:5500:tkZs1O:9EiPbuqDPq',
            '188.130.129.186:5500:tkZs1O:9EiPbuqDPq',
            '109.248.12.44:5500:tkZs1O:9EiPbuqDPq',
            '188.130.136.140:5500:tkZs1O:9EiPbuqDPq',
            '188.130.142.111:5500:tkZs1O:9EiPbuqDPq',
            '46.8.222.126:5500:tkZs1O:9EiPbuqDPq',
            '46.8.17.165:5500:tkZs1O:9EiPbuqDPq',
            '109.248.204.47:5500:tkZs1O:9EiPbuqDPq',
        ]

with open('working_proxies.txt') as f:
    free_proxies = f.readlines()

def get_random_proxy(i):
    proxy = proxies[i].split(':')
    return f"http://{proxy[2]}:{proxy[3]}@{proxy[0]}:{proxy[1]}"

def get_free_proxy(i):
    proxy = free_proxies[i]
    return f"http://{proxy}"
# Получаем список доступных потоков со стрима
streams = streamlink.streams(url)

print(streams)
input()
# Проверяем, доступен ли поток 160p30
stream_quality = "160p"
pids = []
for i in range(30):
    if stream_quality in streams:
        # Получаем URL потока
        stream_url = streams[stream_quality].url

        # Настройки прокси
        proxy_server = get_free_proxy(i)
        print(proxy_server)
        http_proxy = f"--http-proxy={proxy_server}"
        # # Настройки прокси
        # os.environ['http_proxy'] = proxy_server # Замените на ваш прокси-сервер
        # os.environ['https_proxy'] = proxy_server # Замените на ваш прокси-сервер
        config = '--config=/home/alisher/.config/streamlink/config' #- эксперимент
        # Открываем поток в фоновом режиме с помощью VLC с использованием прокси
        process_1 = subprocess.Popen(
            ['streamlink', http_proxy, config,  url, '160p'])  # Замените 'vlc' на путь к вашему медиаплееру, если необходимо
        pids.append(process_1.pid)
        time.sleep(1)
    else:
        print(f"Поток {stream_quality} недоступен.")

input("Нажмите Enter для закрытия всех экземпляров VLC...")
#nircmd
# Завершаем процессы
for pid in pids:
    try:
        os.kill(pid, 9)  # SIGKILL для завершения процесса
        print(f"Процесс с PID {pid} завершен.")
    except OSError as e:
        print(f"Ошибка при завершении процесса с PID {pid}: {e}")
