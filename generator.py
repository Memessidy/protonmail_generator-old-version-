from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
from pynput.keyboard import Controller
from selenium.webdriver.support import expected_conditions as EC
import random
from generate_random import generate_password

from guerrilla import get_guerrilla_mail
from maildrop import MailDrop


def new_protonmail(use_capcha=False, sleeping_time_max=10, min_sleeping_time=5, temporary_mail='guerilla'):
    # options = Options()
    # options.add_argument('--allow-running-insecure-content')
    # options.add_argument('--ignore-certificate-errors')

    # desired_capabilities = DesiredCapabilities().CHROME.copy()
    # desired_capabilities['acceptInsecureCerts'] = True
    # caps = DesiredCapabilities.CHROME.copy()
    # caps["goog:loggingPrefs"] = {"performance": "ALL"}  # enable performance logs
    # options = webdriver.ChromeOptions()
    # options.add_argument('--proxy-server=HOST:PORT')

    random_time_range = (min_sleeping_time, sleeping_time_max)

    options = Options()
    options.set_capability('acceptInsecureCerts', True)

    # test in current session
    # options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(service=Service((ChromeDriverManager().install())), options=options)

    driver.implicitly_wait(5)
    keyboard = Controller()

    if temporary_mail == 'maildrop':
        domain = '@maildrop.cc'
    elif temporary_mail == 'guerrilla':
        domain = '@guerrillamail.com'
    else:
        print('no such mail..')
        return
    url = 'https://account.proton.me/signup?plan=free&billing=12&ref=prctbl&minimumCycle=1' \
          '2&currency=EUR&product=mail&language=en'

    capitalized = bool(random.getrandbits(1))
    user = generate_password(10, 26).lower() if not capitalized else generate_password(10, 26).lower().capitalize()
    password = generate_password(11, 27, True)
    email = generate_password(12, 18)
    full_email = email + domain

    driver.get(url)
    time.sleep(sleeping_time_max)
    keyboard.type(user)
    driver.find_element(By.ID, 'password').send_keys(password)
    driver.find_element(By.ID, 'repeat-password').send_keys(password)
    elem = WebDriverWait(driver, sleeping_time_max).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,
                                        "body > div.app-root > div.flex-no-min-children.flex-nowrap.flex-column.h100.s"
                                        "ign-layout-bg.scroll-if-needed.relative > div.sign-layout-container.flex-"
                                        "item-fluid-auto.flex.flex-nowrap.flex-column.flex-justify-space-between > d"
                                        "iv > main > div.sign-layout-main-content > form > button")))
    time.sleep(random.randint(*random_time_range))
    elem.click()

    try:
        elem = WebDriverWait(driver, sleeping_time_max).until(
            EC.presence_of_element_located((By.XPATH, '//button[@data-testid="tab-header-Email-button"]')))
        time.sleep(random.randint(*random_time_range))
        elem.click()

        driver.find_element(By.ID, 'email').send_keys(full_email)
    except Exception as Exc:
        try:
            if use_capcha:
                print("Finding capcha...")
                elem = WebDriverWait(driver, 6).until(
                    EC.presence_of_element_located((By.XPATH, '//button[@data-testid="tab-header-CAPTCHA-button"]')))
                elem.click()
                input("\nPress enter when you complete the capcha and setup!")
                driver.close()
                return {'login': user + "@proton.me", 'password': password}
            else:
                driver.close()
                return
        except Exception as Exc:
            # print(Exc)
            driver.close()
            return

    elem = WebDriverWait(driver, sleeping_time_max).until(
        EC.presence_of_element_located(
            (By.XPATH, '//button[@class="button w100 button-large button-solid-norm mt1-5"]')))
    time.sleep(random.randint(*random_time_range))
    elem.click()

    if temporary_mail == 'guerrilla':
        content = get_guerrilla_mail(email)
        verification_code = content.split('<br>')[1].strip('</p>')
    elif temporary_mail == 'maildrop':
        mail_drop = MailDrop(mailbox=email, sleeping_time=sleeping_time_max, tries_to_stop=15)
        verification_code = mail_drop.get_code_by_many_tries()
        if not verification_code:
            raise ValueError("code is empty!")

    driver.find_element(By.ID, 'verification').send_keys(verification_code)

    elem = WebDriverWait(driver, sleeping_time_max).until(
        EC.presence_of_element_located(
            (By.XPATH, '//button[@class="button w100 button-large button-solid-norm mt1-5"]')))
    time.sleep(random.randint(*random_time_range))
    elem.click()

    time.sleep(sleeping_time_max)

    elem = WebDriverWait(driver, sleeping_time_max).until(
        EC.presence_of_element_located(
            (By.XPATH, '//button[@class="button w100 button-large button-solid-norm mt1-5"]')))
    time.sleep(random.randint(*random_time_range))
    elem.click()

    # maybe later???
    elem = WebDriverWait(driver, sleeping_time_max).until(
        EC.presence_of_element_located((By.XPATH, '//button[text() = "Maybe later"]')))
    time.sleep(random.randint(*random_time_range))
    elem.click()

    # other ...
    elem = WebDriverWait(driver, sleeping_time_max).until(
        EC.presence_of_element_located((By.XPATH, '//button[text() = "Confirm"]')))
    time.sleep(random.randint(*random_time_range))
    elem.click()
    time.sleep(sleeping_time_max)
    driver.close()

    return {'login': user + "@proton.me", 'password': password}
