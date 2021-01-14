import sys
import toml

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
