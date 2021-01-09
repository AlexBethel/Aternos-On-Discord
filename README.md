# Aternos On Discord

A simple tool to serve your own discord bot so you can manage an Aternos server from discord.

## Getting Started

1. Git clone this repository
2. Install it using either:
   * Copy, paste and execute this command inside the project folder: ```pip install -r requirements.txt```
   * Alternatively you can create a virtual environnement using ```python -m venv venv``` and then ```source venv/bin/activate``` to finally ```pip install -r  requirements.txt```
3. Copy or rename ```config.def.toml``` to ```config.toml```, and fill out each of the listed fields to configure the bot for your particular server.
4. Execute using this command inside the project folder : ```python3 Bot.py```

### Prerequisites

* Python 3.7 or higher
* A Discord server for which you have the rights to add a bot (Manage Server permission)
* An Aternos account

### Discord Commands

* --launch server
* --server status
* --server info
* --players
* --stop server
* --help


### Cloud Hosting Note

Cloud hosting this bot would require some workarounds as Aternos recognizes you are connecting from a data center and prompts for a captcha test.
