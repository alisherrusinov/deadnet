import random

import inquirer
from art import text2art
from rich.console import Console
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium_authenticated_proxy import SeleniumAuthenticatedProxy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from playwright.sync_api import sync_playwright
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
import time

class DeadNetManager:
    def __init__(self):
        self.debug = True

        self.proxies = [
            '45.153.74.241:11104:zbhTPqNA2H:dHOqkDaYhB',
            '185.125.219.205:16036:JyYVjnvfsq:qFjogpe0Yz',
            '81.177.22.35:11481:C2Ty3mjfaq:4jWAJXE6x1',
            '194.67.202.6:17107:N0JWUaqTOz:DLGty4xVi9',
            '193.0.202.136:25588:XWIO0Ui5tP:9rZcxVBo7j',
            '185.5.251.38:17036:IYMG2eSolE:8mporgw0xn',
            '185.5.251.17:24662:xn4UPL9l3A:gA8mTh2c7C',
            '92.63.202.139:22420:zoUNTutFEm:cFeQOMSXfI',
            '185.5.251.111:16201:ZmvaU0dc9n:DFcfaQ4iPR',
            '185.156.75.119:23670:ebYZsX8gof:wnI20lNte9'
        ]
        self.use_proxy = False

        self.console = Console()
        self.greeting()
        self.use_proxy = self.use_proxy_choice()
        self.current_proxy_service = self.proxy_service_choice()
        self.viewers_count = self.viewers_count_choice()
        self.twitch_username = self.nickname_choice()
        self.setup_viewers()
    def greeting(self):
        ascii_art = text2art("DeadNet", font='block')
        self.console.print(ascii_art, justify="center", style='bold red', highlight=False)
        print('Примерное кпд - 50%(на ластовом сервисе)')

    def setup_viewers(self):
        with sync_playwright() as p:
            browser_options = [
                "--headless",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--no-first-run",
                "--disable-blink-features=AutomationControlled",
                "--mute-audio",
                "--webrtc-ip-handling-policy=disable_non_proxied_udp",
                "--force-webrtc-ip-handling-policy",
            ]

            with Progress(SpinnerColumn(), BarColumn(), TextColumn("[progress.description]{task.description}")) as progress:
                task = progress.add_task("Сетап зрителей...", total=self.viewers_count)

                for _ in range(self.viewers_count):
                    # Запуск нового браузера с уникальным прокси
                    proxy = self.get_random_proxy() if self.use_proxy else None
                    browser = p.chromium.launch(
                        channel="chrome",
                        headless=False,
                        args=browser_options
                    )

                    context = browser.new_context(
                        viewport={"width": 1920, "height": 1080},
                        proxy={"server": proxy} if proxy else None
                    )
                    page = context.new_page()

                    # Удаление автоматизации
                    page.evaluate('''() => {
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                    }''')

                    page.goto(f'www.twitch.tv/{self.twitch_username}')

                    # # Заполнение поля URL
                    # id = 'url' if self.current_proxy_service != 'https://blockawayproxy.net/' else 'unique-form-control'
                    # text_box = page.locator(f'#{id}')
                    #
                    # try:
                    #     text_box.fill()
                    # except:
                    #     access_button = page.locator(".fc-cta-consent")
                    #     access_button.click()
                    #     time.sleep(2)
                    #     text_box.fill(f'www.twitch.tv/{self.twitch_username}')
                    #
                    # text_box.press('Enter')
                    progress.update(task, advance=1)  # Обновляем прогресс

                    # Ожидание, чтобы браузер не закрывался сразу
                    time.sleep(5)  # Замените на нужное время ожидания

            # Переключение между вкладками (если нужно)
            # Этот код можно добавить, если вам нужно переключаться между вкладками
            # while True:
            #     for new_page in browser.contexts[0].pages:
            #         new_page.bring_to_front()  # Переключаемся на вкладку
            #     time.sleep(30)

    def get_random_proxy(self):
        proxy = random.choice(self.proxies).split(':')
        return f"http://{proxy[2]}:{proxy[3]}@{proxy[0]}:{proxy[1]}"

    def proxy_service_choice(self):
        proxy_servers = {
            0: "https://blockawayproxy.net/",
            1: "https://www.blockaway.net",
            2: "https://www.croxyproxy.com",
            3: "https://www.croxyproxy.rocks",
            4: "https://www.croxy.network",
            5: "https://www.croxy.org",
            6: "https://www.youtubeunblocked.live",
            7: "https://www.croxyproxy.net",
        }
        # Список вариантов для выбора
        questions = [
            inquirer.List('choice',
                          message="Какой прокси сервис юзать?",
                          choices=list(proxy_servers.values()),
                          ),
        ]

        # Получение ответа
        answer = inquirer.prompt(questions)
        return answer['choice']

    def use_proxy_choice(self):
        # Список вариантов для выбора
        questions = [
            inquirer.List('choice',
                          message="Юзать прокси?",
                          choices=['Нет', 'Да'],
                          ),
        ]

        # Получение ответа
        answer = inquirer.prompt(questions)
        return answer['choice'] == 'Да'

    def viewers_count_choice(self):
        questions = [
            inquirer.Text('choice',
                          message="Сколько просмотров накрутить?",
                          ),
        ]

        # Получение ответа
        answer = inquirer.prompt(questions)
        return int(answer['choice'])

    def nickname_choice(self):
        questions = [
            inquirer.Text('choice',
                          message="Введите ник на твиче",
                          ),
        ]

        # Получение ответа
        answer = inquirer.prompt(questions)
        return answer['choice']

if __name__ == "__main__":
    manager = DeadNetManager()
