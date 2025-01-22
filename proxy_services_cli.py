import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium_authenticated_proxy import SeleniumAuthenticatedProxy
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import random

with open('proxies.txt') as file:
    proxies = file.read().splitlines()

opened_tabs = 0
def get_random_proxy(i):
    global proxies
    proxy = proxies[i]
    proxy = proxy.split(':')
    return f"http://{proxy[2]}:{proxy[3]}@{proxy[0]}:{proxy[1]}"
    return {
        'http' : f"https://{proxy[2]}:{proxy[3]}@{proxy[0]}:{proxy[1]}",
        'https' : f"https://{proxy[2]}:{proxy[3]}@{proxy[0]}:{proxy[1]}"
    }

# Функция для открытия веб-страницы
def open_url(url, views_count, proxy_number):
    # Настройка драйвера
    try:
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920,1080")  # на серваке оставить вместе с хедлесс
        chrome_options.add_argument("--headless")  # на серваке оставить вместе с хедлесс
        chrome_options.add_argument(
            "start-maximized")  # Это раскомментировать при необходимости(тоже чтоб не делало мозг)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        proxy = get_random_proxy(proxy_number)
        print(proxy)
        #
        # chrome_options.add_argument(f"--proxy-server={proxy}")
        if ('@' in proxy):
            proxy_helper = SeleniumAuthenticatedProxy(proxy_url=proxy)
            proxy_helper.enrich_chrome_options(chrome_options)

        else:
            chrome_options.add_argument(f"--proxy-server={proxy}")

        chrome_options.add_argument(
            "--disable-blink-features=AutomationControlled")  # Нужно чтобы сайты типа днс не делали мозг
        # Enrich Chrome options with proxy authentication

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.set_window_position(-2000, 0)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",
                               {  # Нужно чтобы сайты типа днс не делали мозг
                                   'source': '''
                            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                      '''
                               })
        proxy_url = 'https://blockawayproxy.net/'
        driver.get(proxy_url)

        for j in range(views_count):
            # driver.execute_script("window.open('" + proxy_url + "')")
            # driver.switch_to.window(driver.window_handles[-1])
            driver.get(proxy_url)

            text_box = driver.find_element(By.ID, 'unique-form-control')
            text_box.send_keys(f'https://www.twitch.tv/thebiskvit')
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