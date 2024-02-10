from twitterbot import TwitterBot as tb
import time

# create your own txt file in format "username password"
with open('user_details.txt', 'r') as f:
    info = f.read()

username, password = info.split(' ')
bot = tb()

# tested -- works successfully
bot.login(username, password)
bot.fetch_multiple_tweets_data()
bot.generate_csv(csv_of='tweets')
bot.data_from_explore_tabs()
bot.generate_csv(csv_of='trending')

print('finished')
time.sleep(60)
