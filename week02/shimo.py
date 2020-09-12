import json
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')
TIME_OUT = 10

# 无头模式
option = webdriver.ChromeOptions()
option.add_argument('--headless')
browser = webdriver.Chrome(options=option)
wait = WebDriverWait(browser, TIME_OUT)


def load_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config


def shimo_login(login_url, condition, Locator, config):
    logging.info(f'loginging {login_url}...')
    try:
        browser.get(login_url)
        wait.until(condition(Locator))
        input_email = browser.find_element_by_name('mobileOrEmail')
        input_email.send_keys(config['mobile'])
        input_pwd = browser.find_element_by_name('password')
        input_pwd.send_keys(config['pwd'])
        WebDriverWait(browser, 5)
        current_url = browser.current_url
        cookies = browser.get_cookies()
    except TimeoutError:
        logging.error('error occurred while logining {login_url}',
                      exc_info=True)
    return current_url, cookies


if __name__ == '__main__':
    login_url = 'https://shimo.im/login?from=home'
    config = load_config()
    try:
        current_url, cookies = shimo_login(
            login_url,
            condition=EC.visibility_of_element_located,
            Locator=(By.CSS_SELECTOR, '#root .main'),
            config=config)
    finally:
        browser.close()
    print(f'current_url: {current_url}')
    print(f'cookies: {cookies}')