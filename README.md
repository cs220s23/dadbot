# Dad Bot

A discord bot that tells dad jokes and more

Built using [discord.py](https://github.com/Rapptz/discord.py)


## TODO

* [x] add joke command
* [x] read jokes from file
* [ ] read jokes from database
* [ ] update documentation

## Installation

### Local

1. Clone this repo and enter the directory

```bash
git clone REPONAME
cd dadbot
```

2. Create a virtual environment and install requirements

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Docker Compose

Here's how to run the dadbot with docker-compose

```bash
git clone REPONAME
cd dadbot
echo "DISCORD_TOKEN=YOUR_BOT_TOKEN_HERE" > .env
docker compose up
```
