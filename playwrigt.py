from playwright.sync_api import sync_playwright
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
import random
import time
class DeadNetManager:
    def __init__(self):
        self.debug = False
        self.proxies = [
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
        self.use_proxy = True
        self.current_proxy_service = "https://example.com"  # Замените на ваш URL
        self.viewers_count = 20  # Количество зрителей
        self.twitch_username = "lobotomite55"  # Замените на нужное имя

    def get_random_proxy(self, i):
        proxy = self.proxies[i].split(':')
        return {
            "server": f"{proxy[0]}:{proxy[1]}",
            "username": proxy[2],
            "password": proxy[3],
        }

    def setup_viewers(self):
        with sync_playwright() as p:
            browser_options = [
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--no-first-run",
                "--disable-blink-features=AutomationControlled",
                "--mute-audio",
                "--webrtc-ip-handling-policy=disable_non_proxied_udp",
                "--force-webrtc-ip-handling-policy",
            ]
            if(not self.debug):
                browser_options.append('--headless')

            contexts = []  # Список для хранения экземпляров браузеров
            browser = p.firefox.launch(
                channel="firefox",
                headless=False,
                args=browser_options
            )
            with Progress(SpinnerColumn(), BarColumn(), TextColumn("[progress.description]{task.description}")) as progress:
                task = progress.add_task("Сетап зрителей...", total=self.viewers_count)

                for _ in range(self.viewers_count):
                    print(_)
                    # Запуск нового браузера с уникальным прокси
                    try:
                        proxy = self.get_random_proxy(_) if self.use_proxy else None


                        context = browser.new_context(
                            viewport={"width": 1920, "height": 1080},
                            proxy=proxy if proxy else None
                        )
                        contexts.append(context)  # Сохраняем экземпляр браузера в список

                        page = context.new_page()

                        # Удаление автоматизации
                        page.evaluate('''() => {
                                                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                                                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                                                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
                                            }''')

                        page.goto(f'https://www.twitch.tv/{self.twitch_username}', wait_until='domcontentloaded',
                                  timeout=0)

                        progress.update(task, advance=1)  # Обновляем прогресс
                    except Exception as e:
                        print(e)
                        continue

            # Браузеры останутся открытыми после завершения скрипта
            print("Все браузеры открыты. Нажмите Enter для завершения.")
            input()  # Ожидание ввода от пользователя, чтобы завершить работу

            # Закрытие всех браузеров, когда пользователь готов
            for browser in browsers:
                browser.close()

# Пример использования
if __name__ == "__main__":
    manager = DeadNetManager()
    manager.setup_viewers()
