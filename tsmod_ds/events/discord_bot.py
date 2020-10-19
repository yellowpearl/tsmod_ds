import discord
import requests
import json
import asyncio
import aiohttp
from discord.ext import commands

stat_url = 'http://127.0.0.1:8000/events/stat'
win_url = 'http://127.0.0.1:8000/events/win'
check_events_url = 'http://127.0.0.1/events/newevent'

session = requests.Session()
Bot = commands.Bot(command_prefix='!')
client = discord.Client()

@client.event
async def check_new_events():
    while True:
        # GET запрос к вебсервису
        async with session.get(check_events_url) as response:
            txt = response.text
            channel = Bot.get_channel(325360370069929996)
            # Ответ отправить сообщением на канал
            await channel.send(txt)
            await asyncio.sleep(5)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!stat'):
        # Получить ds id
        author_id = message.author
        # Отправить его на /event/stat
        params = {
            'id': author_id
        }
        request_bot = session.get(stat_url, params=params)
        # Распарсить ответ в сообщение
        msg = json.loads(request_bot.text)
        user_name = msg['user_name']
        game_count = msg['game_count']
        score = msg['score']

        await message.channel.send(f'{user_name}, сыграл {game_count} матчей, счет:{score}')

client.loop.create_task(check_new_events())

client.run('NzY3MDY0Mjc1ODIxNzg5MjE0.X4seRg.OULbhV4bkymclEeGgl6MpyS1rfY')
