import sys
import time
import threading

import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardHide, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent
from telepot.delegate import pave_event_space, per_chat_id, create_open


count = 0

users = []

class MessageCounter(telepot.helper.ChatHandler):
   def __init__(self, *args, **kwargs):
      super(MessageCounter, self).__init__(*args, **kwargs)


   def on_chat_message(self, msg):
      chat_id = msg['chat']['id']
      command = msg['text']

      global users
      global count
      
      if chat_id not in users:
         if command == 'y':
            users.append(chat_id)
            count += 1;
      print(count)
   


bot = telepot.DelegatorBot('274523344:AAHAfIUtQ_oP6noOeRgqgwBjNbTQN_cLi30', [
   pave_event_space()(
       per_chat_id(), create_open, MessageCounter, timeout=100),
])
bot.message_loop(run_forever='Listening ...')


