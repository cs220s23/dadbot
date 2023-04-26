# Dad Bot

A discord bot that tells dad jokes and more

Built using [discord.py](https://github.com/Rapptz/discord.py)


## TODO

* [x] add joke command
* [x] read jokes from file
* [x] read jokes from database
* [ ] update documentation
    * [ ] include command info

## Dependencies

* [discord.py](https://github.com/Rapptz/discord.py)
* [redis](https://github.com/redis/redis-py)
* [Pillow](https://github.com/python-pillow/Pillow)


## Installation

### Local

1. Clone this repo and enter the directory

```bash
git clone https://github.com/cs220s23/dadbot
cd dadbot
```

2. Create a virtual environment and install requirements

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Docker Compose

Here's how to run the dadbot with [docker-compose](https://docs.docker.com/compose/)
See [here](https://docs.docker.com/compose/install/) for instructions on how to install docker-compose for your distribution.

```bash
git clone https://github.com/cs220s23/dadbot
```

## AWS EC2 Instance Running Amazon Linux 2

**Note:** commands prefixed with # are to be run as superuser


1. Install git, docker, and docker-compose

```bash
# yum install git docker
# curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
# chmod +x /usr/local/bin/docker-compose
```

2. Start docker service

```bash
# systemctl start docker
```

3. Clone this repo
```bash
git clone https://github.com/cs220s23/dadbot
```

## Running

To have this bot connect to discord's servers you need a bot token.
Following [the official tutorial](https://discord.com/developers/docs/getting-started) will help with this.

All of the following routes require that you have the environment variable `DISCORD_TOKEN` set to your token.
The instructions below assume that you have a `.env` file with the following contents:

```bash
DISCORD_TOKEN=YOUR_BOT_TOKEN_HERE
```

### Locally

1. Place the `.env` file in the same directory as `dadbot.py`
2. Activate the python virtual environment

```bash
source .venv/bin/activate
```

3. Run dadbot

```bash
python3 dadbot.py
```

### Docker Compose/AWS EC2 Instance Running Amazon Linux 2


1. Place the `.env` file in the same directory as `docker-compose.yml`
2. Start with docker compose, building the image may take some time on the first run

```bash
docker compose up
```

**NOTE:** if running on a Linux based system this command must be run as root or the by a user in the `docker` group
