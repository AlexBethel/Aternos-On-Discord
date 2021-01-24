from commands import run_command
from config import USER, PASSWORD, BOT_TOKEN, PREFIX
from connect_and_launch import connect_account
from connect_and_launch import get_status, get_number_of_players
from discord.ext import tasks
import asyncio
import discord

client = discord.Client()


@client.event
async def on_ready():
    text = f"Logging into Aternos... | {PREFIX}help"
    await client.change_presence(activity=discord.Game(name=text))

    connect_account(USER, PASSWORD)  # logs into aternos
    print('The bot is logged in as {0.user}'.format(client))
    await asyncio.sleep(2)
    serverStatus.start()  # starts the presence update loop


@client.event
async def on_message(message):
    if message.author != client.user and message.content.startswith(PREFIX):
        await run_command(message)


@tasks.loop(seconds=5.0)
async def serverStatus():
    text = f"Server: {get_status()} | Players: {get_number_of_players()} | " \
           f"{PREFIX}help"
    activity = discord.Activity(type=discord.ActivityType.watching, name=text)
    await client.change_presence(activity=activity)


client.run(BOT_TOKEN)
