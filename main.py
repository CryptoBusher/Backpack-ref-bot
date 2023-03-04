"""
Script for farming referrals on Backpack (https://twitter.com/xNFT_Backpack)
"""

from os.path import dirname, abspath
from sys import stderr
from time import sleep
from random import randint, sample
from string import ascii_lowercase, ascii_uppercase, digits
from multiprocessing.dummy import Pool

from loguru import logger
from pyfiglet import Figlet
from random_username.generate import generate_username
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config import *


logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <white>{message}</white>")

f = Figlet(font='5lineoblique')
print(f.renderText('Busher'),
      'Telegram channel: @CryptoKiddiesClub',
      'Telegram chat: @CryptoKiddiesChat',
      'Twitter: @CryptoBusher', sep='\n', end='\n\n')


class BackPackAccount:
    BACKPACK_EXT_PATH = f'{dirname(abspath(__file__))}\\backpack_0.5.1_0.crx'
    LINK_TO_EXT = 'chrome-extension://aflkmfhebedbjioipglgcbcmnbpgliof/options.html?onboarding=true'

    def __init__(self, ref_link: str, inv_code: str, username: str | None = None, _proxy: str | None = None):
        self.username = username
        self.ref_link = ref_link
        self.inv_code = inv_code
        self._proxy = _proxy
        self.password = self.__generate_password()
        self.driver = None
        self.seed = None

        if not self.username:
            self.__update_username()

    def __str__(self):
        return f'{self.username}|{self.seed}|{self.password}|{self._proxy}|{self.inv_code}|{self.ref_link}'

    @staticmethod
    def __generate_password() -> str:
        pass_length = randint(10, 15)
        return "".join(sample(ascii_lowercase + ascii_uppercase + digits, pass_length))

    def __create_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_extension(self.BACKPACK_EXT_PATH)

        sw_options = {}
        if self._proxy:
            sw_options['proxy'] = {
                    'http': f'{self._proxy}',
                    'https': f'{self._proxy}',
                    'no_proxy': 'localhost,127.0.0.1'
            }

        service = Service(executable_path='chromedriver.exe')
        driver = webdriver.Chrome(service=service, seleniumwire_options=sw_options, options=options)
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
                delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            """
        })

        self.driver = driver

    def __update_username(self):
        self.username = generate_username()[0]

    def save_account_data(self):
        with open(f'data/backup/{self.username}.txt', 'w') as _file:
            _file.write(f'{self.__str__()}')

    def register_account(self) -> bool:
        self.__create_driver()
        wait = WebDriverWait(self.driver, wait_element_sec)

        self.driver.get(self.ref_link)
        sleep(2)
        self.driver.get(self.LINK_TO_EXT)

        wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="inviteCode"]'))).send_keys(self.inv_code)
        wait.until(EC.presence_of_element_located((By.XPATH, '//button[@type="submit"]'))).click()
        username_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="username"]')))

        for _i in range(10):
            username_input.send_keys(self.username)
            wait.until(EC.presence_of_element_located((By.XPATH, '//button[@type="submit"]'))).click()
            try:
                WebDriverWait(self.driver, 3).until(EC.presence_of_element_located(
                    (By.XPATH, "//*[text()='Create a new wallet']"))).click()
                break
            except:
                if _i < 9:
                    username_input.send_keys(Keys.BACKSPACE * (len(self.username)))
                    self.__update_username()
                    continue
                else:
                    return False

        wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='Create with recovery phrase']"))).click()

        seed = ''
        for _i in range(8):
            word_input = wait.until(EC.presence_of_element_located((By.XPATH, f'//input[@id=":r{_i + 2}:"]')))
            seed += f'{word_input.get_property("value")} '
        for _i in ['a', 'b', 'c', 'd']:
            word_input = wait.until(EC.presence_of_element_located((By.XPATH, f'//input[@id=":r{_i}:"]')))
            seed += f'{word_input.get_property("value")} '

        self.seed = seed.rstrip()

        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='checkbox']"))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='Next']"))).click()

        sleep(1)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Ethereum']"))).click()
        sleep(1)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Solana']"))).click()
        sleep(1)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Next']"))).click()

        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']"))).send_keys(self.password)
        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[@name='password-confirmation']"))).send_keys(self.password)
        wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='checkbox']"))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='Next']"))).click()

        wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='Disable']"))).click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[text()='Visit xnft.gg']")))

        return True


def register_account(account_object: BackPackAccount):
    try:
        is_registered = account_object.register_account()
        if is_registered:
            logger.info(f'Registered account {account_object.username}')
            account_object.save_account_data()
        else:
            logger.error(f'Failed to register account {account_object.username}')
    except:
        logger.error(f'Failed to register account {account_object.username}')

    try:
        account_object.driver.close()
        account_object.driver.quit()
    except:
        pass


if __name__ == '__main__':
    with open('data/usernames.txt', 'r') as file:
        usernames = [line.rstrip() for line in file]
    with open('data/proxies.txt', 'r') as file:
        proxies = [line.rstrip() for line in file]

    backpack_account_objects = []
    for i in range(refs_to_register):
        proxy = None if len(proxies) == 0 else proxies.pop(0)
        if proxy:
            proxies.append(proxy)

        referral = referrals.pop(0)
        referrals.append(referral)

        backpack_account_objects.append(BackPackAccount(
            referral[0],
            referral[1],
            usernames[i] if len(usernames) > i else None,
            proxy
        ))

    with Pool(processes=threads) as executor:
        executor.map(register_account, backpack_account_objects)

    logger.info('Finished working')
