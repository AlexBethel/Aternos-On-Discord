from config import PREFIX
from connect_and_launch import get_server_info
from connect_and_launch import get_status, get_number_of_players
from connect_and_launch import start_server, stop_server
import asyncio
import discord

# Using an array, not a dictionary, because the commands have a
# specific order they must appear in in help messages.
commands = []


# Function decorator for commands.
def command(name, description):
    def inner(function):
        cmd = {}
        cmd['name'] = name
        cmd['description'] = description
        cmd['function'] = function

        commands.append(cmd)

    return inner


@command("start", "Starts the server")
async def cmd_start(message):
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
        text = ("An error occurred. Either the status server is not "
                "responding or you didn't set the server name "
                "correctly.\n\nTrying to launch the server anyways.")
    await message.channel.send(text)
    await start_server()


@command("stop", "Stops the server")
async def cmd_stop(message):
    await message.channel.send("Stopping the server.")
    status = get_status()

    if status != 'Stopping ...' or status != 'Saving ...':
        await stop_server()

    else:
        await message.channel.send("The server is already offline.")


@command("status", "Gets the server status")
async def cmd_status(message):
    await message.channel.send("The server is "
                               f"{get_status().lower()}.")


@command("players", "Gets the number of players")
async def cmd_players(message):
    text = f"There are {get_number_of_players()} players online."
    await message.channel.send(text)


@command("info", "Gets the server info")
async def cmd_info(message):
    ip, status, players, software, version = get_server_info()
    text = (f"**IP:** {ip} \n**Status:** {status} \n**Players: "
            f"**{players} \n**Version:** {software} {version}")
    embed = discord.Embed()
    embed.add_field(name="Server Info", value=text, inline=False)
    await message.channel.send(embed=embed)


@command("help", "Displays this message")
async def cmd_help(message):
    embed = discord.Embed(title="Help")
    for cmd in commands:
        embed.add_field(name=f"{PREFIX}{cmd['name']}",
                        value=cmd['description'],
                        inline=False)

    await message.channel.send(embed=embed)


# Special command, invoked only when an unknown command is read.
async def cmd_unknown(message):
    await message.channel.send(f"Unknown command; use {PREFIX}help to "
                               f"see a list of all avaliable commands.")


# Finds a command whose name matches the given text.
def match_command(text):
    for cmd in commands:
        if cmd['name'] == text:
            return cmd

    return None


# Runs a command with the given source message, which must begin with
# the PREFIX.
async def run_command(message):
    user_command = message.content[len(PREFIX):]
    cmd = match_command(user_command)
    if cmd:
        await cmd['function'](message)
    else:
        await cmd_unknown(message)
