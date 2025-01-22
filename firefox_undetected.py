import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from undetected_geckodriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random



opened_tabs = 0

# Функция для открытия веб-страницы
def open_url(url, views_count, proxy_number):
    # Настройка драйвера
    try:

        proxy_url = 'https://blockawayproxy.net/'
        driver = Firefox()
        driver.get(proxy_url)

        for j in range(views_count):
            # driver.execute_script("window.open('" + proxy_url + "')")
            # driver.switch_to.window(driver.window_handles[-1])
            driver.get(proxy_url)

            text_box = driver.find_element(By.ID, 'unique-form-control')
            text_box.send_keys(f'https://www.twitch.tv/dldkcc')
            text_box.send_keys(Keys.RETURN)
            time.sleep(10)
        print('Боты отправлены')
        time.sleep(1000)
    except Exception as e:
        print(e)
        # driver.quit()

    # Здесь вы можете добавить дополнительные действия с веб-страницей
    # Например, ожидание, взаимодействие и т.д.
    # driver.quit()  # Закрываем браузер после выполнения действий

# Основная часть кода
if __name__ == "__main__":
    url = 'https://blockawayproxy.net/'  # Замените на нужный URL
    threads = []

    for i in range(10):
        thread = threading.Thread(target=open_url, args=(url,5, i))
        threads.append(thread)
        thread.start()

    # Ждем завершения всех потоков
    for thread in threads:
        thread.join()
        # 41