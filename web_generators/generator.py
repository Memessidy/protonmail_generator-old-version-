from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from pynput.keyboard import Controller
from random_press.unit_data import Unit
# from fake_useragent import UserAgent

options = Options()

# ip_addr = '5.78.41.248'
# port = '8080'
#
# options.add_argument(f"--proxy-server={ip_addr}:{port}")
# options.set_capability('acceptInsecureCerts', True)
# options.add_argument(f"user-agent=HelloWorld")
# options.add_argument("--window-size=1366,768")
# options.headless = True


def new_protonmail(sleeping_time_min=10, sleeping_time_max=30, sleeping_time_middle=15):

    keyboard = Controller()
    driver = webdriver.Chrome(service=Service((ChromeDriverManager().install())), options=options)
    driver.maximize_window()
    unit = Unit()

    url = 'https://account.proton.me/signup?plan=free&billing=12&ref=prctbl&minimumCycle=1' \
              '2&currency=EUR&product=mail&language=en'

    driver.get(url)
    time.sleep(sleeping_time_middle)

    # Start input here
    keyboard.type(unit.user_name)

    driver.find_element(By.ID, 'password').send_keys(unit.password)
    driver.find_element(By.ID, 'repeat-password').send_keys(unit.password)

    elem = WebDriverWait(driver, sleeping_time_max).until(
            EC.presence_of_element_located((By.XPATH, '//button[text() = "Create account"]')))
    # Перший клік пілся паролів (середнє очікування)
    elem.click()

    # print("Trying to create account")
    time.sleep(sleeping_time_middle)

    # Пошук кнопки email (коротке очікування)
    try:
        elem = WebDriverWait(driver, sleeping_time_max).until(
                    EC.presence_of_element_located((By.XPATH, '//button[@data-testid="tab-header-Email-button"]')))
        time.sleep(sleeping_time_min)
        elem.click()
    except:
        pass

    driver.find_element(By.ID, 'email').send_keys(unit.mail_box.box_name + unit.mail_box.domain)

    elem = WebDriverWait(driver, sleeping_time_max).until(
            EC.presence_of_element_located((By.XPATH, '//button[text() = "Get verification code"]')))
    time.sleep(sleeping_time_min)
    elem.click()
    # print("Trying to get verification code")
    # Пілся натискання Get verification code

    verification_code = unit.mail_box.get_code()
    driver.find_element(By.ID, 'verification').send_keys(verification_code)

    elem = WebDriverWait(driver, sleeping_time_max).until(
            EC.presence_of_element_located((By.XPATH, '//button[text() = "Verify"]')))
    elem.click()
    # print("Verified")

    # Після натискання кнопки Verify (піля того, як ввели код з пошти)(середнє очікування)
    time.sleep(sleeping_time_middle)

    elem = WebDriverWait(driver, sleeping_time_max).until(
            EC.presence_of_element_located((By.XPATH, '//button[text() = "Next"]')))
    time.sleep(sleeping_time_middle)
    elem.click()
    # print("Trying to create account: continuing")
    # Після натискання кнопки Next (Сережнє очікування)

    elem = WebDriverWait(driver, sleeping_time_max).until(
            EC.presence_of_element_located((By.XPATH, '//button[text() = "Maybe later"]')))
    elem.click()
    time.sleep(sleeping_time_min)

    # Коротке очікування

    elem = WebDriverWait(driver, sleeping_time_max).until(
            EC.presence_of_element_located((By.XPATH, '//button[text() = "Confirm"]')))
    elem.click()
    time.sleep(sleeping_time_min)

    driver.close()

    try:
        driver.quit()
    except:
        pass
    return {'login': f"{unit.user_name}@proton.me", 'password': unit.password}
