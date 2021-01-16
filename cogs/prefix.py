import discord
from discord.ext import commands
from pymongo import MongoClient
from discord.ext.commands import cooldown, BucketType

import os
import motor.motor_asyncio
import nest_asyncio
nest_asyncio.apply()

mongo_url = os.environ.get('MONGO_URL')

cluster = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)

predb = cluster["discord"]["prefix"]


class Prefix(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Prefix cog loaded successfully')

    @commands.command(
        cooldown_after_parsing=True,description="Changes Bot prefix for this server")
    @cooldown(1, 10, BucketType.user)
    @commands.has_permissions(administrator=True)
    async def setprefix(self,ctx,new_prefix):
        if len(new_prefix) > 3:
            embed = discord.Embed(
                timestamp=ctx.message.created_at,
                title='Error',
                description='Looks like the prefix is very big <:nah:796621598752899072>',
                color=0xff0000
            )
            await ctx.send(embed=embed)
        else:

            new_prefix = str(new_prefix)
            stats = await predb.find_one({"guild": ctx.guild.id})

            if stats is None:
                updated= {"guild":ctx.guild.id, "prefix": new_prefix}
                await predb.insert_one(updated)
                embed = discord.Embed(
                    title="Prefix",
                    description = f"This server prefix is now {new_prefix}",
                    color=0xff0000
                )
                await ctx.send(embed=embed)

            else:
                await predb.update_one({
                    "guild": ctx.guild.id
                }, {"$set": {
                    "prefix": new_prefix
                }})

                embed = discord.Embed(
                    timestamp=ctx.message.created_at,
                    title="Prefix",
                    description = f"This server prefix is now {new_prefix}",
                    color=0xff0000
                )
                await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Prefix(client))
