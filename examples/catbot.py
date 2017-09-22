# NTUOSS Telegram Bots Workshop
# 22 September 2017
# Speakers: Clarence Castillo & Steve Ye
# Repository: https://github.com/clarencecastillo/NTUOSS-TelegramBotsWorkshop

# ------------------------ WRITE YOUR CODES BELOW THIS LINE ------------------------ #

import urllib
import time, telepot
from telepot.loop import MessageLoop
from cat import Cat

from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

import requests

import random
from bs4 import BeautifulSoup

from telepot import DelegatorBot
from telepot.delegate import pave_event_space, per_chat_id, create_open

from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from conversation import dialog

from conversation import dialog

TOKEN = ''

MEOW_CHOOSE_LANG = 0
MEOW_CONFIRM_LANG = 1
MEOW_LEAD_TOPIC = 2
MEOW_REACT_SENTIMENT = 3

class CatBot(telepot.helper.ChatHandler):

    def __init__(self, *args, **kwargs):
        super(CatBot, self).__init__(include_callback_query=True, *args, **kwargs)
        self.state = MEOW_CHOOSE_LANG
        self.language = None
        self.sentiment = 0

    def get_random_cat_fact(self):
        response = requests.get('https://catfact.ninja/fact').json()
        return response['fact']

    def get_random_cat_image_url(self):

        # get a random page number
        max_pages = 296
        random_page_number = random.randint(1, max_pages)

        # get the random page
        rand_cat_image_url = 'http://www.cutestpaw.com/tag/cats/page/' + str(random_page_number)
        response = requests.get(rand_cat_image_url)

        # load the page into bs4 and get random image
        soup = BeautifulSoup(response.text, 'html.parser')
        image_container = soup.find('div', {'id': 'photos'})
        images = image_container.find_all('img')
        random_image = random.choice(images)

        return random_image['src']

    def on_chat_message(self, msg):
        global cat_bot
        content_type, chat_type, chat_id = telepot.glance(msg)

        # default response (feel free to change it)
        response = 'Meow!'

        # handle only messages with text content
        if content_type == 'text':

            # get message payload
            msg_text = msg['text']

            if (msg_text.startswith('/')):

                # parse the command excluding the '/'
                command = msg_text[1:].lower()

                # prepare the correct response based on the given command
                if (command == 'ask'):
                    # prepare response with random cat fact if cat is alive
                    if (cat_bot.is_alive):
                        response = 'Meow! ' + self.get_random_cat_fact()
                    else:
                        response = 'This cat is currently unavailable.'
                elif (command == 'status'):
                    bot.sendChatAction(chat_id, 'upload_photo')
                    bot.sendPhoto(chat_id, self.get_random_cat_image_url())
                    response = cat_bot.get_status()
                elif (command == 'feed'):
                    response = cat_bot.feed()
                elif (command == 'clean'):
                    response = cat_bot.clean()
                elif (command == 'kitty'):
                    # TODO: 2.2.1 Confirm User Action Using Keyboard

                    if (cat_bot.is_alive):

                        # prepare confirm keyboard
                        confirm_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                            [InlineKeyboardButton(text='Confirm', callback_data='kitty-confirm')],
                            [InlineKeyboardButton(text='Cancel', callback_data='kitty-cancel')],
                        ])

                        # send response with keyboard
                        response += ' Warning: ' + cat_bot.name + ' is still alive. Issuing this command will kill the cat (brutally) and reset all progress. Please confirm your action.'
                        bot.sendMessage(chat_id, response, reply_markup = confirm_keyboard)

                        # terminate prematurely to avoid sending message twice
                        return

                    else:

                        # respawn cat
                        cat_bot.kill()
                        bot.sendMessage(chat_id, '*respawns ' + cat_bot.name + '*')

                elif (command == 'meow' and self.state == MEOW_CHOOSE_LANG):

                    # get available languages
                    languages = dialog.keys()

                    # prepare custom keyboard
                    choose_lang_keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, keyboard=[
                        [KeyboardButton(text=language)] for language in languages
                    ] + [[KeyboardButton(text='Nevermind')]])

                    response = 'Meow purr mrowww hisss?'
                    bot.sendMessage(chat_id, response, reply_markup=choose_lang_keyboard)

                    # move to next state
                    self.state = MEOW_CONFIRM_LANG

                    # terminate prematurely to avoid sending message twice
                    return

                # suggest the user to respawn the cat using /kitty
                if not (cat_bot.is_alive):
                    response += ' You can respawn your cat using the command /kitty.'
            else:

                # separates responses into before and after 'speak' has been called
                if (self.state > MEOW_CHOOSE_LANG):

                    # dialog variable placeholders
                    dialog_keyboard = None
                    dialog_response = ''

                    if (self.state == MEOW_CONFIRM_LANG):
                        if (msg_text != "Nevermind"):

                            # update context language for later re-use
                            self.language = msg_text

                            # load language dialog
                            language_dialog = dialog[self.language]

                            # prepare greeting and next keyboard
                            dialog_keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, keyboard=[
                                [KeyboardButton(text=language_dialog['yes'])], [KeyboardButton(text=language_dialog['no'])]
                            ])
                            dialog_response = language_dialog['greeting']

                            # move to next state
                            self.state = MEOW_LEAD_TOPIC

                        else:

                            # reset state when user cancels
                            self.state = MEOW_CHOOSE_LANG
                            dialog_response = 'Perhaps it\'s best to not think about it, eh?'

                    elif (self.state == MEOW_LEAD_TOPIC):

                        # load language dialog
                        language_dialog = dialog[self.language]

                        # get random sentiment
                        self.sentiment = random.randrange(2)

                        if (msg_text == language_dialog['yes']):

                            # prepare response and next keyboard
                            dialog_keyboard = ReplyKeyboardMarkup(one_time_keyboard=True, keyboard=[
                                [KeyboardButton(text=sentiment)] for sentiment in language_dialog['sentiments'].values()
                            ])

                            # get a random leading clause
                            dialog_response = random.choice(language_dialog['responses']['leading'])

                            # get a random topic
                            dialog_response += random.choice(sum(language_dialog['topics'].values(), [])) + '?'

                            # move to next state
                            self.state = MEOW_REACT_SENTIMENT

                        else:

                            # reset state when user cancels
                            self.state = MEOW_CHOOSE_LANG
                            dialog_response = 'That\'s a shame.'

                    elif (self.state == MEOW_REACT_SENTIMENT):

                        # load language dialog
                        language_dialog = dialog[self.language]

                        if (msg_text != language_dialog['sentiments']['cancel']):

                            # get numeric value of user answer
                            answer = [language_dialog['sentiments']['good'],
                            language_dialog['sentiments']['meh'],
                            language_dialog['sentiments']['bad']].index(msg_text)

                            # prepare random response accordingly if user's answer matches bot's sentiment
                            responses = language_dialog['responses']['good' if self.sentiment == answer else 'bad']
                            dialog_response = random.choice(responses)

                        else:

                            # prepare different response when user cancels
                            dialog_response = "Was it all a dream? You could have sworn that cat just spoke to you..."

                        # reset state either way
                        self.state = MEOW_CHOOSE_LANG

                    bot.sendMessage(chat_id, dialog_response, reply_markup=dialog_keyboard)
                    return

                else:
                    # talk to the cat if no command was matched and 'meow' not initialized
                    response = cat_bot.chat()

        # send the response
        bot.sendMessage(chat_id, response)

    def on_callback_query(self, msg):
        global cat_bot
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

        # close inline keyboard
        inline_message_id = msg['message']['chat']['id'], msg['message']['message_id']
        bot.editMessageReplyMarkup(inline_message_id, reply_markup=None)

        # kill cat (brutally) on confirm
        if (query_data == 'kitty-confirm'):
            bot.sendMessage(from_id, 'Meow!!!')
            bot.sendMessage(from_id, '*scratches your face*')
            bot.sendMessage(from_id, cat_bot.name + ' was killed.')

            #respawn cat
            cat_bot.kill()
            bot.sendMessage(from_id, '*respawns ' + cat_bot.name + '*')
        else:
            bot.sendMessage(from_id, text='Meowww~~~')
            bot.sendMessage(from_id, text='*licks your face*')

        # answer callback query or else telegram will forever wait on this
        bot.answerCallbackQuery(query_id)

# bootstrap the bot and spawn the cat
bot = DelegatorBot(TOKEN, [
    pave_event_space()
    (per_chat_id(), create_open, CatBot, timeout=100)
])
MessageLoop(bot).run_as_thread()

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
