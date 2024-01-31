from twitterbot import TwitterBot as tb
import time


with open('user_details.txt', 'r') as f:
    info = f.read()

username, email, password = info.split(' ')

bot = tb()
# tested -- works successfully
# bot.login_with_username(username, password)

# tested -- works successfully
bot.login_with_email(username, email, password)

time.sleep(30)
