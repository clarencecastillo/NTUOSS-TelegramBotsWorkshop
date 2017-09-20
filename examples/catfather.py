
import sys
import datetime
import telepot
import random
import time

from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from telepot.delegate import pave_event_space, per_chat_id, create_open


TOKEN = ''


number = 1
tasks = [0,0,0,0,0]
task0 = 0
task1 = 0
task2 = 0
task3 = 0
task4 = 0
text0 = ''
text1 = ''
text2 = ''
text3 = ''
text4 = ''
users = []
names = []


class MessageCounter(telepot.helper.ChatHandler):



    count = 0
    text0 = 'Finished Task 0'
    text1 = 'Finished Task 1'
    text2 = 'Finished Task 2'
    text3 = 'Finished Task 3'
    text4 = 'Finished Task 4'

    gname_dict = {
        'a': 'Fluffy',
        'n': 'Cuddles',
        'b': 'Banana',
        'o': 'Sparkly',
        'c': 'Rainbow',
        'p': 'Fatty',
        'd': 'Mainbitch',
        'q': 'Querty',
        'e': 'Buddy',
        'r': 'Hairy',
        'f': 'Kissy',
        's': 'Sassy',
        'g': 'Bitchy',
        't': 'Motherfucker',
        'h': 'Kitty',
        'u': 'Cutiepie',
        'i': 'Handsome',
        'v': 'Scratchy',
        'j': 'Stormy',
        'w': 'Moon',
        'k': 'Pussy',
        'x': 'Pouncey',
        'l': 'Spiderpig',
        'y': 'Lucky',
        'm': 'Midnight',
        'z': 'Snowy'
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
        self.line = ''

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
        global number
        global tasks
        global task0
        global task1
        global task2
        global task3
        global task4
        global users
        global names
        
        self.count += 10
        

        chat_id = msg['chat']['id']
        command = msg['text'].lower()

        self.line += command
        self.line += ','

        print(command)

        if self.count == 10:
            bot.sendMessage(chat_id, "What is your Matriculation number? (string)")

        elif self.count == 20:
            self.catname += self.matric_list[self.matricHandle(command)]
            self.catname += ' '
            bot.sendMessage(chat_id, "What is your family name? (string)")

        elif self.count == 30:
            self.catname += self.gname_dict[self.gnameHandle(command)]
            self.catname += ' '
            bot.sendMessage(chat_id, "Next, what is you DAY of birth? (int)")

        elif self.count == 40:
            self.bdayHandle(command)
            bot.sendMessage(chat_id, "And finally, what is your GPA? (float)")

        elif self.count == 50:
            self.catname += self.gpa_list[self.gpaHandle(command)]
            markup = ReplyKeyboardMarkup(one_time_keyboard=True,keyboard=[
                [KeyboardButton(text='Nice! My totally not imaginary friends will be pleased.')],
                [KeyboardButton(text='Wait a minute! Let me do over.')]
            ])
            bot.sendMessage(chat_id, "Your cat name is " + self.catname +
                            ". Go tell your friends about it, if you have any hahaha",
                            reply_markup=markup)
            f = open("people.csv", "a")
            f.write(self.line+'\n')
            f.close()
            self.line = ''

        elif self.count == 60:
            if command == 'Nice! My totally not imaginary friends will be pleased.'.lower():
                if chat_id not in users:
                    users.append(chat_id)
                    number += 1;
                markup = ReplyKeyboardMarkup(one_time_keyboard=True,keyboard=[
                    [KeyboardButton(text='Finished Task 0')],
                    [KeyboardButton(text='Finished Task 1')],
                    [KeyboardButton(text='Finished Task 2')],
                    [KeyboardButton(text='Finished Task 3')],
                    [KeyboardButton(text='Finished Task 4')]
                ])
                bot.sendMessage(chat_id, "Okay, let's get started with the tasks!\n\
                    Click on a task when you're done.", reply_markup=markup)
            elif command == 'Wait a minute! Let me do over.'.lower():
                bot.sendMessage(chat_id, "Sure, take your time." )
                self.count = 0
            else:
                self.count -= 10
        elif self.count > 60:
            if command == 'Wait a minute! Let me do over.'.lower():
                bot.sendMessage(chat_id, "Sure, take your time." )
                self.count = 0
            else:
                if command == 'Finished Task 1'.lower():
                    self.text1 = 'Undo Task 1'
                    tasks[1] = tasks[1] + 1
                elif command == 'Undo Task 1'.lower():
                    self.text1 = 'Finished Task 1'
                    tasks[1] = tasks[1] - 1
                elif command == 'Finished Task 2'.lower():
                    self.text2 = 'Undo Task 2'
                    tasks[2] = tasks[2] + 1
                elif command == 'Undo Task 2'.lower():
                    self.text2 = 'Finished Task 2'
                    tasks[2] = tasks[2] - 1
                elif command == 'Finished Task 3'.lower():
                    self.text3 = 'Undo Task 3'
                    tasks[3] = tasks[3] + 1
                elif command == 'Undo Task 3'.lower():
                    self.text3 = 'Finished Task 3'
                    tasks[3] = tasks[3] - 1
                elif command == 'Finished Task 0'.lower():
                    self.text0 = 'Undo Task 0'
                    tasks[0] = tasks[0] + 1
                elif command == 'Undo Task 0'.lower():
                    self.text0 = 'Finished Task 0'
                    tasks[0] = tasks[0] - 1
                elif command == 'Finished Task 4'.lower():
                    self.text4 = 'Undo Task 4'
                    tasks[4] = tasks[4] + 1
                elif command == 'Undo Task 4'.lower():
                    self.text4 = 'Finished Task 4'
                    tasks[4] = tasks[4] - 1


                markup = ReplyKeyboardMarkup(one_time_keyboard=True,keyboard=[
                    [KeyboardButton(text=self.text0)],
                    [KeyboardButton(text=self.text1)],
                    [KeyboardButton(text=self.text2)],
                    [KeyboardButton(text=self.text3)],
                    [KeyboardButton(text=self.text4)]
                ])
                bot.sendMessage(chat_id, "Okay, let's get started with the tasks!\n\
                    Click on a task when you're done.", reply_markup=markup)

            


bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(per_chat_id(), create_open, MessageCounter, timeout=100),])

MessageLoop(bot).run_as_thread()

line = ''
line += (('+' + '-'*8)*5 + '+\n')
line += (('|' + ' '*8)*5 + '|\n')
line += ('| Task 0 | Task 1 | Task 2 | Task 3 | Task 4 |\n')
line += (('|' + ' '*8)*5 + '|\n')
line += (('+' + '-'*8)*5 + '+\n')

c = open("tasks.csv", "a")
c.write('Task 1,Task 2,Task 3,Task 4,Task 5\n')
c.close

while True:
    cline = ''
    time.sleep(5)
    print('update')
    for x in tasks:
        line += ('|{0:5}   '.format(x))
        cline += str(x) + ','
    line += '|\n'
    cline += '\n'
    
    line += (('+' + '-'*8)*5 + '+\n')
    for x in tasks:
        n = x/number*100
        line += ('| {:5.1f}% '.format(n))
    line += '|\n'
    
    line += (('+' + '-'*8)*5 + '+\n')
    f = open("people.txt", "w")
    f.write(line)
    f.close()

    c = open("tasks.csv", "a")
    c.write(cline)
    c.close()
    

    
