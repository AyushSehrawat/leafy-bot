import os

import discord
import motor.motor_asyncio
import nest_asyncio
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
from pymongo import MongoClient

nest_asyncio.apply()
mongo_url = os.environ.get("MONGO_URL")

cluster = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)


notedb = cluster["discord"]["note"]


class Note(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Note cog loaded successfully")

    @commands.command(cooldown_after_parsing=True, description="Creates a note for you")
    @cooldown(1, 10, BucketType.user)
    async def note(self, ctx, *, message):
        message = str(message)
        print(message)
        stats = await notedb.find_one({"id": ctx.author.id})
        if len(message) <= 50:
            #
            if stats is None:
                newuser = {"id": ctx.author.id, "note": message}
                await notedb.insert_one(newuser)
                await ctx.send("**Your note has been stored**")
                await ctx.message.delete()

            else:
                x = notedb.find({"id": ctx.author.id})
                z = 0
                async for i in x:
                    z += 1
                if z > 2:
                    await ctx.send("**You cannot add more than 3 notes**")
                else:
                    newuser = {"id": ctx.author.id, "note": message}
                    await notedb.insert_one(newuser)
                    await ctx.send("**Yout note has been stored**")
                    await ctx.message.delete()

        else:
            await ctx.send("**Message cannot be greater then 50 characters**")

    @commands.command(description="Shows your note")
    async def notes(self, ctx):
        stats = await notedb.find_one({"id": ctx.author.id})
        if stats is None:
            embed = discord.Embed(
                timestamp=ctx.message.created_at,
                title="Notes",
                description=f"{ctx.author.mention} has no notes",
                color=0xFF0000,
            )
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                title="Notes", description=f"Here are your notes", color=0xFF0000
            )
            x = notedb.find({"id": ctx.author.id})
            z = 1
            async for i in x:
                msg = i["note"]
                embed.add_field(name=f"Note {z}", value=f"{msg}", inline=False)
                z += 1
            await ctx.author.send(embed=embed)
            await ctx.send("**Please check your private messages to see your notes**")

    @commands.command(description="Delete the notes , it's a good practice")
    async def trash(self, ctx):
        try:
            await notedb.delete_many({"id": ctx.author.id})
            await ctx.send("**Your notes have been deleted , thank you**")
        except:
            await ctx.send("**You have no record**")


def setup(client):
    client.add_cog(Note(client))
