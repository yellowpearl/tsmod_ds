import discord
import requests
import json
import asyncio
import aiohttp
from discord.ext import commands
import time

stat_url = 'http://127.0.0.1:8000/events/stat/'
win_url = 'http://127.0.0.1:8000/events/win/'
check_events_url = 'http://127.0.0.1/events/last/'
registration_url = 'http://127.0.0.1/events/registration/'

session = requests.Session()
Bot = commands.Bot(command_prefix='!')
client = discord.Client()


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
        channel = client.get_channel(768067793198645258)
        print(type(channel))
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


@Bot.event
async def check_new_events():
    await asyncio.sleep(15)
    channel = client.get_channel(768067793198645258)
    while True:
        # GET запрос к вебсервису
        with session.get(check_events_url) as response:
            msg = json.loads(response.text)
        if msg['oldest_event'] == 'no events':
            await channel.send(content='No events111')
            await asyncio.sleep(5)
        else:
            message = msg['oldest_event']
            await channel.send(content=message)
            await asyncio.sleep(5)



client.loop.create_task(check_new_events())

client.run('NzY3MDY0Mjc1ODIxNzg5MjE0.X4seRg.OULbhV4bkymclEeGgl6MpyS1rfY')
