import os
import re
import datetime
import asyncio
from dotenv import load_dotenv
from telethon import TelegramClient, events, Button, sync, functions
from telethon.tl.functions.messages import ExportChatInviteRequest
from telethon.tl.types import InputChannel, InputPeerChannel, InputPeerEmpty, ChannelParticipantsBanned
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsKicked
from telethon import TelegramClient, events, types
from telethon.tl.custom.adminlogevent import AdminLogEvent
from telethon.tl.functions.messages import SendMessageRequest
from telethon.tl.custom.participantpermissions import ParticipantPermissions
from telethon.client.chats import ChatMethods

load_dotenv(dotenv_path=".env")

# Configurar as variáveis de ambiente
API_ID = 23855116  # os.getenv("API_ID")
API_HASH = "09ebabe70588b4cac32873f90a0c1a1a"  # os.getenv("API_HASH")
BOT_TOKEN = "5978677525:AAFmazl33wBu6e0LjBikyA3Pb1N6nxLRlVA"  # os.getenv("BOT_TOKEN")
CHANNEL_ID = -1001639113531  # os.getenv("CHANNEL_ID")
GROUP_ID = -1974447589  # os.getenv("GROUP_ID")
client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

channel = None


# Cria Link exclusivo de um canal
@client.on(events.NewMessage(pattern='/canal'))
async def canal(event):
    invite_link = await client(ExportChatInviteRequest(CHANNEL_ID, usage_limit=1))
    await event.respond(f"Seu link exclusivo: {invite_link.link}")
    return


# Bani um usuário do grupo permanetemente e o bloqueia
@client.on(events.NewMessage(pattern='/ban'))
async def remove(event):
    user_id = event.sender_id
    user_id = 6018767990

    chat = await client.get_entity(6018767990)
    await client.edit_permissions(CHANNEL_ID, user_id, view_messages=False)

    chat = await client.get_entity(GROUP_ID)
    name_canal = chat.title
    message = f"Você foi removido do canal: {name_canal}"

    await client(SendMessageRequest(user_id, message))
    # await event.respond(user_id,f"Você foi removido do canal: {name_canal}")


# Remove o bloqueio do usuário ao canal.
@client.on(events.NewMessage(pattern='/remove_ban'))
async def remove_ban(event):
    user_id = 6018767990
    await client.edit_permissions(CHANNEL_ID, user_id, view_messages=True)
    message = "você foi aceito no canal "
    await client(SendMessageRequest(user_id, message))
    return


# Lista os usuários de um canal/grupo
@client.on(events.NewMessage(pattern='/participantes'))
async def removidos(event):
    channel = await client.get_entity(CHANNEL_ID)
    users = await client.get_participants(channel, aggressive=True)
    membros = list()
    message = "Participantes do Canal/Grupo:\n"
    for user in users:
        membros.append(user.first_name)
        message += f"{user.first_name} {user.last_name}\n"

    await event.respond(message)
    return


# Lista os usuários banidos do grupo
@client.on(events.NewMessage(pattern='/removidos'))
async def get_banned_users(event):
    membros_banidos = list()
    message = "Participantes removidos do Canal/Grupo:\n"
    async for user in client.iter_participants(CHANNEL_ID, filter=ChannelParticipantsKicked):
        membros_banidos.append(user)
        message += f"\n{user.first_name}"
    await event.respond(message)
    return


@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    handled = True
    buttons = [[Button.inline("Sim ✅", b'sim'), Button.inline("Não ❌", b'nao')]]
    await event.respond("Olá, tudo bem? Escolha entre Sim ou Não.", buttons=buttons)
    return


@client.on(events.CallbackQuery(data=b'sim'))
async def sim(event):
    await event.edit("Você escolheu Sim ✅")
    return


@client.on(events.CallbackQuery(data=b'nao'))
async def nao(event):
    await event.edit("Você escolheu Não! ❌")
    return

@client.on(events.NewMessage())
async def response(event):
    if not event.is_group and event.is_private and event.raw_text != "/start":
        return
    text = "Bem vindo"  # UCUser().welcome_user(event)
    await event.reply(text)


async def start_telegram():
    # client = TelegramClient('default_session', API_ID, API_HASH)
    await client.start()


if __name__ == '__main__':
    print("executando.....")
    client.run_until_disconnected()
