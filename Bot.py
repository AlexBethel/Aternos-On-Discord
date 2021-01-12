import discord
import sys
import toml
import asyncio
from discord.ext import tasks
from connect_and_launch import get_status, get_number_of_players
from connect_and_launch import connect_account, get_server_info
from connect_and_launch import start_server, stop_server

config = None
try:
    config = toml.load("config.toml")
except FileNotFoundError:
    print("Missing config.toml.")
    print("Copy or rename 'config.def.toml' to 'config.toml', then")
    print("fill out each of the fields.")
    sys.exit(1)

USER = config["aternos"]["username"]
PASSWORD = config["aternos"]["password"]
BOT_TOKEN = config["discord"]["bot_token"]
PREFIX = config["discord"]["prefix"]

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

    if message.author == client.user:
        return

    if message.content.startswith(PREFIX):

        command = message.content[len(PREFIX):]
        if command.lower() == 'start':

            await message.channel.send("Launching Server...")
            status = get_status()

            if status == "Offline":
                await start_server()
                author = message.author
                # loops until server has started and pings person who launched
                while True:
                    await asyncio.sleep(5)
                    if get_status() == "Online":
                        await message.channel.send(f"{author.mention}, the "
                                                   f"server has started!")
                        break

            elif status == "Online":
                await message.channel.send("The server is already online.")

            elif status == 'Starting ...' or status == 'Loading ...':
                text = "The server is already starting..."
                await message.channel.send(text)

            elif status == 'Stopping ...' or status == 'Saving ...':
                text = "The server is stopping. Please wait."
                await message.channel.send(text)

            else:
                text = "An error occurred. Either the status server is not " \
                       "responding or you didn't set the server name " \
                       "correctly.\n\nTrying to launch the server anyways."
                await message.channel.send(text)
                await start_server()

        elif command.lower() == 'status':
            await message.channel.send("The server is "
                                       f"{get_status().lower()}.")

        elif command.lower() == 'players':
            text = f"There are {get_number_of_players()} players online."
            await message.channel.send(text)

        elif command.lower() == 'info':
            ip, status, players, software, version = get_server_info()
            text = f"**IP:** {ip} \n**Status:** {status} \n**Players: " \
                   f"**{players} \n**Version:** {software} {version}"
            embed = discord.Embed()
            embed.add_field(name="Server Info", value=text, inline=False)
            await message.channel.send(embed=embed)

        elif command.lower() == 'stop':
            await message.channel.send("Stopping the server.")
            status = get_status()

            if status != 'Stopping ...' or status != 'Saving ...':
                await stop_server()

            else:
                await message.channel.send("The server is already offline.")

        elif message.content.lower() == f'{PREFIX}help':
            embed = discord.Embed(title="Help")
            embed.add_field(name=f"{PREFIX}start",
                            value="Starts the server",
                            inline=False)
            embed.add_field(name=f"{PREFIX}stop",
                            value="Stops the server",
                            inline=False)
            embed.add_field(name=f"{PREFIX}status",
                            value="Gets the server status",
                            inline=False)
            embed.add_field(name=f"{PREFIX}info",
                            value="Gets the server info",
                            inline=False)
            embed.add_field(name=f"{PREFIX}players",
                            value="Gets the number of players",
                            inline=False)
            embed.add_field(name=f"{PREFIX}help",
                            value="Displays this message",
                            inline=False)
            await message.channel.send(embed=embed)

        else:
            await message.channel.send("Unknown command, use {PREFIX}help to "
                                       "see a list of all avaliable commands.")


@tasks.loop(seconds=5.0)
async def serverStatus():
    text = f"Server: {get_status()} | Players: {get_number_of_players()} | " \
           f"{PREFIX}help"
    activity = discord.Activity(type=discord.ActivityType.watching, name=text)
    await client.change_presence(activity=activity)


client.run(BOT_TOKEN)
