# Enable Developer Mod in discord , go to appearances and on developer mod :)
import asyncio
import datetime
import json
import os
import random
from itertools import cycle
from threading import Thread

import discord
import motor.motor_asyncio
import nest_asyncio
import psutil
from discord.ext import commands, tasks
from discord.ext.commands import BucketType, cooldown
from discord.utils import get
from flask import Flask
from pymongo import MongoClient

import discord_pass

nest_asyncio.apply()

mongo_url = os.environ.get("MONGO_URL")

cluster = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)

predb = cluster["discord"]["prefix"]


async def get_prefix(bot, message):
    stats = await predb.find_one({"guild": message.guild.id})
    # server_prefix = stats["prefix"]
    if stats is None:
        updated = {"guild": message.guild.id, "prefix": "--"}
        await predb.insert_one(updated)
        extras = "--"
        return commands.when_mentioned_or(extras)(bot, message)
    else:
        extras = stats["prefix"]
        return commands.when_mentioned_or(extras)(bot, message)


bot = commands.AutoShardedBot(
    command_prefix=get_prefix, intents=discord.Intents.all(), owner_id=727365670395838626
)

bot.remove_command("help")

status = cycle(["Leafy | Ping to know prefix", "Leafy | Ping to know prefix"])

unicode_list = ["\U0001f600", "\U0001f970", "\U0001f609", "\U0001f60a", "\U0001f971"]


@bot.event
async def on_ready():
    change_status.start()
    print("Bot is ready")


@bot.event
async def on_guild_join(guild):
    updated = {"guild": guild.id, "prefix": "--"}
    predb.insert_one(updated)
    print("Joined a guild")
    try:
        #
        embed = discord.Embed(
            title="Hello!",
            description="Thanks for adding me to your server! I hope you like me <:rainblob:796632292503977995>! I got a new family :)",
            color=0xFF0000,
        )
        embed.add_field(
            name="Use --help to know more about me",
            value="To get started use `--help` or `--help setup` to setup few things",
        )
        if guild.system_channel:
            await guild.system_channel.send(embed=embed)
        else:
            print("No system channel")

    except:
        raise


@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


@client.command(hidden=True)
@cooldown(1, 60, BucketType.user)
async def hello(ctx):
    msg = await ctx.send(f"Hello {ctx.author.mention}")
    await msg.add_reaction(f"{random.choice(unicode_list)}")


@client.command(description="Sends a password of given length")
@cooldown(1, 10, BucketType.user)
async def password(ctx, passlength=10):
    passlength = int(passlength)
    if passlength > 51:
        embed = discord.Embed(
            title="Invalid usage",
            description="Your password cannot be so long",
            color=0xFF000,
        )
        embed.set_image(
            url="https://media1.tenor.com/images/7cb7b5cc74e9a63d11e474a3e135d617/tenor.gif"
        )
        await ctx.send(embed=embed)

    elif passlength < 51:
        passwor = discord_pass.secure_password_gen(passlength)
        embed = discord.Embed(
            title="Password Sent <:CheckMark:795884692024590367>",
            description="Check your dm for password ",
            color=0xFF000,
        )
        await ctx.send(embed=embed)
        await ctx.send(f"{ctx.author.mention} Check your dm for the password! ")
        await ctx.author.send(f"You password is \n `{passwor}`")


@bot.command(hidden=True)
async def load(ctx, extension):
    if ctx.author.id == 727365670395838626:
        bot.load_extension(f"cogs.{extension}")
        await ctx.send("Done")


@bot.command(hidden=True)
async def unload(ctx, extension):
    if ctx.author.id == ctx.bot.owner_id:
        bot.unload_extension(f"cogs.{extension}")
        await ctx.send("Done")


@bot.command(hidden=True)
async def reload(ctx, extension):
    if ctx.author.id == ctx.bot.owner_id:
        bot.unload_extension(f"cogs.{extension}")
        bot.load_extension(f"cogs.{extension}")
        await ctx.send("Done")


@bot.event
async def on_message(msg):
    if msg.content == f"<@!{bot.user.id}>":
        stats = await predb.find_one({"guild": msg.guild.id})
        if stats is None:
            pref = "--"
        else:
            pref = stats["prefix"]
        embed = discord.Embed(color=0xFF0000)
        embed.set_author(
            name=f"My prefix is `{pref}` and use `{pref}help` to see all commands",
            icon_url=msg.author.avatar_url,
        )
        await msg.channel.send(embed=embed)
    await bot.process_commands(msg)


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.load_extension("jishaku")

token = os.environ.get("BOT_TOKEN")

bot.run(f"{token}")  # Here goes your token in ''
