import ctx as ctx
import discord
import requests
import json
import asyncio
import aiohttp
from discord.ext import commands
import time
base_url = "http://127.0.0.1:8000/events/"

events = {
    'stat_url': base_url+'stat/',
    'win_url ': base_url+'win/',
    'check_events_url': base_url+'last/',
    'registration_url': base_url+'registration/',
    'leaderboard_url': base_url+'leaderboard/',
}

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
        params = {
            'ds_id': author_id_as_str
        }

        with session.get(events['stat_url'], params=params) as response:
            msg = json.loads(response.text)
        if msg['response'] == 'Error':
            await message.channel.send(f'{author_id_as_str} вы не зарегистрированы')
            return

        # Распарсить ответ в сообщение
        user_name = msg['user_name']
        game_count = msg['game_count']
        score = msg['score']

        await message.channel.send(f'{user_name}, сыграл {game_count} матчей, счет: {score}')
        return


    if message.content.startswith('!reg'):
        if isinstance(message.channel, discord.channel.DMChannel):
            body_data = {'ds_id': author_id_as_str}
            with session.post(events['registration_url'], data=body_data) as response:
                msg = json.loads(response.text)
            if msg['response'] == 'success':
                await message.channel.send(f'{msg["sha"]} ваш id')


    if message.content.startswith('!leaderboard'):
        if isinstance(message.channel, discord.channel.DMChannel):
            with session.get(events['leaderboard_url']) as response:
                msg = json.loads(response.text)
            if msg['response'] == 'success':
                top = msg['items']
            count = 1
            leader_response = ''
            for item in top:
                leaderboard_string = f"{count}. {item['user_name']}, рейтинг:{item['user_score']}, игр сыграно: {item['game_count']}" + '\n'
                leader_response = leader_response + leaderboard_string
                count += 1
            await message.channel.send(leader_response)


@Bot.event
async def check_new_events():
    await client.wait_until_ready()
    channel = client.get_channel(768067793198645258)
    while True:
        with session.get(events['check_events_url']) as response:
            msg = json.loads(response.text)
        if msg['oldest_event'] == 'no events':
            await asyncio.sleep(5)
        else:
            message = msg['oldest_event']
            await channel.send(content=message)
            await asyncio.sleep(5)


@Bot.event
async def update_leaderboard():
    await client.wait_until_ready()
    channel = client.get_channel(768591814147440641)
    print('rd')
    while True:
        counter = 1
        async for message in channel.history(limit=200):
            await message.delete()
        with session.get(events['leaderboard_url']) as response:
            msg = json.loads(response.text)
        if msg['response'] == 'success':
            top = msg['items']
        else:
            await asyncio.sleep(5)
            continue
        count = 1
        leader_response = ''
        for item in top:
            leaderboard_string = f"{count}. {item['user_name']}, рейтинг:{item['user_score']}, игр сыграно: {item['game_count']}" + '\n'
            leader_response += leaderboard_string
            count += 1
        await channel.send(content=leader_response)
        await asyncio.sleep(5)


client.loop.create_task(check_new_events())
client.loop.create_task(update_leaderboard())

client.run('NzY3MDY0Mjc1ODIxNzg5MjE0.X4seRg.OULbhV4bkymclEeGgl6MpyS1rfY')
