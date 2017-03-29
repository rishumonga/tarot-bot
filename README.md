# Simple Telegram ChatBot for Tarot cards readings.

---

The whole project is implemented in one file [`tarot-bot.py`](./tarot-bot.py). 

## Create Bot on Telegram

Go to [Telegram API](https://core.telegram.org/api#getting-started) and follow
instructions under "Obtaining api_id".

Use the following commands with BotFather to configure your bot:

* /setdescription
* /setabouttext
* /setuserpic
* /setjoingroups
* /setinline
* /setcommands

## Python Prerequisites:

pip install telepot

pip install jsonpickle

pip install transitions

## How to run

The bot takes 3 arguments (in this order):

* TOKEN -- api_id from Telegram API
* GMAILuser -- gmail account to use to send emails out (check Gmail guide on security for smtp outgoing use)
* GMAILpwd -- gmail account password

