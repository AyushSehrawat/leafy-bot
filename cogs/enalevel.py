import discord
from discord.ext import commands
from pymongo import MongoClient

import os
import motor.motor_asyncio
import nest_asyncio
nest_asyncio.apply()
mongo_url = os.environ.get('MONGO_URL')

cluster = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)

ledb = cluster["discord"]["enalevel"]


class Enalevel(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Enalevel cog loaded successfully')

    @commands.command(aliases=["levelling"],description='Enable or disable levelling')
    @commands.has_permissions(administrator=True)
    async def level(self,ctx,choice):
        lst = ["enable","disable"]
        stats = await ledb.find_one({"id": ctx.guild.id})
        if choice in lst:
            if choice == "enable":
                choice = 0
                stats = await ledb.find_one({"id": ctx.guild.id})
                if stats is None:
                    newuser = {"id": ctx.guild.id, "type": choice}
                    await ledb.insert_one(newuser)
                    await ctx.send('**Changes are saved**')

                elif stats['type'] == 0:
                    await ctx.send('**Command is already enabled**')

                else:
                    await ledb.update_one({
                        "id": ctx.guild.id
                    }, {"$set": {
                        "type": choice
                    }})

                    await ctx.send('**Changes are saved | Command enabled**')
            else:
                choice = 1

                stats = await ledb.find_one({"id": ctx.guild.id})
                if stats is None:
                    newuser = {"id": ctx.guild.id, "type": choice}
                    await ledb.insert_one(newuser)
                    await ctx.send('**Changes are saved**')

                elif stats['type'] == 1:
                    await ctx.send('**Command is already disabled**')

                else:
                    await ledb.update_one({
                        "id": ctx.guild.id
                    }, {"$set": {
                        "type": choice
                    }})

                    await ctx.send('**Changes are saved | Command disabled**')

        else:
            await ctx.send("**It can be enable/disable only**")




def setup(client):
    client.add_cog(Enalevel(client))