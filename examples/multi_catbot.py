

import time
import requests
import random
import random
from bs4 import BeautifulSoup

import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.delegate import pave_event_space, per_chat_id, create_open

from cat import Cat

TOKEN = ''


# Texts for responding to users
# You should write your own
eng_badlist = ['Hitler', 'Donald Trump', 'human suffering', 'dogs', 'rats', 'insurance fraud', 'the police']
ger_badlist = ['Hitler', 'Donald Trump', 'diktaturen', 'hund', 'ratten', 'versicherungsbetrug']
spa_badlist = ['Hitler', 'Donald Trump', 'muerte', 'perros', 'ratas', 'fraude de seguro', 'los policia']

eng_mehlist = ['homeless people', 'true love', 'pants', 'rain', 'vegans', 'Swedish people']
ger_mehlist = ['liebe', 'Donald Trump', 'ein schone frau', 'dogs', 'rats', 'insurance fraud']
spa_mehlist = ['amor', 'veganos', 'pantalones', 'dogs', 'illuvia', 'carteles de drogas']

eng_goodlist = ['cats', 'the Simpsons', 'flamingoes', 'drug money', 'fire', 'death', 'Tom Cruise', 'burritos']
ger_goodlist = ['weiss bier', 'der Simpsons', 'sorgfaltig gefertigte witze', 'fussball', 'schnitzel', 'feuer', 'Tom Cruise']
spa_goodlist = ['gato', 'pollos', 'fuego', 'el jefe', 'flamencos', 'biblioteca', 'los Simpsons', 'Tom Cruise']

englist = [eng_goodlist,eng_mehlist,eng_badlist]
spalist = [spa_goodlist,spa_mehlist,spa_badlist]
gerlist = [ger_goodlist,ger_mehlist,ger_badlist]

eng_prompt = ["Very good! Let's see... What do you think of ",
                "Excellent. Now, what do you say about ",
                "That is well. Come, let's hear your thoughts on ",
                "Indeed. May I ask for your opinion on "]
spa_prompt = ["Salud! Que piensas de ",
                "Buenos dias! Quiero tu opinion sobre ",
                "Que bueno oirlo! Cuales son tus pensamientos sobre ",
                "Y lo que piensas sobre "]
ger_prompt = ["Und was du denkst uber ",
                "Guten tag! Ich mochte deine Meinung zu ",
                "Bitte, ich möchte deine Gedanken hören ",
                "Jetzt, was sagst du über "]

eng_goodresp = ["Impeccable",
                "Couldn't say it better meself.",
                "That's right!",
                "Yes, I have finally found someone who thinks the way I do.",
                "Couldn't agree more.",
                "My whiskers are twitching in vehemont agreement."]
ger_goodresp = ["Ach, das ist gut.",
                "Ja, das ist richtig,",
                "Mein gott! Ich zustimmen.",
                "Du sprichst die Wahrheit."]
spa_goodresp = ["Oh, eso es bueno,",
                "Sí, eso es correcto",
                "Dios mío, estoy de acuerdo.",
                "Hablas la verdad."]

eng_badresp = ["You disgust me.",
                "Now even I wouldn't stoop so low",
                "You disappoint me.",
                "If I had never felt shame before, I'm sure I do now.",
                "You're a SOB.",
                "You're a POS."
                ]
ger_badresp = ["Du widerst mich an.",
                 "Jetzt würde ich auch nicht so tief bücken",
                 "Du enttäuschst mich.",
                 "Wenn ich noch nie Schande gehabt hätte, bin ich mir sicher, dass ich es jetzt mache.",
                 "Du bist ein hurensohn.",
                 "Du bist scheisse."
                 ]
spa_badresp = ["Me das asco.",
                 "Ahora ni siquiera me inclinaría tan bajo",
                 "Me decepcionas.",
                 "Si nunca antes había sentido vergüenza, estoy seguro de que lo haré ahora.",
                 "Eres un hijo de puta.",
                 "Eres un cagada."
                 ]

class MessageCounter(telepot.helper.ChatHandler):


   def __init__(self, *args, **kwargs):
      super(MessageCounter, self).__init__(*args, **kwargs)
      self.state = 0
      self.language = ''
      self.feel = 0
      self.ans = 0


   # TODO: Get Random Cat Fact
   def get_random_cat_fact(self):
       rand_cat_fact_url = 'https://catfact.ninja/fact'
       response = requests.get(rand_cat_fact_url).json()
       return response['fact']

   # TODO: Get Random Cat Image URL
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
       print(self.state)
       global cat_bot
       content_type, chat_type, chat_id = telepot.glance(msg)

       # TODO: Create Hello World

       # default response (feel free to change it)
       response = 'Meow!'

       # handle only messages with text content
       if content_type == 'text':

           # get message payload
           msg_text = msg['text']
           msg_sender = msg['from']['username']
           print('Received: "' + msg_text + '" from ' + msg_sender)

           # TODO: Implement Command Handling
           if (msg_text.startswith('/')):

               # parse the command excluding the '/' and other arguments
               command = msg_text[1:].lower().split()[0]

               # prepare the correct response given the command
               if (command == 'ask'):

                   # prepare response with random cat fact if cat is alive
                   if (cat_bot.is_alive):
                       response = 'Meow! ' + self.get_random_cat_fact()
                   else:
                       response = 'This cat is currently unavailable.'
               elif (command == 'status'):
                   # TODO: Send User Random Cat Image
                   bot.sendChatAction(chat_id, 'upload_photo')
                   bot.sendPhoto(chat_id, self.get_random_cat_image_url())
                   response = cat_bot.get_status()
               elif (command == 'feed'):
                   response = cat_bot.feed()
               elif (command == 'clean'):
                   response = cat_bot.clean()
               elif (command == 'kitty'):

                   if (cat_bot.is_alive):

                       # prepare confirm keyboard
                       confirm_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                           [InlineKeyboardButton(text='Confirm', callback_data='kitty-confirm')],
                           [InlineKeyboardButton(text='Cancel', callback_data='kitty-cancel')],
                       ])

                       # send response with keyboard
                       response += ' Warning: ' + cat_bot.name + ' is still alive. Issuing this command will kill the cat (brutally) and reset all progress. Please confirm your action.'
                       bot.sendMessage(chat_id, response, reply_markup = confirm_keyboard)
                       return # prematurely terminate function call to await user response

                   else:

                       # respawn cat
                       cat_bot = Cat(bot_name)
                       bot.sendMessage(chat_id, '*respawns ' + cat_bot.name + '*')



               # begin interaction with saved states with 'speak' command

               elif (command == 'speak' and self.state == 0):
                   self.state = 10

                   # prepares a custom keyboard
                   markup = ReplyKeyboardMarkup(one_time_keyboard=True,keyboard=[
                       [KeyboardButton(text='English')], [KeyboardButton(text='Spanish')],
                       [KeyboardButton(text='German')], [KeyboardButton(text='Nevermind')]
                   ])
                   bot.sendMessage(chat_id, 'Meow meow mrow hisss:\n1. English\
                   \n2. Spanish\n3. German', reply_markup=markup)




               # suggest the user to respawn the cat using /kitty
               if not (cat_bot.is_alive):
                   response += ' You can respawn your cat using the command /kitty.'
           else:

               # TODO: insert interactions with various states (0 to 30)

               # separates responses into before and after 'speak' has been called
               if (self.state > 0):
                   command = msg_text.lower()

                   # TODO: insert code for state 10

                   # first state after initialisation, assign language based on
                   # user choice
                   if (self.state == 10):
                       if (command != "nevermind"):
                           if (command == "english"):
                               self.language = 'eng'
                               self.state = 20
                               markup = ReplyKeyboardMarkup(one_time_keyboard=True,keyboard=[
                                   [KeyboardButton(text='I am indeed')], [KeyboardButton(text='Nope')]
                               ])
                               resp = "Well met! Ah, a fellow purveyor of the Anglo-Saxon tongue, I see."
                           elif (command == "spanish"):
                               self.language = 'spa'
                               self.state = 20
                               markup = ReplyKeyboardMarkup(one_time_keyboard=True,keyboard=[
                                   [KeyboardButton(text='Si senor')], [KeyboardButton(text='No se')]
                               ])
                               resp = "Hola mi amigo! Parece que hablas espanol. Te gustaria hablar conmigo?"

                           elif (command == "german"):
                               self.language = 'ger'
                               self.state = 20
                               markup = ReplyKeyboardMarkup(one_time_keyboard=True,keyboard=[
                                   [KeyboardButton(text='Ja')], [KeyboardButton(text='Nein')]
                               ])
                               resp = "Heute Deutschland, morgen die ganze welt! Warte, ich scherze nur! Komm zuruck!"
                           bot.sendMessage(chat_id, resp, reply_markup=markup)
                       else:
                           self.state = 0
                           resp = "*perhaps it's best to not think about it, eh?"
                           bot.sendMessage(chat_id, resp)

                   # TODO: add in code for state 20

                   # second state after initialisation, takes in user input and asks
                   # a question accordingly
                   elif (self.state == 20):
                       resp = ''
                       self.feel = random.randrange(3)
                       if (self.language == 'eng'):
                           if (command == 'i am indeed'):
                               self.state = 30
                               markup = ReplyKeyboardMarkup(one_time_keyboard=True,keyboard=[
                                   [KeyboardButton(text='I love it')], [KeyboardButton(text='Meh')],
                                   [KeyboardButton(text='I hate it')], [KeyboardButton(text='I want out')]
                               ])
                               resp += random.choice(eng_prompt)
                               resp += random.choice(englist[self.feel])
                               resp += '?'
                               bot.sendMessage(chat_id, resp, reply_markup=markup)
                           else:
                               self.state = 0
                               resp = "That's a shame."
                               bot.sendMessage(chat_id, resp)
                       elif (self.language == 'ger'):
                           if (command == 'ja'):
                               self.state = 30
                               markup = ReplyKeyboardMarkup(one_time_keyboard=True,keyboard=[
                                   [KeyboardButton(text='Ich liebe es')], [KeyboardButton(text='Meh')],
                                   [KeyboardButton(text='Ich hasse es')], [KeyboardButton(text='Ich will gehen')]
                               ])
                               resp += random.choice(ger_prompt)
                               resp += random.choice(gerlist[self.feel])
                               resp += '?'
                               bot.sendMessage(chat_id, resp, reply_markup=markup)
                           else:
                               self.state = 0
                               resp = "Das ist zu schade."
                               bot.sendMessage(chat_id, resp)
                       elif (self.language == 'spa'):
                           if (command == 'si senor'):
                               self.state = 30
                               markup = ReplyKeyboardMarkup(one_time_keyboard=True,keyboard=[
                                   [KeyboardButton(text='Me gusta')], [KeyboardButton(text='Meh')],
                                   [KeyboardButton(text='No me gusta')], [KeyboardButton(text='Quiero irme')]
                               ])
                               resp += random.choice(spa_prompt)
                               resp += random.choice(spalist[self.feel])
                               resp += '?'
                               bot.sendMessage(chat_id, resp, reply_markup=markup)
                           else:
                               self.state = 0
                               resp = "Eso es muy malo."
                               bot.sendMessage(chat_id, resp)

                   # TODO: add in state 30

                   # third state after initialisation, takes in user input, remembers
                   # the previous question, and responds in the context of the question in the second state
                   elif (self.state == 30):
                       resp = ''
                       if (command == 'i love it' or command == 'ich liebe es' or command == 'me gusta'):
                           self.ans = 0
                       elif (command == 'meh'):
                           self.ans = 1
                       elif (command == 'i hate it' or command == 'ich hasse es' or command == 'no me gusta'):
                           self.ans = 2
                       else:
                           self.ans = 3

                       if (self.ans == 3):
                           self.state = 0
                           resp = "*Was it all a dream? You could have sworn that cat just spoke to you..."
                       else:
                           if self.language == 'eng':
                               if (self.feel == self.ans):
                                   resp = random.choice(eng_goodresp)
                               else:
                                   resp = random.choice(eng_badresp)
                           elif self.language == 'ger':
                               if (self.feel == self.ans):
                                   resp = random.choice(ger_goodresp)
                               else:
                                   resp = random.choice(ger_badresp)
                           elif self.language == 'spa':
                               if (self.feel == self.ans):
                                   resp = random.choice(spa_goodresp)
                               else:
                                   resp = random.choice(spa_badresp)
                           self.state = 0
                           bot.sendMessage(chat_id, resp)


               else:
                   # talk to the cat if no command was matched
                   # and 'speak' not initialised
                   response = cat_bot.chat()

       # send the response
       bot.sendMessage(chat_id, response)

       # TODO: Handle Callback Query

   def on_callback_query(self, msg):
       global cat_bot
       query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
       print('Callback Query:', query_id, from_id, query_data)

       # close inline keyboard
       inline_message_id = msg['message']['chat']['id'], msg['message']['message_id']
       bot.editMessageReplyMarkup(inline_message_id, reply_markup=None)

       # kill cat on confirm
       if (query_data == 'kitty-confirm'):
           cat_bot = Cat(bot_name)
           bot.sendMessage(from_id, 'Meow!!!')
           bot.sendMessage(from_id, '*scratches your face*')
           bot.sendMessage(from_id, cat_bot.name + ' was killed.')

           #respawn cat
           cat_bot = Cat(bot_name)
           bot.sendMessage(from_id, '*respawns ' + cat_bot.name + '*')
       else:
           bot.sendMessage(from_id, text='Meowww~~~')
           bot.sendMessage(from_id, text='*licks your face*')

       # answer callback query or else telegram will forever wait on this
       bot.answerCallbackQuery(query_id)



bot = telepot.DelegatorBot(TOKEN,
                           [pave_event_space()
                            (per_chat_id(),
                             create_open,
                             MessageCounter,
                             timeout=100),])



bot_name = bot.getMe()['first_name']
cat_bot = Cat(bot_name)

MessageLoop(bot).run_as_thread()

print('Meow! ' + bot_name + ' at your service...')

# keep the program running and simulate cat life
cat_last_update = time.time()
while True:
    print('yes')
    time.sleep(10)
    # update cat every 6 hours
    if (time.time() - cat_last_update > 24/4*60*60):
        cat_bot.on_update()
        cat_last_update = time.time()
