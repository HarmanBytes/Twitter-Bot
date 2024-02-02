from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from datetime import datetime
import pytz
import traceback
import sys


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

    # tweet data xpath
    tweet_container = '//article[(@role="article") and (@data-testid="tweet")]'

    # needs tweet_container
    tweet_by_container = './/div[@data-testid="User-Name"]'
    tweet_text = './/div[@data-testid="tweetText"]'
    tweet_stats = './/span[@data-testid="app-text-transition-container"]'
    tweet_media = './/div[@data-testid="card.wrapper"]//*[@src]'

    # needs tweet_by_container
    tweet_by_display_name = './div[1]//span/span'
    tweet_by_username = './/span[starts-with(text(),"@")]'
    tweet_datetime = './/time'

    # explore section
    explore_btn = '//a[@data-testid="AppTabBar_Explore_Link"]'
    explore_tabs = '//div[(@role="tablist") and (@data-testid="ScrollSnap-List")]'
    explore_tabs_dict = {
        "trending": './/span[text()="Trending"]',
        "news": './/span[text()="News"]',
        "sports": './/span[text()="Sports"]',
        "entertainment": './/span[text()="Entertainment"]'
    }

    # trends
    trend_window = '//div[@aria-label="Timeline: Explore"]'
    trends = '//div[@data-testid="trend"]'
    single_trend_data = './div/div'

    @classmethod
    def waitfor_elementpresence(cls, driver, wait_time, by, value):
        try:
            return WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((by, value)))
        except Exception as e:
            print(e)

    @classmethod
    def wait_for_elements_presence(cls, driver, wait_time, by, value):
        try:
            return WebDriverWait(driver, wait_time).until(EC.presence_of_all_elements_located((by, value)))
        except Exception as e:
            print(e)


class BotFunctions(UI):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.df = pd.DataFrame()

        self.trending_df = {
            'trending': pd.DataFrame(),
            'news': pd.DataFrame(),
            'sports': pd.DataFrame(),
            'entertainment': pd.DataFrame()
        }

        self.trending_dict = {
            'trending': {
                'rank': 'NA',
                'trending_in': 'Unknown',
                'tag_or_text': 'NA',
                'posts': 'NA',
                'fetch_datetime': 'NA'
            },
            'news': {
                'trending_in': 'Unknown',
                'tag_or_text': 'NA',
                'posts': 'NA',
                'fetch_datetime': 'NA'
            },
            'sports': {
                'trending_in': 'Unknown',
                'tag_or_text': 'NA',
                'posts': 'NA',
                'fetch_datetime': 'NA'
            },
            'entertainment': {
                'trending_in': 'Unknown',
                'tag_or_text': 'NA',
                'posts': 'NA',
                'fetch_datetime': 'NA'
            }
        }

    def reset_data(self):
        self.df = pd.DataFrame()

        self.trending_df = {
            'trending': pd.DataFrame(),
            'news': pd.DataFrame(),
            'sports': pd.DataFrame(),
            'entertainment': pd.DataFrame()
        }

        self.trending_dict = {
            'trending': {
                'rank': 'NA',
                'trending_in': 'Unknown',
                'tag_or_text': 'NA',
                'posts': 'NA',
                'fetch_datetime': 'NA'
            },
            'news': {
                'trending_in': 'Unknown',
                'tag_or_text': 'NA',
                'posts': 'NA',
                'fetch_datetime': 'NA'
            },
            'sports': {
                'trending_in': 'Unknown',
                'tag_or_text': 'NA',
                'posts': 'NA',
                'fetch_datetime': 'NA'
            },
            'entertainment': {
                'trending_in': 'Unknown',
                'tag_or_text': 'NA',
                'posts': 'NA',
                'fetch_datetime': 'NA'
            }
        }

    def current_time(self):
        # current datetime
        current_datetime = time.strftime('%H:%M:%S %d-%m-%Y %z')

        # Convert string to datetime object
        datetime_object = datetime.strptime(current_datetime, '%H:%M:%S %d-%m-%Y %z')

        # Convert to UTC timezone
        utc_timezone = pytz.timezone('UTC')
        datetime_utc = datetime_object.astimezone(utc_timezone)

        current_datetime_in_utc = datetime_utc.strftime('%H:%M:%S %d-%m-%Y %z')
        return current_datetime_in_utc

    def click_on_signin(self):
        try:
            # finding sign in button using xpath
            # sign_in_btn = self.driver.find_element(by='xpath', value=UI.sign_in_btn)
            sign_in_btn = UI.waitfor_elementpresence(self.driver, 15, By.XPATH, UI.sign_in_btn)
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

    def scroll_down(self, scroll_to):
        try:
            self.driver.execute_script(f'return window.scrollTo(0,{scroll_to});')
        except Exception as e:
            print(e)

    def current_scroll_position(self):
        try:
            return self.driver.execute_script('return window.scrollY;')
        except Exception as e:
            print(e)

    def viewport_length(self):
        try:
            return self.driver.execute_script(f'return window.innerHeight;')
        except Exception as e:
            print(e)

    def page_height(self):
        try:
            return self.driver.execute_script("return document.body.scrollHeight;")
        except Exception as e:
            print(e)

    def check_page_end(self, last_scroll_position):
        try:
            if self.current_scroll_position() == last_scroll_position:
                return True
            else:
                return False
        except Exception as e:
            print(e)

    def remove_duplicate(self, trends, last_trend_location):
        position = 0
        try:
            if last_trend_location is None:
                return trends
            else:
                for trend in trends:
                    if trend.location['y'] <= last_trend_location:
                        position += 1
                if len(trends) == position:
                    return []
                return trends[position:]
        except Exception as e:
            print(e)
            # Use traceback to get the line number
            traceback_details = traceback.extract_tb(sys.exc_info()[2])
            line_number = traceback_details[len(traceback_details) - 1][1]
            print(f"Error occurred on line {line_number}: {e}")

    def load_tweets(self):
        try:
            tweets = UI.wait_for_elements_presence(self.driver, 15, By.XPATH, UI.tweet_container)
            return tweets
        except Exception as e:
            print(e)

    def click_on_explore(self):
        try:
            explore_btn = UI.waitfor_elementpresence(self.driver, 15, By.XPATH, UI.explore_btn)
            explore_btn.click()

            explore_tabs = UI.waitfor_elementpresence(self.driver, 15, By.XPATH, UI.explore_tabs)
            return explore_tabs
        except Exception as e:
            print(e)

    def click_on_explore_tabs(self, tab_name):
        try:
            explore_tabs = self.click_on_explore()
            tab = UI.waitfor_elementpresence(explore_tabs, 15, By.XPATH, UI.explore_tabs_dict[tab_name])
            tab.click()
        except Exception as e:
            print(e)

    def explore_tab_data(self, tab_name):
        last_trend_location = None
        last_scroll_position = None
        try:
            self.click_on_explore_tabs(tab_name)
            while True:
                trend_window = UI.waitfor_elementpresence(self.driver, 15, By.XPATH, UI.trend_window)
                trends = UI.wait_for_elements_presence(trend_window, 15, By.XPATH, UI.trends)
                trends = self.remove_duplicate(trends, last_trend_location)

                if not trends:
                    break

                for trend in trends:
                    try:
                        trending_data = self.trending_dict[tab_name].copy()
                        single_trend_data = UI.wait_for_elements_presence(trend, 15, By.XPATH, UI.single_trend_data)
                        if tab_name == 'trending':
                            rank_and_trending = [i.strip() for i in single_trend_data[0].text.split('\u00B7')]
                            trending_data['rank'] = rank_and_trending[0]
                            trending_data['trending_in'] = ' '.join(rank_and_trending[1:])
                        else:
                            trending_data['trending_in'] = single_trend_data[0].text
                        trending_data['tag_or_text'] = single_trend_data[1].text
                        trending_data['posts'] = single_trend_data[2].text.split()[0]
                        trending_data['fetch_datetime'] = self.current_time()

                        self.trending_df[tab_name] = pd.concat((self.trending_df[tab_name], pd.DataFrame([trending_data])))
                    except Exception as e:
                        # Use traceback to get the line number
                        traceback_details = traceback.extract_tb(sys.exc_info()[2])
                        line_number = traceback_details[len(traceback_details) - 1][1]
                        print(f"Error occurred on line {line_number}: {e}")

                # checking end
                if self.check_page_end(last_scroll_position) or last_trend_location == trends[-1].location['y']:
                    break

                last_trend_location = trends[-1].location['y']
                last_scroll_position = self.current_scroll_position()
                self.scroll_down(last_trend_location)
                time.sleep(5)

        except Exception as e:
            print(e)
            # Use traceback to get the line number
            traceback_details = traceback.extract_tb(sys.exc_info()[2])
            line_number = traceback_details[len(traceback_details) - 1][1]
            print(f"Error occurred on line {line_number}: {e}")

    def data_from_explore_tabs(self):
        try:
            self.explore_tab_data('trending')
            self.explore_tab_data('news')
            self.explore_tab_data('sports')
            self.explore_tab_data('entertainment')
        except Exception as e:
            print(e)

    def fetch_single_tweet_data(self, tweet):
        try:
            tweet_container = tweet

            tweet_details = {'display_name': 'NA', 'username': 'NA', 'tweet_text': 'NA', 'reply': 'NA', 'retweet': 'NA',
                             'like': 'NA', 'view': 'NA', 'media_links': 'NA', 'tweet_datetime': 'NA',
                             'fetch_datetime': 'NA'}

            tweet_by_container = tweet_container.find_element(by='xpath', value=UI.tweet_by_container)
            # from tweet_by_container
            tweet_details['display_name'] = tweet_by_container.find_element(by='xpath', value=UI.tweet_by_display_name).text
            tweet_details['username'] = tweet_by_container.find_element(by='xpath', value=UI.tweet_by_username).text

            # tweet datetime
            tweet_datetime = tweet_by_container.find_element(by='xpath', value=UI.tweet_datetime).get_attribute('datetime')
            tweet_datetime = datetime.fromisoformat(tweet_datetime)
            tweet_details['tweet_datetime'] = tweet_datetime.strftime('%H:%M:%S %d-%m-%Y %z')

            # tweet text
            tweet_details['tweet_text'] = tweet_container.find_element(by='xpath', value=UI.tweet_text).text

            # media links
            media_links = tweet_container.find_elements(by='xpath', value=UI.tweet_media)
            tweet_details['media_links'] = [link.get_attribute('src') for link in media_links]

            # tweet stats
            tweet_stats = tweet_container.find_elements(by='xpath', value=UI.tweet_stats)
            (tweet_details['reply'], tweet_details['retweet'], tweet_details['like'],
                tweet_details['view']) = [stat.text for stat in tweet_stats]

            # fetch datetime
            tweet_details['fetch_datetime'] = self.current_time()

            return pd.DataFrame([tweet_details])

        except Exception as e:
            print(e)

    def fetch_multiple_tweets_data(self):
        try:
            tweets = self.load_tweets()
            for tweet in tweets:
                tweet_details = self.fetch_single_tweet_data(tweet)
                self.df = pd.concat((self.df, tweet_details))
        except Exception as e:
            print(e)

    def generate_csv(self, csv_of, file_name='tweets'):
        if csv_of == 'tweets':
            self.df.to_csv(f'{file_name}.csv', index=False)
        elif csv_of == 'trending':
            for name, df in self.trending_df.items():
                df.to_csv(f'{name}.csv', index=False)


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



