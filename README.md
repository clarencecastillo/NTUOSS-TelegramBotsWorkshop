# NTUOSS Telegram Bots Workshop

*by [Clarence Castillo](https://github.com/clarencecastillo) and [Steve Ye](https://github.com/HandsomeJeff) for NTU Open Source Society*

This workshop is based on [nickoala/telepot](https://github.com/nickoala/telepot) and assumes intermediate knowledge of Python.

**Disclaimer:** *This document is only meant to serve as a reference for the attendees of the workshop. It does not cover all the concepts or implementation details discussed during the actual workshop.*
___

### Workshop Details
**When**: Friday, 22 Sept 2017. 6:30 PM - 8:30 PM.</br>
**Where**: Theatre@TheNest, Innovation Centre, Nanyang Technological University</br>
**Who**: NTU Open Source Society

### Questions
Please raise your hand any time during the workshop or email your questions to [me](mailto:hello@clarencecastillo.me) later.

### Errors
For errors, typos or suggestions, please do not hesitate to [post an issue](https://github.com/clarencecastillo/NTUOSS-TelegramBotsWorkshop/issues/new). Pull requests are very welcome! Thanks!
___

## Index

Task 0 - Getting Started
    - 0.1 Introduction
    - 0.2 Initial Setup

___

## Task 0 - Getting Started

#### 0.1 Introduction

<!-- TODO: write about this workshop -->
<!-- TODO: write about telegram -->

For this tutorial, we'll be creating a *Cat Bot* which allows users to
1. get random facts about cats
2. get random cat pictures
3. talk to an actual cat *LIVE*\*

#### 0.2 Initial Setup

1.  Download a text editor of your choice. I strongly recommend either:
    1.  [Atom](https://atom.io/)
    2.  [Sublime Text 3](http://www.sublimetext.com/3)
    3.  [Brackets](http://brackets.io/)
2.  Download [this project](https://github.com/clarencecastillo/NTUOSS-TelegramBotsWorkshop/archive/master.zip) and unzip the folder to your preferred workspace to get started.
3.  Download [Telegram Desktop](https://desktop.telegram.org/) if you want easier access to quickly debug your bot.
4.  Download required Python 3.6.x packages:
    1.  [telepot](https://github.com/nickoala/telepot)
    2.  [requests](https://github.com/requests/requests)
    1.  [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/)

> **Note**<br>
> The easiest way to install python modules is via [pip](https://pypi.python.org/pypi/pip). Running this one-liner will install all of the required modules indicated above:
> <br>`pip install telepot requests beautifulsoup4`

## Task 1 - BotFather

#### 1.1 Name Your Cat Bot

Since we need unique names for our Cat Bots, you can name your bot after your very own cat (or the cat you've never had). That way, BotFather won't likely complain about reserved usernames. If you don't have a cat, I've compiled a *Cat Name Matrix* aka "What's Your Cat Name" that could help you name your cat bot:

**Step 1:** Sum of the digits in your Matriculation Number mod 10

| Number | Name | Number | Name |
| --- | --- | --- | --- |
| 0 | `Mister` | 5 | `Moon` |
| 1 | `Miss` | 6 | `Sir` |
| 2 | `Lord` | 7 | `Captain` |
| 3 | `Lady` | 8 | `General` |
| 4 | `Princess` | 9 | `Professor` |

<br>**Step 2:** First initial of your given name

| Letter | Name | Letter | Name |
| --- | --- | --- | --- |
| a | `Fluffy` | n | `Cuddles` |
| b | `Banana` | o | `Sparkly` |
| c | `Rainbow` | p | `Fatty` |
| d | `Mainbitch` | q | `Querty` |
| e | `Buddy` | r | `Hairy` |
| f | `Kissy` | s | `Sassy` |
| g | `Bitchy` | t | `Motherfucker` |
| h | `Kitty` | u | `Cutiepie` |
| i | `Handsome` | v | `Scratchy` |
| j | `Stormy` | w | `Moon` |
| k | `Pussy` | x | `Pouncey` |
| l | `Spiderpig` | y | `Lucky` |
| m | `Midnight` | z | `Snowy` |

<br>**Step 3:** Your GPA times your day of birth mod 10

| Digit | Name | Digit | Name |
| --- | --- | --- | --- |
| 0  | `Bellyrubs` | 5 | `Waggles` |
| 1 | `Purbox` | 6 | `Furface` |
| 2 | `Wiggles` | 7 | `Fluffles` |
| 3 | `Munchkin` | 8 | `Moon` |
| 4 | `Cheeks` | 9 | `Meowers` |

For example, if my matriculation number is U1359234X, my cat bot's honorific would be `Captain` as derived from `(1+3+5+9+2+3+4)%10 = 7` . Combined with my name's first initial `C` (which maps to `Rainbow`) and given my *5.0* GPA times the day of my birth 20, `5.0*20%10 = 0` (which maps to `Bellyrubs`), my cat bot's full name would be `Captain Rainbow Bellyrubs`. Consequently, my cat bot's username would be `captainrainbowbellyrubscatbot`.

#### 1.2 Acquire Telegram HTTP API Token

Once we've got our Cat Bot name settled, the next step is to acquire a token from Telegram. To do this, we need to let BotFather know that we want to create a bot. Open Telegram and search for *BotFather* in the contacts search field. Ask it to register a new bot for you by sending the command `/newbot` after which it'll ask you for your bot's name and username.

![task 1.2 screenshot](screenshots/task_1_2.png?raw=true)

Take note of our new bot's token to access Telegram's HTTP API as we'll need it in the code we're about to write so we can tell Telegram the behavior of our cat bot.

The token should look something like this:

```
2351749591:VskzWEJdWj_rlCx23Hyu5mIJdWjTVskzdEx
```

#### 1.3 Meow! Hello World

![task 1.3 screenshot a](screenshots/task_1_3_a.png?raw=true)

Now that we got everything we need to start developing our bot, let's start programming to define the behavioral aspects of our Cat Bot. To start off, open `catbot/catbot.py` on your text editor and paste following on the line indicated within `def on_chat_message(msg)`:

```python
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
    response += ' Hi ' + msg_sender + '. Hello world! '

# send the response
bot.sendMessage(chat_id, response)
```

Don't forget to add in our bot's API token:
```python
# TODO: Replace Token

TOKEN = '2351749591:VskzWEJdWj_rlCx23Hyu5mIJdWjTVskzdEx'
```

Let's bring our bot to life by running it. If you didn't get any errors this far, you should be able to test your bot by talking to it via Telegram Desktop. Enter your bot's username in the contacts search field and press `start` to begin the conversation. Remember that bots cannot initiate conversations with users so you have to send it a message first.

Assuming you did not make any changes to the `response` variable, the bot should respond with `Meow! Hi <username>. Hello world!` and your message should be printed on the terminal.

![task 1.3 screenshot b](screenshots/task_1_3_b.png?raw=true)

## Task 2 - Handling Message Events

#### 2.1 Commands

When processing a message, few pieces of information are presented which we will be using to determine the *intention* of the user. Much like instructions that you give to your cat (e.g. `sit`, `fetch` or `bark`), **commands** present a flexible yet semantic way to communicate with your bot. The following syntax may be used:

```
/command [optional] [argument]
```

As you may have noticed, commands start with `/` and may contain latin letters, numbers and underscores. We can suggest to the user what commands our bot understands by providing this information to BotFather. Doing so enables command suggestions where typing a `/` shows the user a list of available commands (more on this later).

For this section, we'll program our cat bot such that it would be able to recognize and behave *differently* provided the following commands:

| Command | Description |
| --- | --- |
| `/ask` | This command returns a random fact about cats. |
| `/status` | This command returns the status of the cat together with a random picture of it. |
| `/feed` | This command returns the response of the cat after feeding it. |
| `/clean` | This command returns the response of the cat after bathing it. |
| `/kitty` | This command murders your current cat if it's still alive and spawns you a new kitten. |

For this tutorial, we will be using a *very sophisticated* cat simulator class which has already been coded for us. You're free to explore the codes inside `catbot/cat.py` for personal learning, but it would be beyond the scope of this workshop. For now, use the information below as reference of the commands made available to us to use when interfacing with an instance of the Cat class.

-   Attributes:
    -   `name (str)`: Name of cat
    -   `hunger (int)`: Tracks how hungry the cat is (-100 to 100)
    -   `dirt (int)`: Tracks how dirty the cat is (-100 to 100)
    -   `cycles_passed (int)`: Tracks how many cycles (updates) the cat has been through
    -   `is_alive (bool)`: Indicates whether the cat is still alive

-   Methods:
    -   `get_status()`: Returns the cat's age, needs and whether if it's still alive
    -   `feed()`: Feeds the cat (hunger - 25); returns the cat's response after feeding
    -   `clean()`: Cleans the cat (dirt - 25); returns the cat's response after cleaning
    -   `chat()`: Returns a hyper realistic cat response

The idea is to take care of a simulated cat using our bot. The cat's behavior and states have already been taken care of by `cat.py`, so the only thing left for us to do is to link the class' methods to our `on_chat_message` function. Our user would then be able to *take care* of the cat via the commands provided.

![task 2.1 screenshot a](screenshots/task_2_1_a.png?raw=true)

Let's update our code by adding logic which would route the program flow according to the user's command.

```python
# TODO: Implement Command Handling

if (msg_text.startswith('/')):

    # parse the command excluding the '/' and other arguments
    command = msg_text[1:].lower().split()[0]

    # prepare the correct response given the command
    if (command == 'ask'):
        response = 'Meow? *licks paws*'
    elif (command == 'status'):
        response = cat_bot.get_status()
    elif (command == 'feed'):
        response = cat_bot.feed()
    elif (command == 'clean'):
        response = cat_bot.clean()
    elif (command == 'kitty'):

        # TODO: Confirm User Action Using Keyboard

        # kill cat if still alive
        if (cat_bot.is_alive):
            bot.sendMessage(chat_id, 'Meow! *scratches your face*')
            bot.sendMessage(chat_id, cat_bot.name + ' was killed.')

        # respawn cat
        cat_bot = Cat(bot_name)
        bot.sendMessage(chat_id, '*respawns ' + cat_bot.name + '*')

    # suggest the user to respawn the cat using /kitty
    if not (cat_bot.is_alive):
        response += ' You can respawn your cat using the command /kitty.'
else:

    # talk to the cat if no command was matched
    response = cat_bot.chat()
```

With reference to how we handle `/kitty`, notice that we can actually send multiple messages to the user within the context of a single message event. Since telepot's default implementation is *synchronous*, the user will still receive the messages in the very same order we're sending them.

![task 2.1 screenshot b](screenshots/task_2_1_b.png?raw=true)

#### 2.2 Keyboards

Besides receiving, parsing and sending message back and forth, Telegram Bots allow richer interactions with the user using keyboards. To prevent our user from *accidentally* `/kitty`-ing our live cat, we can prompt the user again to confirm this action. To do this, let's add an **Inline Keyboard** which we could use to prompt the user to confirm his/her action.

With reference to the clause where `# TODO: Confirm User Action Using Keyboard` is at, replace everything under that with with the following:

```python

# TODO: Confirm User Action Using Keyboard

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
```

While you're at it, don't forget to import `InlineKeyboardMarkup` and `InlineKeyboardButton` from `telepot.namedtuple` at the beginning of our code:

```python
# TODO: Import Keyboards

from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
```

To handle the inline keyboard *on press* event, let's add some logic to our `on_callback_query` which would be called whenever the user presses any buttons on our custom keyboard. Paste the following right where `# TODO: Handle Callback Query` is at:

```python
# TODO: Handle Callback Query

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
```

## Task 3 - Dynamic Content

#### 3.1 APIs

#### 3.2 Web Scraping

#### 3.3 Asynchronous

## Task 4 - Deployment

#### 4.1 Git

#### 4.2 Heroku
