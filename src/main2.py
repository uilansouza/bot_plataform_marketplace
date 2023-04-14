import telebot
from telebot import types
from dotenv import load_dotenv
from os import getenv
from usecases.user import UCUser
load_dotenv(dotenv_path=".env")
import datetime
import re
bot = telebot.TeleBot(getenv("API_KEY_BOT"))
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('Option 1', 'Option 2')
    msg = bot.send_message(message.chat.id, "Hi! Choose an option:", reply_markup=markup)
    bot.register_next_step_handler(msg, option_selected)

def option_selected(message):
    msg = bot.send_message(message.chat.id, "You selected: {}".format(message.text))

def check(message):
    return True
@bot.message_handler(func=check)
def response(message):
    text = UCUser().welcome_user(message)
    bot.reply_to(message, text)
if __name__ =='__main__':
    print("executando....")
    bot.polling()