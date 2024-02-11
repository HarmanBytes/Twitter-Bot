from twitterbot import TwitterBot as tb
import time

bot = tb(input("Enter Username: "))
bot.open_website()
if not bot.load_cookies():
    bot.login(password=input('Enter password: '))
    bot.save_cookies()
else:
    bot.refresh_page()

# tested -- works successfully

# bot.fetch_multiple_tweets_data()
# bot.generate_csv(csv_of='tweets')
# bot.data_from_explore_tabs()
# bot.generate_csv(csv_of='trending')

print('finished')
time.sleep(60)
