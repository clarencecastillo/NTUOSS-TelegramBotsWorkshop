# NTUOSS Telegram Bots Workshop
# 22 September 2017
# Speakers: Clarence Castillo & Steve Ye
# Repository: https://github.com/clarencecastillo/NTUOSS-TelegramBotsWorkshop

# import required modules
import time, json, requests, telepot
from telepot.loop import MessageLoop
from cat import Cat

# ------------------------ WRITE YOUR CODES BELOW THIS LINE ------------------------ #



# ------------------------ WRITE YOUR CODES ABOVE THIS LINE ------------------------ #

# bootstrap the bot and spawn the cat
bot = telepot.Bot(TOKEN)
bot_name = bot.getMe()['first_name']
cat_bot = Cat(bot_name, 4)

MessageLoop(bot, on_chat_message).run_as_thread()
print('Meow! ' + bot_name + ' at your service...')

# keep the program running
while True: time.sleep(10)
