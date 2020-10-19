import discord
import requests
import json
import asyncio
import aiohttp
from discord.ext import commands

stat_url = 'http://127.0.0.1:8000/events/stat/'
win_url = 'http://127.0.0.1:8000/events/win/'
check_events_url = 'http://127.0.0.1/events/last/'
registration_url = 'http://127.0.0.1/events/registration/'

session = requests.Session()
Bot = commands.Bot(command_prefix='!')
client = discord.Client()

#@client.event
#async def check_new_events():
#    while True:
#        # GET запрос к вебсервису
#        response = session.get(check_events_url)
#        txt = response.text
#        channel = Bot.get_channel(325360370069929996)
#        # Ответ отправить сообщением на канал
#        await channel.send(txt)
#        await asyncio.sleep(5)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    author_id_as_str = str(message.author).replace('#', '')

    if message.content.startswith('!stat'):
        # Отправить его на /event/stat
        params = {
            'ds_id': author_id_as_str
        }
        with session.get(stat_url, params=params) as response:
            msg = json.loads(response.text)
        try:
            err = msg['Error']
            await message.channel.send(f'{author_id_as_str} вы не зарегистрированы')
            return
        except:
            pass
        # Распарсить ответ в сообщение
        user_name = msg['user_name']
        game_count = msg['game_count']
        score = msg['score']

        await message.channel.send(f'{user_name}, сыграл {game_count} матчей, счет: {score}')
        return

    if message.content.startswith('!reg'):
        body_data = {'ds_id': author_id_as_str}
        # await сделать POST запрос
        with session.post(registration_url, data=body_data) as response:
            msg = json.loads(response.text)['response']
        # await отправить сообщение с hash_id
        await message.channel.send(f'{msg} ваш id')

#client.loop.create_task(check_new_events())

client.run('NzY3MDY0Mjc1ODIxNzg5MjE0.X4seRg.OULbhV4bkymclEeGgl6MpyS1rfY')
