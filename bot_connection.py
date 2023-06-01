import telebot as tb
from telebot import types
from log import log
from bot import bestiary_bot
from database_connection import add_to_db


def get_token(url): # read token from file
    with open (file=url, mode='r') as token_file:
        return token_file.read()


TOKEN_URL = 'D:\Dropbox\Coding\Tokens\dnd_bestiary_token'

# Telegram API connection
try:
    token = get_token(TOKEN_URL)
    bot = tb.TeleBot(token)
except:
    log.add('ERROR: Connection failed, check token')

def reply_user(user, reply):
    '''
    Send reply to user
    '''
    for type, message in reply.items():
        if type == 'text':                                      # send text
            log.bot_activity(user, 'text', message)
            bot.send_message(user, message, parse_mode="HTML")
        elif type == 'pic':                                     # send picture
            log.bot_activity(user, 'pic', message)
            bot.send_photo(user, message)
        elif type == 'buttons':                                 # send buttons
            log.bot_activity(user, 'buttons', *message)
            keyboard = types.InlineKeyboardMarkup()
            for button in message[1:]:
                keyboard.add(types.InlineKeyboardButton(text=button[1], callback_data=button[0]))
            bot.send_message(user, text=message[0], reply_markup=keyboard, parse_mode='HTML')



@bot.message_handler(commands=['start', 'help']) # start and help commands handling
def start_messages(message):
    user = message.from_user
    log.user_activity('user message', message.text, user=user)
    add_to_db(user, 'command', message.text)
    bot.send_message(user.id, bestiary_bot.message_start, parse_mode="HTML")
    log.bot_activity(user.id, bestiary_bot.message_start)

@bot.message_handler(content_types=['text'])  # message handling
def get_text_messages(message):
    user = message.from_user
    log.user_activity('user message', message.text, user=user)
    add_to_db(user, 'text', message.text)
    reply = bestiary_bot.text_replier(message.text)
    reply_user(user.id, reply)

@bot.callback_query_handler(func=lambda call: True) # buttons handling
def callback_worker(call):
    user_info = call.json['from']
    user = types.User(id=user_info['id'], first_name=user_info.get('first_name', None),
                      last_name=user_info.get('last_name', None),
                      username=user_info.get('username', None), is_bot=user_info['is_bot'])
    button_id = call.data
    log.user_activity('user push button', button_id, user=user)
    add_to_db(user, 'button', f'id: {button_id}')
    reply = bestiary_bot.button_replier(button_id)
    reply_user(user.id, reply)



log.clear()
log.add('bot.py started')
bot.polling(none_stop=True, interval=0)

log.add('bot.py stopped')