from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd


class UI:
    #  login system ui buttons xpath
    #  screen1
    sign_in_btn = '//a[@data-testid="loginButton"]'
    username_input = '//input[@autocomplete="username"]'
    next_btn = '//div[@role="group"][1]//div[@role="button"][2]'

    # if user entered email in screen1
    username_input_2 = '//input[@data-testid="ocfEnterTextTextInput"]'
    next_btn_2 = '//div[@data-testid="ocfEnterTextNextButton"]'

    # if user entered username in screen1
    password_input = '//input[@name="password"]'
    login_button = '//div[@data-testid="LoginForm_Login_Button"]'

    # close popup xpath
    pop_up = '//div[@data-testid="app-bar-close"]'

    @classmethod
    def waitfor_elementpresence(cls, driver, wait_time, by, value):
        try:
            return WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((by, value)))
        except Exception as e:
            print(e)


class BotFunctions(UI):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver

    def click_on_signin(self):
        try:
            # finding sign in button using xpath
            sign_in_btn = self.driver.find_element(by='xpath', value=UI.sign_in_btn)
            # clicking on sign in button
            sign_in_btn.click()
        except Exception as e:
            print(e)

    def remove_popup(self):
        try:
            pop_up = UI.waitfor_elementpresence(self.driver, 10, By.XPATH, UI.pop_up)
            pop_up.click()
            print('Pop up closed')
        except:
            print('No pop up found.')

    def password_in(self, password):
        try:
            password_input = UI.waitfor_elementpresence(self.driver, 15, By.XPATH, UI.password_input)
            password_input.send_keys(password)
            time.sleep(2)

            login_btn = self.driver.find_element(by='xpath', value=UI.login_button)
            login_btn.click()
        except Exception as e:
            print(e)

    def login_with_username(self, username, password):
        try:
            self.click_on_signin()
            time.sleep(2)

            username_input = UI.waitfor_elementpresence(self.driver, 15, By.XPATH, UI.username_input)
            username_input.click()
            username_input.send_keys(username)
            time.sleep(2)

            next_btn = self.driver.find_element(by='xpath', value=UI.next_btn)
            next_btn.click()
            time.sleep(2)

            self.password_in(password)
            self.remove_popup()
        except Exception as e:
            print(e)

    def login_with_email(self, username, email, password):
        try:
            self.click_on_signin()
            time.sleep(2)

            email_input = UI.waitfor_elementpresence(self.driver, 15, By.XPATH, UI.username_input)
            email_input.send_keys(email)
            time.sleep(2)

            next_btn = self.driver.find_element(by='xpath', value=UI.next_btn)
            next_btn.click()
            time.sleep(2)

            username_input = UI.waitfor_elementpresence(self.driver, 15, By.XPATH, UI.username_input_2)
            username_input.send_keys(username)

            next_btn_2 = self.driver.find_element(by='xpath', value=UI.next_btn_2)
            next_btn_2.click()
            time.sleep(2)

            self.password_in(password)
            self.remove_popup()
        except Exception as e:
            print(e)

    def fetch_tweet_data(self):
        pass

    def generate_csv(self):
        pass
class TwitterBot(BotFunctions):
    """
    Implicit waits are added temporarily for testing purposes
    """

    def __init__(self):
        self.driver = None
        self.options = Options()
        self.url = 'https://twitter.com/?lang=en'
        self.driver_loc = 'D:/Software/edgeDriver/msedgedriver.exe'
        self.edge_service = webdriver.EdgeService(executable_path=self.driver_loc)
        self.driver = webdriver.Edge(service=self.edge_service, options=self.options)
        self.driver.maximize_window()
        self.driver.get(self.url)
        super().__init__(self.driver)



