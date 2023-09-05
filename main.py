import concurrent.futures
import random
import string
import time

import tls_client
from tls_client import Session
from colorama import Fore, Style, Back

import dtypes


class Joiner:


    with open("proxies.txt") as prueba:
        lineas = prueba.readlines()
        random_proxy = random.choice(lineas)

    prueba_session = Session(
        client_identifier="opera_90",
        random_tls_extension_order=True
    )
    
    prueba_session.proxies = {
        "http": "http://" + random_proxy,
        "https": "http://" + random_proxy
    }

    counter = 0
    def __init__(self, data: dtypes.Instance) -> None:
        self.prueba_session = data.client
        self.prueba_session.headers = data.headers
        self.get_cookies()
        self.instance = data

    def rand_str(self, length: int) -> str:
        return ''.join(random.sample(string.ascii_lowercase + string.digits, length))

    def get_cookies(self) -> None:
        site = self.prueba_session.get("https://discord.com")
        self.prueba_session.cookies = site.cookies

    def join(self) -> None:
        self.prueba_session.headers.update({"Authorization": self.instance.token})
        result = self.prueba_session.post(f"https://discord.com/api/v9/invites/{self.instance.invite}", json={
            'session_id': self.rand_str(32),
        })

        if result.status_code == 200:
            Joiner.counter += 1
            logger.printk(logger.color('green', f'[{Joiner.counter}] Joined server: {result.status_code}'))
            time.sleep(2)

        elif result.status_code == 429:
            logger.printk(logger.color('yellow', "Got captcha, sleeping for 10 seconds..."))
            time.sleep(10)

        elif result.status_code == 400:
            logger.printk(logger.color('blue', f"Got cap/ratelimit, sleeping for 20 seconds... {status_code}"))
            time.sleep(20)

        elif result.status_code == 404:
            logger.printk(logger.color('blue', f"Got cap/ratelimit, sleeping for 20 seconds... {status_code}"))
            time.sleep(20)
        
        else:
            logger.printk(logger.color('red', result))
            time.sleep(2)
          

class logger:
    colors_table = {
        "green": Fore.GREEN,
        "red": Fore.RED,
        "yellow": Fore.YELLOW,
        "magenta": Fore.MAGENTA,
        "blue": Fore.BLUE,
        "cyan": Fore.CYAN,
        "gray": Fore.LIGHTBLACK_EX,
        "white": Fore.WHITE,
    }

    @staticmethod
    def printk(text) -> None:
        print(f"[>] {text}")

    @staticmethod
    def convert(color):
        return logger.colors_table[color]

    @staticmethod
    def color(opt, obj):
        return f"{logger.convert(opt)}{obj}{Style.RESET_ALL}"


class intilize:
    @staticmethod
    def start(i):
        Joiner(i).join()



if __name__ == '__main__':
    with open("tokens.txt") as token_file:
        tokens = [line.strip() for line in token_file]

    with open("invites.txt") as invite_file:
        invites = [line.strip() for line in invite_file]

    instances = []
    max_threads = 1

    for token_ in tokens:
        header = dtypes.OtherInfo.headers
        for invite in invites:
            instances.append(
                dtypes.Instance(
                    client=tls_client.Session(
                        client_identifier=f"chrome_{random.randint(110, 115)}",
                        random_tls_extension_order=True,
                    ),
                    token=token_,
                    headers=header,
                    invite=invite,
                )
            )

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        for i in instances:
            executor.submit(intilize.start, i)