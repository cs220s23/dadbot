# Dad Bot

A discord bot that tells dad jokes and more

Built using [discord.py](https://github.com/Rapptz/discord.py)


## TODO

* [x] add joke command
* [x] read jokes from file
* [ ] read jokes from database
* [ ] update documentation

## Redis

* stores jokes as set of lists
* use SRANDMEMBER to randomly select joke
* 

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

