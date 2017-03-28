import sys
import telepot
from pprint import pprint
import datetime
import time
import random
import io
from PIL import Image
import jsonpickle
from transitions import Machine, State, Transition
import logging
from transitions import logger
import traceback

import smtplib


logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
#logger.setLevel(logging.INFO)
#logger.addHandler(consoleHandler)


def send_email(user, pwd, recipient, subject, body):
  gmail_user = user
  gmail_pwd = pwd
  FROM = user
  TO = recipient if type(recipient) is list else [recipient]
  SUBJECT = subject
  TEXT = body

  # Prepare actual message
  message = """From: %s\nTo: %s\nSubject: %s\n\n%s
  """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
  try:
    server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server_ssl.ehlo()  # optional, called by login()
    server_ssl.login(gmail_user, gmail_pwd)
    server_ssl.sendmail(FROM, TO, message)
    server_ssl.close()

  except Exception as e:
    print ( "failed to send mail " + e )



class Card:
  def __init__(self):
    self.number = None
    self.suit = None
    self.name = None
    self.image = None
    self.image_down = None
    self.teleimage_up = None
    self.teleimage_down = None
    self.description = None
    self.meaning_up_short = None
    self.meaning_down_short = None
    self.meaning_up = None
    self.meaning_down = None

def readfile(fname, mode):
  if (mode == 'rb'):
    f = open(fname, mode)
  else:
    f = open(fname, mode, encoding='utf-8')
  c = f.read()
  f.close()
  return c


def load_suit(suit, folder, length):
  for j in range(0,length):
    c = Card()
    c.number = j
    c.suit = suit
    c.name = readfile(folder+str(j)+'-name.txt','r')
    c.image = readfile(folder+str(j)+'.jpg','rb')
    out = io.BytesIO()
    Image.open(io.BytesIO(c.image)).rotate(180).save(out, format='JPEG')
    c.image_down = out.getvalue()
    out.close()    
    c.description = readfile(folder+str(j)+'-desc.txt','r')
    c.meaning_up_short = readfile(folder+str(j)+'-short-u.txt','r')
    c.meaning_down_short = readfile(folder+str(j)+'-short-r.txt','r')
    c.meaning_up = readfile(folder+str(j)+'-umean.txt','r')
    c.meaning_down = readfile(folder+str(j)+'-rmean.txt','r')
    deck.append(c)

def load_cards():
  deck.clear()
  load_suit('major',     'c/',  22)
  load_suit('cups',      'c1/', 14)
  load_suit('pentacles', 'c2/', 14)
  load_suit('swords',    'c3/', 14)
  load_suit('wands',     'c4/', 14)

def pull_card(full_deck=True, reversed=True):
  if full_deck:
    m = len(deck)
  else:
    m = 21 # just major arcana
  card =  random.randint(0,m)
  if reversed==False:
    res = {'n': card, 'card': deck[card], 'reversed': False}
  elif random.randint(0,1)==0:    
    res = {'n': card, 'card': deck[card], 'reversed': False}
  else:
    res = {'n': card, 'card': deck[card], 'reversed': True}
  return res

def logmsg(msg):
  f = open('msg.log','a')
  f.write('%s\n' % datetime.datetime.now()) 
  pprint(msg, stream=f)
  f.close()

def log_err(e):
  s = '%s\n' % datetime.datetime.now()
  s += traceback.format_exc() + '\n'
  f = open('error.log','a')
  f.write(s)
  f.close()
  send_email(GMAILuser, GMAILpwd, "alexey.simonov@gmail.com", "error in tarot bot", s)



def reply_tarot(userid, userfname, msg):
  full_deck = True
  reversed = True
  card = pull_card(full_deck, reversed)
  # pic
  if card['reversed']:
    if (card['card'].teleimage_down==None):
      f = io.BytesIO(card['card'].image_down)
      f.name = card['card'].name+'_reversed.jpg'
      r = bot.sendPhoto(userid, f)
      f.close()
    else:
      r = bot.sendPhoto(userid, card['card'].teleimage_down)
  else:
    if (card['card'].teleimage_up==None):
      f = io.BytesIO(card['card'].image)
      f.name = card['card'].name+'.jpg'
      r = bot.sendPhoto(userid, f)
      f.close()
    else:
      r = bot.sendPhoto(userid, card['card'].teleimage_up)
  #pprint(response)
  logmsg(r)
  if (card['reversed'] & (card['card'].teleimage_down==None)):
    card['card'].teleimage_down = r['photo'][2]['file_id']
  elif (card['reversed']==False & (card['card'].teleimage_up==None)):
    card['card'].teleimage_down = r['photo'][2]['file_id']
  # name
  if card['reversed']:
    r = bot.sendMessage(userid, '*' + card['card'].name + '* (reversed)', parse_mode='markdown')
  else:
    r = bot.sendMessage(userid, '*' + card['card'].name + '* (upright)', parse_mode='markdown')
  logmsg(r)
  if card['reversed']:
    r = bot.sendMessage(userid, '*Keywords: * _' + card['card'].meaning_down_short + '_', parse_mode='markdown')
  else:
    r = bot.sendMessage(userid, '*Keywords: * _' + card['card'].meaning_up_short + '_', parse_mode='markdown')
  r = bot.sendMessage(userid, '*Description: *' + card['card'].description, parse_mode='markdown')
  if card['reversed']:
    r = sendLongMessageInManyParts(bot, userid, '*Meanings: *' + card['card'].meaning_down, parse_mode='markdown')
  else:
    r = sendLongMessageInManyParts(bot, userid, '*Meanings: *' + card['card'].meaning_up, parse_mode='markdown')

def sendLongMessageInManyParts(bot, userid, msg, parse_mode, reply_markup):
  m = msg
  while len(m)>0:
    s = m[:4000]
    m = m[4000:]
    r = bot.sendMessage(userid, s, parse_mode=parse_mode, reply_markup=reply_markup)
  return r

class Message(object):
  def __init__(self, direction, timestamp, msg):
    self.direction = direction # either 'in' or 'out'
    self.timestamp = timestamp # timestamp
    self.message   = msg




# this is the chat with a particular user.
# its a finite state machine which remembers where we are in the interaction
# and routes the requests to the right handlers
class Chat(Machine):
  userid = None
  messages = []
  def __init__(self, userid):
    self.userid = userid
    states = ['start',
              'waiting_command', 
              'desc_multi_match_select', 
              'desc_single_reversed_select', 
              'desc_detail_select',
              'desc_meaning_select',
              'read_spread_select',
              'read_arcana_select',
              'read_reversed_select',
              'prefs_select',
              'prefs_daily_time_select',
              'prefs_daily_spread_select',
              'reading_spread_select',
              'reading_arcana_select'
              ]
    Machine.__init__(self, states=states, initial='start')
    self.add_transition('tr_wait',          'start',                  'waiting_command')
    self.add_transition('tr_restart',       '*',                      'waiting_command')
    self.add_transition('tr_choose_card',   'waiting_command',        'desc_multi_match_select')
    self.add_transition('tr_choose_reversed','waiting_command',        'desc_single_reversed_select')
    self.add_transition('tr_choose_detail', 'waiting_command',        'desc_detail_select')
    self.add_transition('tr_choose_reversed','desc_multi_match_select','desc_single_reversed_select')
    self.add_transition('tr_choose_detail', 'desc_single_reversed_select','desc_detail_select')
    self.add_transition('tr_choose_meaning','desc_detail_select',     'desc_meaning_select')
    self.add_transition('tr_reading',       'waiting_command',        'read_spread_select')
    self.add_transition('tr_arcana',        'read_spread_select',     'read_arcana_select')
    self.add_transition('tr_reversed',       'read_arcana_select',     'read_reversed_select')
    self.add_transition('tr_choose_detail2', 'read_reversed_select',   'desc_detail_select')
    self.show_greeting()
    self.tr_wait()
  # main message processing loop
  def process_msg(self, direction, time, msg):
    self.log_message(direction, time, msg)
    text = msg["text"]
    if self.state == 'waiting_command':
      command = self.identify_command(text)
#      print('command: '+command[0]+'\n')
      if command[0]=='invalid':
        self.send_message('sorry, I could not recognise your command. please try again')
      elif command[0]=='help':
        self.show_help()
      elif command[0]=='prefs':
        self.show_prefs()
      elif command[0]=='start':
        self.tr_restart()
      elif command[0]=='card_multiple':
        self.show_choose_card(command[1])
        self.tr_choose_card()
      elif command[0]=='card_single':
        self.card = command[1]
        self.send_message('Upright or Reversed?', markup={'keyboard': [['Upright', 'Reversed']], 'one_time_keyboard':True})
        self.tr_choose_reversed()
      elif command[0]=='card_single_reversed':
        self.card = command[1]
        self.reversed = (command[2]=='reversed')
        self.reply_card()
        self.tr_choose_detail()
      elif command[0]=='question':
        self.send_message('Choose Spread or type number of cards to pull', markup={'keyboard': [['One Card', 'Three Cards']], 'one_time_keyboard':True})
        self.tr_reading()
    elif self.state == 'read_spread_select':
      self.spread = text.lower()
      self.send_message('Choose Arcana', markup={'keyboard': [['All Cards', 'Major']], 'one_time_keyboard':True})
      self.tr_arcana()
    elif self.state == 'read_arcana_select':
      self.arcana = text.lower()
      self.send_message('Use reversed cards?', markup={'keyboard': [['Yes', 'No']], 'one_time_keyboard':True})
      self.tr_reversed()
    elif self.state == 'read_reversed_select':
      self.reversed = text.lower()
      if self.spread=='one card':
        n = 1
      elif self.spread=='three cards':
        n = 3
      else:
        try:
          n = int(self.spread)
        except ValueError:
          self.send_message('cannot recognise the spread you want to do')
          n = -1
      if ((n > 22) or (n<1)):
        self.send_message('sorry, cannot do spreads more than 22 cards')
      else:
        if n>1:                
          pulled_cards = []
          for i in range(1,n+1):
            self.send_message('*Card '+str(i)+'*')        
            self.choose_one_card_and_reply(pulled_cards, links_only=True)
            pulled_cards.append(self.card)
          self.show_greeting()
          self.tr_restart()
        else:
          self.choose_one_card_and_reply([], links_only=False)
          self.tr_choose_detail2()
    elif self.state == 'desc_multi_match_select':
      command = self.identify_command(text)
      if command[0]=='invalid':
        self.send_message('sorry, I could not recognise your command. please start again', markup={'hide_keyboard': True})
        self.tr_restart()
      elif command[0]=='card_single':
        self.card = command[1]
        self.send_message('Upright or Reversed?', markup={'keyboard': [['Upright', 'Reversed']], 'one_time_keyboard':True})
        self.tr_choose_reversed()
      elif command[0]=='card_single_reversed':
        self.card = command[1]
        self.reversed = (command[2]=='reversed')
        self.reply_card()
        self.tr_choose_detail()
    elif self.state == 'desc_single_reversed_select':
      self.reversed = (text.lower()=='reversed')
      self.reply_card()
      self.tr_choose_detail()
    elif self.state == 'desc_detail_select':
      if text.lower()=='yes':
        self.show_card_desc()
        self.tr_choose_meaning()
      else:
        self.show_greeting()
        self.tr_restart()
    elif self.state == 'desc_meaning_select':
      if text.lower()=='yes':
        self.show_card_meanings()
      self.show_greeting()
      self.tr_restart()
    #reply_tarot(userid, userfname, msg)
  # show multi card choice menu
  def choose_one_card_and_reply(self, already_chosen, links_only):
    full_deck = False if self.arcana=='major' else True
    reversed = True if self.reversed=='yes' else False
    while True:
      card = pull_card(full_deck, reversed)
      if card['n'] in already_chosen:
        pass
      else:
        break
    self.card = card['n']
    self.reversed = card['reversed']
    self.reply_card(links_only=links_only)
  def show_choose_card(self, cards):
    k = []
    for c in cards:
      k.append(['/'+c])
    self.send_message('Which card did you mean?', markup={'keyboard': k, 'one_time_keyboard':True})
  # send one card pic+keywords
  def reply_card(self, links_only=False):
    if ((deck[self.card].teleimage_down if self.reversed else deck[self.card].teleimage_up)==None):
      f = io.BytesIO(deck[self.card].image_down if self.reversed else deck[self.card].image)
      f.name = deck[self.card].name+('_reversed.jpg' if self.reversed else '.jpg')
      r = self.send_photo(f)
      f.close()
    else:
      r = self.send_photo(deck[self.card].teleimage_down if self.reversed else deck[self.card].teleimage_up)
    if (self.reversed & (deck[self.card].teleimage_down==None)):
      deck[self.card].teleimage_down = r['photo'][2]['file_id']
    elif (self.reversed==False & (deck[self.card].teleimage_up==None)):
      deck[self.card].teleimage_up = r['photo'][2]['file_id']
    text = '*' + deck[self.card].name + '* '+ ('(reversed)' if self.reversed else '(upright)')
    self.send_message(text)    
    cmd = 'for details use: /' + names[self.card] + ('reversed' if self.reversed else 'upright')
    self.send_message(cmd)    
    self.send_message('*Keywords: * _' + (deck[self.card].meaning_down_short if self.reversed else deck[self.card].meaning_up_short) + '_')
    if (links_only==False):
      self.send_message('Show Description?', markup={'keyboard': [['Yes', 'No']], 'one_time_keyboard':True})
  def show_card_desc(self):
    self.send_message('*Description: *' + deck[self.card].description)
    self.send_message('Show Meanings?', markup={'keyboard': [['Yes', 'No']], 'one_time_keyboard':True})
  def show_card_meanings(self):
    self.send_message('*Meanings: *' + (deck[self.card].meaning_down if self.reversed else deck[self.card].meaning_up), markup={'hide_keyboard': True})
  def show_greeting(self):
    self.send_message('Use /help or just type a question.', markup={'hide_keyboard': True})    
  def show_help(self):
    self.send_message('''
      You can use the following:
        ```/help``` -- see this message
        ```/start``` -- start from the beginning
        ```/<card>``` -- see <card> picture/description. E.g. /aceofwands or /aceofwandsreverse. These are shown during the reading and you can use them later to see card descriptions and meanings
        ```question``` -- have a reading about _question_.

       The *Major Arcana* Tarot card meanings illustrate the structure of human consciousness and, as such, hold the keys to life lessons passed down through the ages. The imagery of the Major Arcana Tarot cards is filled with wisdom from multiple cultures and esoteric traditions, including the Egyptian, Buddhist, Hindu, Sufi, Hebrew and Christian religions.

       The *Suit of Wands* is representative of the element of Fire. The Suit of Wands Tarot card meanings are associated with primal energy, spirituality, inspiration, determination, strength, intuition, creativity, ambition and expansion, original thought and the seeds through which life springs forth.

       The *Suit of Swords* is representative of the element of Air. The Suit of Swords Tarot card meanings are associated with action, change, force, power, oppression, ambition, courage and conflict.

       The *Suit of Pentacles* (also known as Coins or Disks) is representative of the element of Earth. The Suit of Pentacles Tarot card meanings cover material aspects of life including work, business, trade, property, money and other material possessions.

       The *Suit of Cups* Tarot card meanings deal with the emotional level of consciousness and are associated with love, feelings, relationships and connections.

       The numbered Tarot cards reflect everyday life situations while the Tarot Court Cards reflect personality-types or actual people. 
       
       While the Major Arcana Tarot card meanings reveal events that will naturally occur due to laws of the Universe, the Minor Arcana Tarot card meanings reveal events that naturally occur due to laws of human nature. Therefore, the Minor Arcana highlight the more practical aspects of life and can refer to current issues that have a temporary or minor influence.

       If a Tarot reading is predominantly made up of the Minor Arcana Tarot cards, you are dealing with day-to-day issues which will not necessarily having a lasting influence on your life.

       Final Advice:
       
       Ask open-ended questions to stimulate your subconscious. Ask 'what do i need to know about ...' not 'when will X happen?' Ask about yourself, not other people. Ask about input to something you can control. Respect the answers and dont abuse tarot. Be fully conscious of the question as you ask it.
    ''')    
#        ```/prefs``` -- setup preferences
  def show_prefs(self):
    self.send_message('/prefs not working yet...')
  def restart(self):
    self.show_greeting()
  # identify command
  def identify_command(self, text):
    text = text.lower()
    if (len(text)==0):
      return ('invalid',)
    if text[0:6]=='/start':
      command = ('start',)
    elif text[0:5]=='/help': 
      command = ('help',)
    elif text[0:6]=='/prefs': 
      command = ('prefs',)
    elif text[0]=='/':
      text = text[1:].replace(' ', '').replace('\t', '')
      if len(text)==0:
        command=('invalid',)
      else:
        reversed = ''
        if 'reversed' in text:
          reversed = 'reversed'
          text = text.replace('reversed','')
        if 'upright' in text:
          reversed = 'upright'
          text = text.replace('upright','')
        if text in names:
          if reversed in ['upright','reversed']:
            param1 = names.index(text)
            param2 = reversed
            command = ('card_single_reversed', param1, param2,)
          else:
            param1 = names.index(text)
            command = ('card_single', param1,)
        else:
          l = [s for s in names if text in s]
          if ((len(l)>1) & (len(l)<=4)):
            param1 = l
            command = ('card_multiple',param1,)
          else:
            command = ('invalid',)
    else:
      command = ('question',)
    return command
  def log_message(self, direction, time, msg):
    message = Message(direction, time, msg)
    self.messages.append(message)
    f = open('chats/%i.log' % self.userid,'a')
    f.write(jsonpickle.encode(message)+'\n') 
    f.close()
  def send_message(self, text, markup=None):
    if len(text)>4000:
      r = sendLongMessageInManyParts(bot, self.userid, text, parse_mode='markdown', reply_markup=markup)
    else:
      r = bot.sendMessage(self.userid, text, parse_mode='markdown', reply_markup=markup)
    logmsg(r) # global log file with all users communications
    self.log_message('out', datetime.datetime.now(), r)
    return r
  def send_photo(self, stream):
    r = bot.sendPhoto(self.userid, stream)
    logmsg(r)
    self.log_message('out', datetime.datetime.now(), r)
    return r



# msg handler to play with
def specific_handler(msg):
  # content_type, chat_type, chat_id = telepot.glance(msg)
  userid = msg["from"]["id"]
  if userid not in chats.keys():
    chat = Chat(userid)
    chats[userid] = chat
  else:
    chat = chats[userid]
  chat.process_msg('in',datetime.datetime.now(), msg)
                           

# top level message handler
def handle_message(msg):
  logmsg(msg)
  try:
    content_type, chat_type, chat_id = telepot.glance(msg)
    userid=msg["from"]["id"]
  except BaseException as e:
    log_err(e)
    #r = bot.sendMessage(userid, '*' + card['card'].name + '* (reversed)', parse_mode='markdown')
    raise e
  #userfname=msg["from"]["first_name"]
  #userlname=msg["from"]["last_name"]  
  if (content_type!='text'):
    print(str(userid)+': !!! '+content_type)
    bot.sendMessage(userid, "please only send text")
  else:  
    msgtext = msg["text"]
    print(str(userid)+': '+msgtext+'\n')
    try:
      specific_handler(msg)
    except BaseException as e:
      log_err(e)
      bot.sendMessage(userid, "internal error occurred, we will look into it! sorry about the inconvenience!")
#      raise e




deck=[]
load_cards()
names=[]
for d in deck:
  names.append(d.name.replace(' ', '').lower())
random.seed()

chats={}


TOKEN = sys.argv[1]
GMAILuser = sys.argv[2]
GMAILpwd = sys.argv[3]
bot = telepot.Bot(TOKEN)
bot.notifyOnMessage(handle_message)



while True:
  print('%s' % datetime.datetime.now()) 
  time.sleep(3)


