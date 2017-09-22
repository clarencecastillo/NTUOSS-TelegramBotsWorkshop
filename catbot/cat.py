# NTUOSS Telegram Bots Workshop
# 22 September 2017
# Speakers: Clarence Castillo & Steve Ye
# Repository: https://github.com/clarencecastillo/NTUOSS-TelegramBotsWorkshop

# ------------------------ DO NOT TOUCH THIS FILE ------------------------ #

import random, requests

MAX_HUNGER = 100
MIN_HUNGER = -100
FEED_AMOUNT = 50

MAX_DIRT = 100
MIN_DIRT = -100
CLEAN_AMOUNT = 50

CYCLES_PER_DAY = 4

DEAD_CAT_COUNTER_URL = 'http://05492820.ngrok.io'

class Cat(object):

    def __init__(self, name):
        self.name = name
        self.hunger = 0
        self.dirt = 0
        self.cycles_passed = 0
        self.is_alive = True

    def feed(self):
        response = ""
        if not (self.is_alive):
            response = self.name + " is not responding. Seems like dead cats don't like to eat food anymore."
        else:
            self.hunger -= FEED_AMOUNT
            if (self.hunger < MIN_HUNGER):
                self.is_alive = False
                response = self.name + " died of overeating. RIP (Rest In Pizza)."
            elif (self.hunger < 0):
                response = "Although " + self.name + " was't really that hungry, the cat ate the food anyway. Be careful not to feed the cat too much."
            else:
                response = "You fed " + self.name + ". Cat is appeased and is forever greatful."
        return response

    def clean(self):
        response = ""
        if (self.dirt < 0):
            response = self.name + " is already very clean. That last bath didn't really do much."
        elif (self.dirt > MAX_DIRT):
            response = self.name + " is still quite dirty. Please remember to take good care of your pet's hygiene."
        else:
            response = "You gave " + self.name + " a bath. Cat smells very good."
        self.dirt -= CLEAN_AMOUNT
        if (self.dirt < MIN_DIRT):
            self.dirt = MIN_DIRT
        return response

    def get_status(self):
        response = self.name + " is "
        if (self.is_alive):
            response += "doing well. The cat is " + str(self.cycles_passed/CYCLES_PER_DAY) + " days old."
            if (self.hunger > MAX_HUNGER / 2):
                response += " It is a little hungry. Perhaps it's about time to feed it."
            if (self.dirt > MAX_DIRT / 2):
                response += " It is a little dirty. Maybe it's time to give it a bath."
        else:
            response += "dead. There's nothing more that we can do about it."
        return response

    def on_update(self):
        if (self.is_alive):
            self.dirt += MAX_DIRT / CYCLES_PER_DAY
            if (self.dirt > MAX_DIRT):
                self.dirt = MAX_DIRT
            self.hunger += MAX_HUNGER / CYCLES_PER_DAY
            if (self.hunger >= MAX_HUNGER):
                self.is_alive = False
            self.cycles_passed += 1

    def chat(self):
        if (self.is_alive):
            return ("Meow " + "meow " * random.randint(0, 4)).strip() + random.choice(["?", "!", ".", "!!", "?!"])
        else:
            return "..."

    def kill(self):
        try:
            requests.get(DEAD_CAT_COUNTER_URL + 'kitty')
        except:
            pass
        self.__init__(self.name)
        return

# ------------------------ DO NOT TOUCH THIS FILE ------------------------ #
