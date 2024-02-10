# importing libraries
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
    """
    A class representing the user interface elements and XPath selectors for interacting with Twitter.
    To know more checkout <filename>.
    """
    #  Login System XPath selectors
    sign_in_btn = '//a[@data-testid="loginButton"]'
    username_or_email_input = '//input[@autocomplete="username"]'
    sign_in_window_next_btn = '//div[@role="group"][1]//div[@role="button"][2]'
    username_or_phone_heading = '//h1/span/span[text()="Enter your phone number or username"]'
    username_or_phone_input = '//input[@data-testid="ocfEnterTextTextInput"]'
    verify_window_next_btn = '//div[@data-testid="ocfEnterTextNextButton"]'
    password_heading = '//h1/span/span[text()="Enter your password"]'
    password_input = '//input[@name="password"]'
    login_button = '//div[@data-testid="LoginForm_Login_Button"]'

    remove_pop_up = '//div[@data-testid="app-bar-close"]'

    # Tweet data XPath selectors
    tweet_container = '//article[(@role="article") and (@data-testid="tweet")]'

    # Needs tweet_container as parent element
    tweet_by_container = './/div[@data-testid="User-Name"]'
    tweet_text = './/div[@data-testid="tweetText"]'
    tweet_stats = './/span[@data-testid="app-text-transition-container"]'
    tweet_media = './/div[@data-testid="card.wrapper"]//*[@src]'

    # Needs tweet_by_container as parent element
    tweet_by_display_name = './div[1]//span/span'
    tweet_by_username = './/span[starts-with(text(),"@")]'
    tweet_datetime = './/time'

    # Explore sections XPath selectors
    explore_btn = '//a[@data-testid="AppTabBar_Explore_Link"]'
    explore_tabs = '//div[(@role="tablist") and (@data-testid="ScrollSnap-List")]'
    explore_tabs_dict = {
        "trending": './/span[text()="Trending"]',
        "news": './/span[text()="News"]',
        "sports": './/span[text()="Sports"]',
        "entertainment": './/span[text()="Entertainment"]'
    }

    # Trend section XPath selectors
    trend_window = '//div[@aria-label="Timeline: Explore"]'
    trends = '//div[@data-testid="trend"]'
    single_trend_data = './div/div'

    @classmethod
    def wait_for_element_presence(cls, driver, wait_time, by, value, find_all=False):
        """
        Wait for the presence of a web element identified by the given selector.

        Parameters:
            driver: WebDriver instance to use for locating the element.
            wait_time (int): Maximum time to wait for the element to be present, in seconds.
            by: Locator strategy to use for finding the element (e.g., By.ID, By.XPATH).
            value: Value of the locator (e.g., ID, XPath expression) to locate the element.
            find_all (bool): If True, wait for all elements matching the selector. Default is False.

        Returns:
            WebElement or List[WebElement]: The located web element(s) if present within the specified wait time.
            Returns a single WebElement if find_all is False, otherwise returns a list of WebElements.

        Raises:
            TimeoutException: If the element is not found within the specified wait time.
        """
        try:
            if find_all:
                return WebDriverWait(driver, wait_time).until(EC.presence_of_all_elements_located((by, value)))
            return WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((by, value)))
        except Exception as e:
            print(e)


class BotFunctions(UI):
    """
    A class representing bot functions for interacting with Twitter.
    Inherits UI class for accessing XPath selectors.
    """
    def __init__(self, driver):
        """
        Initializes BotFunctions object.

        Parameters:
            driver: WebDriver instance.
        """
        super().__init__()
        self.driver = driver
        self.tweets_df = pd.DataFrame()

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
        """
        Reset data attributes to empty DataFrames.

        Resets the tweets DataFrame and trending DataFrames to empty DataFrames.
        Also resets the trending dictionary with default values.

        Returns:
            None
        """
        self.tweets_df = pd.DataFrame()
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

    def current_datetime(self):
        """
        Tells the current date and time in UTC timezone.

        Returns:
            Current date and time in UTC timezone.
        """
        current_datetime = time.strftime('%H:%M:%S %d-%m-%Y %z')
        datetime_object = datetime.strptime(current_datetime, '%H:%M:%S %d-%m-%Y %z')
        utc_timezone = pytz.timezone('UTC')
        datetime_utc = datetime_object.astimezone(utc_timezone)
        current_datetime_in_utc = datetime_utc.strftime('%H:%M:%S %d-%m-%Y %z')
        return current_datetime_in_utc

    def perform(self, driver, wait_time, by, value, action, keys=None, message=None):
        """
        Perform the desired action on a located element.

        Actions include clicking a button, typing in a text box, etc.

        Parameters:
            driver (WebDriver): The WebDriver instance used for locating the element.
            wait_time (int): Maximum time to wait for the element to be present, in seconds.
            by: Locator strategy to use for finding the element (e.g., By.ID, By.XPATH).
            value: Value of the locator (e.g., ID, XPath expression) to locate the element.
            action (str): Type of action to perform on the located element.
                Available actions: 'click', 'send_keys'.
            keys: Additional data to send to the located element (default is None).
            message: Message to show if the element is not located (default is None).

        Returns:
            None

        Raises:
            TimeoutException: If the element is not found within the specified wait time.
        """
        try:
            element = UI.wait_for_element_presence(driver, wait_time, by, value)
            actions = {
                'click': element.click,
                'send_keys': element.send_keys
            }
            if action == 'send_keys':
                actions[action](keys)
            else:
                actions[action]()
        except Exception as e:
            if message is not None:
                print(message)
            else:
                print(e)

    def login(self, username, password):
        """
        Login to Twitter.

        Parameters:
            username (str): Username, phone number, or email address associated with the account.
                            Username is preferred to enter.
            password (str): Account password.

        Returns:
            None

        Raises:
            Any exceptions that occur during the login process are caught and printed.
        """
        try:
            # Click the sign-in button, Input username/email/phone and Click next
            self.perform(self.driver, 15, By.XPATH, UI.sign_in_btn, action='click')
            self.perform(self.driver, 15, By.XPATH, UI.username_or_email_input, action='send_keys', keys=username)
            self.perform(self.driver, 15, By.XPATH, UI.sign_in_window_next_btn, action='click')

            # If additional verification is needed
            if UI.wait_for_element_presence(self.driver, 15, By.XPATH, UI.username_or_phone_heading, find_all=True) is not None:
                if not username.isdigit():
                    username = input('Enter Username')
                time.sleep(5)
                self.perform(self.driver, 15, By.XPATH, UI.username_or_phone_input, action='send_keys', keys=username)
                self.perform(self.driver, 15, By.XPATH, UI.verify_window_next_btn, action='click')

            # Input password and Click login button
            time.sleep(2)
            self.perform(self.driver, 15, By.XPATH, UI.password_input, action='send_keys', keys=password)
            time.sleep(2)
            self.perform(self.driver, 15, By.XPATH, UI.login_button, action='click')

            # Handle any pop-up if present
            self.perform(self.driver, 15, By.XPATH, UI.remove_pop_up, action='click', message='No popup found.')

        except Exception as e:
            print(e)

    def scroll_down(self, scroll_to):
        """
        Scroll the webpage vertically to the specified position.

        Parameters:
            scroll_to (int): The vertical position (in pixels) to scroll to.

        Returns:
            None

        Raises:
            Any exceptions that occur during the scrolling process are caught and printed.
        """
        try:
            self.driver.execute_script(f'return window.scrollTo(0,{scroll_to});')
        except Exception as e:
            print(e)

    def current_scroll_position(self):
        """
        Returns the current vertical scroll position of the page.

        Parameters: None

        Returns:
            int: The current vertical scroll position of the page, in pixels.

        Raises:
            Any exceptions that occur during the retrieval of the scroll position are caught and printed.
        """
        try:
            return self.driver.execute_script('return window.scrollY;')
        except Exception as e:
            print(e)

    def check_page_end(self, last_scroll_position):
        """
        Check if the user has reached the end of the webpage.

        Parameters:
            last_scroll_position (int): The last recorded vertical scroll position of the page.

        Returns:
            bool: True if the user has reached the end of the page (scroll position unchanged),
                  False otherwise.

        Raises:
            Any exceptions that occur during the retrieval of the scroll position are caught and printed.
        """
        try:
            if self.current_scroll_position() == last_scroll_position:
                return True
            else:
                return False
        except Exception as e:
            print(e)

    def filter_out_duplicates(self, trends, last_trend_location):
        """
        Remove duplicate trends based on their vertical position.

        Parameters:
            trends (list): A list of trend objects.
            last_trend_location (int or None): The vertical position (y-coordinate) of the last trend
                displayed on the page, or None if no trends have been displayed yet.

        Returns:
            list: A filtered list of trend objects, removing duplicates that have a vertical position
                less than or equal to the last trend location.

        Raises:
            Any exceptions that occur during the removal process are caught and printed, along with
            the line number where the error occurred.
        """
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
        """
        Locate and return all the tweets present on the webpage.

        Returns:
            list: A list containing all the tweets found on the webpage.

        Raises:
            Any exceptions that occur during the tweet loading process are caught and printed.
        """
        try:
            tweets = UI.wait_for_element_presence(self.driver, 15, By.XPATH, UI.tweet_container, find_all=True)
            return tweets
        except Exception as e:
            print(e)

    def fetch_single_tweet_data(self, tweet):
        """
        Extract data from a single tweet element and return it as a DataFrame.

        Parameters:
            tweet: WebElement object representing the tweet element to extract data from.

        Returns:
            DataFrame: A pandas DataFrame containing the extracted data from the tweet.

        Raises:
            Any exceptions that occur during the data extraction process are caught and printed.
        """
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
            tweet_details['fetch_datetime'] = self.current_datetime()

            return pd.DataFrame([tweet_details])

        except Exception as e:
            print(e)

    def fetch_multiple_tweets_data(self):
        """
        Fetch data from multiple tweets and append it to the DataFrame.

        This method iterates through the tweets loaded on the webpage, extracts data from each tweet using
        the fetch_single_tweet_data method, and appends the extracted data to the DataFrame self.tweets_df.

        Returns:
            None

        Raises:
            Any exceptions that occur during the data fetching process are caught and printed.
        """
        try:
            tweets = self.load_tweets()
            for tweet in tweets:
                tweet_details = self.fetch_single_tweet_data(tweet)
                self.tweets_df = pd.concat((self.tweets_df, tweet_details))
        except Exception as e:
            print(e)

    def click_on_explore(self):
        """
        Clicks on the explore button present on the left sidebar of Twitter.

        This method performs a click action on the explore button, waits for the explore tabs to load,
        and returns an object containing the trending sections like Trending, Sports, News, and Entertainment.

        Returns:
            WebElement: An object representing the explore tabs section containing trending sections.

        Raises:
            Any exceptions that occur during the process of clicking on explore or waiting for the explore
            tabs to load are caught and printed.
        """
        try:
            self.perform(self.driver, 15, By.XPATH, UI.explore_btn, action='click')
            explore_tabs = UI.wait_for_element_presence(self.driver, 15, By.XPATH, UI.explore_tabs)
            return explore_tabs
        except Exception as e:
            print(e)

    def click_on_explore_tabs(self, tab_name):
        """
        Clicks on the tab corresponding to the given tab name in the explore section.

        This method first clicks on the explore button to ensure the explore section is open, then
        clicks on the tab specified by the tab_name parameter.

        Parameters:
            tab_name (str): The name of the tab to click on.
            Available tab_name: 'Trending', 'News', 'Sports' and 'Entertainment'.

        Returns:
            None

        Raises:
            Any exceptions that occur during the process of clicking on explore or the specified tab
            are caught and printed.
        """
        try:
            explore_tabs = self.click_on_explore()
            self.perform(explore_tabs, 15, By.XPATH, UI.explore_tabs_dict[tab_name], action='click')
        except Exception as e:
            print(e)

    def explore_tab_data(self, tab_name):
        """
        Extract data from the specified explore tab and store it in the trending DataFrame.

        This method clicks on the explore tab specified by the tab_name parameter, iterates through
        the trending topics present in the tab, extracts relevant data for each topic, and appends
        it to the trending DataFrame.

        Parameters:
            tab_name (str): The name of the explore tab to extract data from.

        Returns:
            None

        Raises:
            Any exceptions that occur during the data extraction process are caught and printed, along
            with the line number where the error occurred.
        """
        last_trend_location = None
        last_scroll_position = None
        try:
            self.click_on_explore_tabs(tab_name)
            while True:
                trend_window = UI.wait_for_element_presence(self.driver, 15, By.XPATH, UI.trend_window)
                trends = UI.wait_for_element_presence(trend_window, 15, By.XPATH, UI.trends, find_all=True)
                trends = self.filter_out_duplicates(trends, last_trend_location)

                if not trends:
                    break

                for trend in trends:
                    try:
                        trending_data = self.trending_dict[tab_name].copy()
                        single_trend_data = UI.wait_for_element_presence(trend, 15, By.XPATH, UI.single_trend_data, find_all=True)
                        if tab_name == 'trending':
                            rank_and_trending = [i.strip() for i in single_trend_data[0].text.split('\u00B7')]
                            trending_data['rank'] = rank_and_trending[0]
                            trending_data['trending_in'] = ' '.join(rank_and_trending[1:])
                        else:
                            trending_data['trending_in'] = single_trend_data[0].text
                        trending_data['tag_or_text'] = single_trend_data[1].text
                        trending_data['posts'] = single_trend_data[2].text.split()[0]
                        trending_data['fetch_datetime'] = self.current_datetime()

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
        """
        Extract data from multiple explore tabs and store it in the trending DataFrame.

        This method extracts data from the 'Trending', 'News', 'Sports', and 'Entertainment' explore tabs
        using the explore_tab_data method and stores it in the trending DataFrame.

        Returns:
            None

        Raises:
            Any exceptions that occur during the data extraction process are caught and printed.
        """
        try:
            self.explore_tab_data('trending')
            self.explore_tab_data('news')
            self.explore_tab_data('sports')
            self.explore_tab_data('entertainment')
        except Exception as e:
            print(e)

    def generate_csv(self, csv_of, file_name='tweets'):
        """
        Generate CSV file(s) based on the provided data type.

        This method generates CSV file(s) based on the provided data type. If csv_of is 'tweets',
        it generates a CSV file containing tweet data. If csv_of is 'trending', it generates
        separate CSV files for each trending category.

        Parameters:
            csv_of (str): Specifies the type of data to generate CSV file(s) for. It can be either
                'tweets' or 'trending'.
            file_name (str): Optional. The base name for the generated CSV file(s). Defaults to 'tweets'.

        Returns:
            None
        """
        if csv_of == 'tweets':
            self.tweets_df.to_csv(f'{file_name}.csv', index=False)
        elif csv_of == 'trending':
            for name, df in self.trending_df.items():
                df.to_csv(f'{name}.csv', index=False)


class TwitterBot(BotFunctions):
    """
    Initializes a TwitterBot instance.

    This constructor sets up the TwitterBot instance by initializing the WebDriver for
    Microsoft Edge browser, maximizing the window, and navigating to the Twitter homepage.

    Parameters: None

    Returns:
        None
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



