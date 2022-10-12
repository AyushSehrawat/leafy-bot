Note - This project is not maintained and has old version of dependencies. 
If you are interested in continuing this project create an issue to let me know. 


![Python-Versions](https://img.shields.io/badge/python-3.8.7-blue?style=flat-square)
![Discord.py-Version](https://img.shields.io/badge/discord.py-1.6.0-blue?style=flat-square)

# Leafy-Bot
**A multipurpose bot for Discord coded in Discord.py*

<img alt="Leafy-Logo" align="right" src="https://i.imgur.com/qDVEowI.png" width=40%/>

Code here serves for education purposes only


## Features and Commands

There are a lot of features and many of the commands are dependant on mongoDB
it's preferred that you create a cluster on mongoDB and create the following collections in order to use the database based commands

![Like this](https://i.imgur.com/JlYlvqE.png)




Commands:

* Main: general, mod, fun, info, music, setup, extra

* General: rank, lb, ping, avatar, wiki, search, note, notes, trash, poll, quickpoll, remind, pip/pypi

* Fun: ascii, ga, cat, dog, password, ly, sendnuke, roast, 8ball, choose, choosebestof, lenny, meme, joke, ipinfo, calc, activity, remind, guess, bird, fml, sadcat, say, bj

* Bot owner commands: load/unload cogs, jsk cog - Can be used to run python scripts, shell and much more! Check docs [here](https://jishaku.readthedocs.io/en/latest/index.html)

* Moderation: kick, ban, unban, softban, clear, warn, warns, case, clearwarns/cw, mute, unmute, slow, rslow, block, unblock, lock, unlock, addrole, unrole

* Info: bot, user/ui, server/si, mem/memcount

* Music: join, play, stop, pause, resume, skip, queue, shuffle, remove, leave

* Setup: level, setprefix

* Extra: invite ( add Leafy!) , vote ( Vote for Leafy!) , suggest ( Suggest us )

* Nsfw - Requires Ksoft api key


### Install Modules/ Dependancies

```
pip install -r requirements.txt
```



#### Sample layout of `.env` file

```bash
BOT_TOKEN=token_here
MONGO_URL = url_here
ALEX = token_here
```

# Contributing Guidelines

## These are few needed things for contributing to Leafy

You should use pre-commit.

```bash
python3 -m pip install pre-commit  # required only once
pre-commit install
```

That's it! The plugin will run every time you commit any changes. If there are any errors found during the run, fix them and commit those changes. You can even run the plugin manually on all files:

```bash
pre-commit run --all-files --show-diff-on-failure
```
* Note - Use `.env` or `.venv` instead of `env` or `venv` ( virtual environments ). It is to prevent pre-commit from scanning them.
