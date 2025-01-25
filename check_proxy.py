import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


def check_proxy(proxy):
    # Укажите URL для проверки, например, http://httpbin.org/ip
    url = "https://www.twitch.tv/"

    # Настройки прокси
    proxies = {
        "http": proxy.strip(),  # Удаляем лишние пробелы
        "https": proxy.strip(),
    }

    try:
        # Выполняем запрос через прокси
        response = requests.get(url, proxies=proxies, timeout=5)

        # Проверяем статус-код ответа
        if response.status_code == 200:
            return proxy.strip()  # Возвращаем рабочий прокси
        else:
            print(f"Прокси {proxy.strip()} не работает. Статус-код:", response.status_code)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при подключении к прокси {proxy.strip()}:", e)


def main():
    with open(' free_proxies.txt') as f:
        free_proxies = f.readlines()

    working_proxies = []

    # Используем ThreadPoolExecutor для многопоточной проверки прокси
    with ThreadPoolExecutor(max_workers=100) as executor:  # Вы можете изменить max_workers по вашему усмотрению
        future_to_proxy = {executor.submit(check_proxy, proxy): proxy for proxy in free_proxies}

        for future in as_completed(future_to_proxy):
            result = future.result()
            if result:
                working_proxies.append(result)

    with open('working_proxies.txt', 'w') as f:
        for proxy in working_proxies:
            f.write(proxy + '\n')


if __name__ == "__main__":
    main()
