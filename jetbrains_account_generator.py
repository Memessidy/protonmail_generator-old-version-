from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
from pynput.keyboard import Controller, Key
from fake_data import get_person
import csv


class JetAcc:
    def __init__(self):
        self.person = get_person()
        self.keyboard = Controller()
        self.driver = None
        self.proton_login = None
        self.proton_password = None
        self.file_name = 'data.csv'
        self.jetbrains_accounts = 'jetbrains_accs.csv'

    def start_register_jetbrains(self):
        self.driver.get('https://account.jetbrains.com/login')
        time.sleep(6)
        self.driver.find_element(By.NAME, "email").send_keys(self.proton_login)
        elem = WebDriverWait(self.driver, 6).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[@class="btn btn-primary btn-lg sign-up-button eml-submit-btn"]')))
        elem.click()

    def protonmail_login(self):
        """
        Підтверджувати обліковий запис
        """

        url = 'https://account.proton.me/login'
        time.sleep(8)
        self.driver.get(url)
        elem = WebDriverWait(self.driver, 6).until(
            EC.presence_of_element_located((By.ID, 'username')))
        elem.send_keys(self.proton_login)

        elem = WebDriverWait(self.driver, 6).until(
            EC.presence_of_element_located((By.ID, 'password')))
        elem.send_keys(self.proton_password)

        elem = WebDriverWait(self.driver, 6).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[@class="button w100 button-large button-solid-norm mt1-5"]')))
        elem.click()

        time.sleep(15)

        try:
            for i in range(3):
                elem = WebDriverWait(self.driver, 6).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//button[@class="button w100 button-large button-solid-norm"]')))
                elem.click()
                time.sleep(1)
        except:
            pass

        self.keyboard.press(Key.tab)
        self.keyboard.press(Key.enter)
        # in message here
        time.sleep(1)
        for i in range(14):
            self.keyboard.press(Key.tab)
            time.sleep(0.5)
        self.keyboard.tap(Key.enter)
        self.keyboard.press(Key.enter)

    def continue_registration(self):
        elem = self.driver.find_element(By.XPATH, '//span[@class="text-bold text-break"]')
        self.driver.get(elem.text)
        # in jetbrains
        time.sleep(14)

        self.driver.find_element(By.NAME, "firstName").send_keys(self.person['first name'])
        self.driver.find_element(By.NAME, "lastName").send_keys(self.person['last name'])
        self.driver.find_element(By.NAME, "userName").send_keys(self.person['nickname'])
        self.driver.find_element(By.NAME, "password").send_keys(self.person['password'])
        self.driver.find_element(By.NAME, "pass2").send_keys(self.person['password'])
        self.driver.find_element(By.NAME, "privacy").click()
        elem = WebDriverWait(self.driver, 6).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button[@class="pwd-submit-btn btn btn-primary btn-lg"]')))
        elem.click()

    def write_jetbrains_data(self, data):
        with open(self.jetbrains_accounts, mode='a+',  newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(data)

    def get_data(self):
        with open(self.file_name, newline='', mode='r') as csvfile:
            for row in csv.reader(csvfile, delimiter=';'):
                yield row

    def generate_account(self, row):
        self.driver = webdriver.Chrome(service=Service((ChromeDriverManager().install())), options=Options())
        self.driver.maximize_window()
        self.proton_login, self.proton_password = row
        time.sleep(5)
        self.start_register_jetbrains()
        time.sleep(5)
        self.protonmail_login()
        self.continue_registration()
        self.driver.close()
        return self.person['password']

    def try_app(self, row):
        writed = False
        while not writed:
            try:
                password = self.generate_account(row)
                row.append(password)
                self.write_jetbrains_data(row)
                print("Записано!")
                writed = True
            except:
                continue

    def generate_accounts(self):
        for row in self.get_data():
            if not row:
                print("Немає доступних скриньок!")
            else:
                self.try_app(row)


if __name__ == '__main__':
    jet_acc = JetAcc()
    jet_acc.generate_accounts()
