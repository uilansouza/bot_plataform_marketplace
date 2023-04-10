import telebot
from dotenv import load_dotenv
from os import getenv
import datetime
import re

load_dotenv(dotenv_path=".env")
API_KEY_BOT = getenv("API_KEY_BOT")
print(API_KEY_BOT)
bot = telebot.TeleBot(API_KEY_BOT)


def check(message):
    return True


def start_user(message):
    user = message.from_user.first_name
    timestamp = message.date
    date = datetime.datetime.fromtimestamp(timestamp)
    hour = date.hour
    if hour >= 5 and hour < 12:
        greetings = "Bom dia,"
    elif hour >= 12 and hour < 18:
        greetings = "Boa tarde,"
    else:
        greetings = "Boa noite,"

    text = ""
    if user:
        text = f"Ola {user}, {greetings} Tudo bem?\nPor qual opção você prefere validar seu acesso?" \
               f"\n/email - Para validar por email" \
               f"\n/codigo_compra - Para validar com o código da compra"

    return text


"""Valida acesso"""


@bot.message_handler(commands=['email'])
def email(message):
    text = "Por favor digite seu e-mail:"
    bot.send_message(message.chat.id, text)
    validade_access(message, 'email')


@bot.message_handler(commands=['codigo_compra'])
def codigo_compra(message):
    text = "Por favor digite o código da sua compra:"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['validate_acess'])
def validade_access(message, type_acess):
    if type_acess in 'email':
        while not (validate_email(message.text)):
            text = 'Esse não é um email válido, por favor digite um email valido ou digite "sair" pra recomeçar'
            bot.reply_to(message, text)
            validade_access(message, 'email')




def validate_email(email):
    # Definindo a expressão regular
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    # Validando o endereço de e-mail
    if re.match(padrao, email):
        return True
    else:
        return False


# --- First message
@bot.message_handler(func=check)
def response(message):
    text = start_user(message)
    bot.reply_to(message, text)


bot.polling()
