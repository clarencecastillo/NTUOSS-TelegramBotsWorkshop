
import sys
import datetime
import telepot
import random
import time

from telepot.delegate import pave_event_space, per_chat_id, create_open

class MessageCounter(telepot.helper.ChatHandler):
    count = 0

    gname_dict = {
    'a':        'Fluffy',
    'n':	'Cuddles',
    'b':	'Banana',
    'o':	'Sparkly',
    'c':	'Rainbow',
    'p':	'Fatty',
    'd':	'Mainbitch',
    'q':	'Querty',
    'e':	'Buddy',
    'r':	'Hairy',
    'f':	'Kissy',
    's':	'Sassy',
    'g':	'Bitchy',
    't':	'Motherfucker',
    'h':	'Kitty',
    'u':	'Cutiepie',
    'i':	'Handsome',
    'v':	'Scratchy',
    'j':	'Stormy',
    'w':	'Moon',
    'k':	'Pussy',
    'x':	'Pouncey',
    'l':	'Spiderpig',
    'y':	'Lucky',
    'm':	'Midnight',
    'z':	'Snowy'
    }
   
    matric_list = ['Mister', 'Moon', 'Miss', 'Sir',
                  'Lord', 'Captain', 'Lady', 'General',
                  'Princess', 'Professor']

    gpa_list = ['Bellyrubs', 'Waggles', 'Purbox', 'Furface',
               'Wiggles', 'Fluffles', 'Munchkin', 'Moon',
               'Cheeks', 'Meowers']


   
    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)
        self.catname = ''
        self.daybirth = 2

    def matricHandle(self, matric):
        sum = 0
        for letter in matric:
            if letter.isdigit():
                sum += int(letter)
        return(sum % 10)

    def gnameHandle(self, gname):
        if gname[0] in self.gname_dict:
            return gname[0]
        else:
            return 't'

    def bdayHandle(self, day):
        try:
            self.daybirth = int(day)
        except:
            pass
    
    def gpaHandle(self, gpa):
        try:
            gpa = float(gpa)
        except:
            gpa = 4.0
        return int(gpa * self.daybirth) % 10

    def on_chat_message(self, msg):
        self.count += 10
        
        chat_id = msg['chat']['id']
        command = msg['text'].lower()

        print(command)

        if self.count <= 10:
            bot.sendMessage(chat_id, "What is your Matriculation number? (string)")

        elif 10 < self.count <= 20:
            self.catname += self.matric_list[self.matricHandle(command)]
            self.catname += ' '
            bot.sendMessage(chat_id, "What is your family name? (string)")

        elif 20 < self.count <= 30:
            self.catname += self.gname_dict[self.gnameHandle(command)]
            self.catname += ' '
            bot.sendMessage(chat_id, "Next, what is you DAY of birth? (int)")

        elif 30 < self.count <= 40:
            self.bdayHandle(command)
            bot.sendMessage(chat_id, "And finally, what is your GPA? (float)")

        elif self.count > 40:
            self.catname += self.gpa_list[self.gpaHandle(command)]
            bot.sendMessage(chat_id, "Your cat name is " + self.catname +
                            ". Go tell your friends about it, if you have any hahaha")
            self.count = 0


      
        


bot = telepot.DelegatorBot('432090010:AAF2aLZ3o2VWtb-JGT2X7rSsn1fTcTMRigE', [
    pave_event_space()(per_chat_id(), create_open, MessageCounter, timeout=100),])
bot.message_loop(run_forever='Listening ...')
