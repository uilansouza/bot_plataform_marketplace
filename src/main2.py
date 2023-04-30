import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
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
    bot.send_message(chat_id=message.chat.id, text="Olá, tudo bem? Escolha entre Sim ou Não.", reply_markup=create_buttons())

    # markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    # markup.add('Option 1', 'Option 2')
    # msg = bot.send_message(message.chat.id, "Hi! Choose an option:", reply_markup=markup)
    # bot.register_next_step_handler(msg, option_selected)

@bot.message_handler(commands=['canal'])
def canal(message):
    """pegar o chat_id do grupo no bot  jsondump bot"""
    invite_link= bot.create_chat_invite_link(chat_id='-1001639113531',name="market_place",member_limit=1,)

    #invite_link = bot.export_chat_invite_link(chat_id='-1639113531')
    print("message_id",type(invite_link))
    print(f"id_usuario:{ message.chat.id}")
    bot.send_message(chat_id=message.chat.id, text=f"Seu link exclusivo: {invite_link.invite_link}")

    #bot.send_message(chat_id=message.chat.id, text="Olá, tudo bem? Escolha entre Sim ou Não.", reply_markup=create_buttons())

@bot.message_handler(commands=['remove'])
def remove_canal(message):
    id_canal = -1001639113531
    id_user = 6018767990
    bot.kick_chat_member(chat_id=id_canal, user_id=id_user)
    chat = bot.get_chat(-1001639113531)
    name_canal = chat.title
    bot.send_message(chat_id="6018767990", text=f"Você foi removido do canal: {name_canal}")

@bot.message_handler(commands=['removidos'])
def removidos(message):
    chat_id = -1001639113531
    membros_bloqueados = []
    total_members = bot.get_chat_members_count(chat_id)
    print("TOTAL MEMBER: ",total_members )
    for i in range(1, total_members + 1):
        user = bot.get_chat_member(chat_id, i).user
        if user.is_bot:
            continue  # Pular usuários que são bots
        if user.status == 'kicked':
            membros_bloqueados.append(user)
    bot.send_message(chat_id=message.chat.id, text=f"Membros bloqueados {membros_bloqueados}")

def option_selected(message):
    msg = bot.send_message(message.chat.id, "You selected: {}".format(message.text))

bot.callback_query_handler(func=lambda call: True)
def create_buttons():
    keyboard = [[InlineKeyboardButton("Sim ✅", callback_data='sim'),
                 InlineKeyboardButton("Não ❌", callback_data='nao')]]
    return InlineKeyboardMarkup(keyboard)


@bot.callback_query_handler(func=lambda call: True)
def button_pressed(call):
    chat_id = call.message.chat.id
    if call.data == 'sim':
        bot.send_message(chat_id=chat_id, text="Você escolheu Sim ✅")
        #bot.answer_callback_query(callback_query_id=call.id, text="Você escolheu Sim.")
    elif call.data == 'nao':
         bot.send_message(chat_id=chat_id, text="Você escolheu Não! ❌")
        #bot.send_message(chat_id=chat_id, text="Você escolheu Não.")
        #bot.answer_callback_query(callback_query_id=call.id, text="Você escolheu Não.")


def check(message):
    return True
@bot.message_handler(func=check)
def response(message):
    text = UCUser().welcome_user(message)
    bot.reply_to(message, text)

if __name__ =='__main__':
    print("executando.....")
    bot.polling()