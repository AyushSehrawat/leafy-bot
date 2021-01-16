import datetime

from discord.ext import commands, timers
from discord.ext import commands
import requests
import discord
from discord.ext import tasks
from discord.ext.commands import cooldown, BucketType
from pymongo import MongoClient
import os
import time
import datetime
import motor.motor_asyncio
import nest_asyncio
nest_asyncio.apply()
mongo_url = os.environ.get('MONGO_URL')
cluster = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
reminder = cluster['discord']['reminder']


class Remind(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.checker.start()

    @commands.Cog.listener()
    async def on_ready(self):
        print('Remind cog loaded successfully')

    @commands.command(cooldown_after_parsing=True,aliases=['remind','reminder'])
    @cooldown(1, 30, BucketType.user)
    async def notify(self, ctx: commands.Context, ttime, *, desc: str):
        try:

            if len(desc) < 50:
                typ = ttime[-1]
                ttime = int(ttime[0:-1])
                choices = ['s','m','h','d']
                if typ not in choices:
                    await ctx.send('**Only s(seconds), m(minutes),h(hours),d(days)**')
                else:
                    if typ == 's':
                        conv = ttime
                    elif typ == 'm':
                        conv = ttime*60
                    elif typ == 'h':
                        conv = ttime*3600
                    elif typ == 'd':
                        conv = ttime*86400


                    if conv >604800:
                        await ctx.send('**Not more than 7 days**')
                    else:
                        await ctx.send('**Reminder has been set**')
                        a = datetime.datetime.now()
                        a = a + datetime.timedelta(seconds=conv)
                        newuser = {'id':ctx.author.mention, 'Time': a,'Desc' : desc,'Channel' : ctx.channel.id}
                        await reminder.insert_one(newuser)



            else:
                await ctx.send('**Too Long Reminder**')
        except ValueError:
            pass

    
    @tasks.loop(seconds=10)
    async def checker(self):
        try:
            all = reminder.find({})
            current = datetime.datetime.now()
            async for x in all:
                if current >= x['Time']:
                    channel_only = self.client.get_channel(x['Channel'])
                    desc = x['Desc']
                    person = x['id']
                    await channel_only.send(f"{person} **Reminder :** {desc}")
                    await reminder.delete_one(x)
                else:
                    pass
        except Exception:
            pass

def setup(client):
    client.add_cog(Remind(client))