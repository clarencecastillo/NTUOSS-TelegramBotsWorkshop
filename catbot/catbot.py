# NTUOSS Telegram Bots Workshop
# 22 September 2017
# Speakers: Clarence Castillo & Steve Ye
# Repository: https://github.com/clarencecastillo/NTUOSS-TelegramBotsWorkshop

# ------------------------ WRITE YOUR CODES BELOW THIS LINE ------------------------ #

import urllib
import time, telepot
from telepot.loop import MessageLoop
from cat import Cat

# TODO: 2.2.2 Import Keyboards #######################################################

# TODO: 3.1.2 Import Requests ########################################################

# TODO: 3.2.1 Import Random and BeautifulSoup ########################################

# TODO: 4.1.1 Import DelegatorBot ####################################################

# TODO: 4.2.2 Import KeyboardButton, ReplyKeyboardMarkup and Conversation Dialog #####

# TODO: 1.3.2 Replace Token ##########################################################
TOKEN = ''

# TODO: 4.2.1 Set Conversation States ################################################

# TODO: 4.1.2 Wrap CatBot Class ######################################################

# TODO: 3.1.1 Get Random Cat Fact ####################################################

# TODO: 3.2.2 Get Random Cat Image URL ###############################################

def on_chat_message(msg):
    global cat_bot
    content_type, chat_type, chat_id = telepot.glance(msg)

    # TODO: 1.3.1 Create Hello World #################################################

def on_callback_query(msg):
    global cat_bot
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

    # TODO: 2.2.3 Handle Callback Query ##############################################

    # answer callback query or else telegram will forever wait on this
    bot.answerCallbackQuery(query_id)

# bootstrap the bot and spawn the cat
# TODO: 4.1.3 Implement DelegatorBot #################################################
bot = telepot.Bot(TOKEN)
MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query}).run_as_thread()

bot_name = bot.getMe()['first_name']
cat_bot = Cat(bot_name)
print('Meow! ' + bot_name + ' at your service...')

# keep the program running and simulate cat life
cat_last_update = time.time()
while True:
    time.sleep(10)

    # update cat every 6 hours
    if (time.time() - cat_last_update > 24/4*60*60):
        cat_bot.on_update()
        cat_last_update = time.time()

# ------------------------ WRITE YOUR CODES ABOVE THIS LINE ------------------------ #
