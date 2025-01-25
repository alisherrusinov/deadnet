import time
import requests
from fake_useragent import UserAgent
from stem import Signal
from stem.control import Controller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium_authenticated_proxy import SeleniumAuthenticatedProxy
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Tor proxies setup for HTTP and HTTPS
proxies = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}

print("Changing IP Address every 30 seconds...\n")

def get_driver(proxy):
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")  # на серваке оставить вместе с хедлесс
    chrome_options.add_argument("--headless")  # на серваке оставить вместе с хедлесс
    chrome_options.add_argument(
        "start-maximized")  # Это раскомментировать при необходимости(тоже чтоб не делало мозг)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
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

drivers = []
for i in range(10):
    try:
        # Random User-Agent for each request
        headers = {'User-Agent': UserAgent().random}

        # Connect to the Tor Controller and switch IP
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password='rrr565656')  # Ensure this is configured in torrc
            controller.signal(Signal.NEWNYM)
            print("Requested new IP...")

        # Wait for the Tor network to update the IP
        time.sleep(5)

        # Request the current IP address to verify the change
        response = requests.get('https://ident.me', proxies=proxies, headers=headers)
        print(f"Your IP is: {response.text} || User Agent: {headers['User-Agent']}")

    except requests.RequestException as req_err:
        print(f"Network error: {req_err}")

    except Exception as err:
        print(f"An error occurred: {err}")
