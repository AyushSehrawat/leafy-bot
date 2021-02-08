import os

import discord
import motor.motor_asyncio
import nest_asyncio
from discord.ext import commands

nest_asyncio.apply()

mongo_url = os.environ.get("MONGO_URL")

cluster = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
levelling = cluster["discord"]["levelling"]

isitenabled = cluster["discord"]["enalevel"]


class Levelsys(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Levelsys cog loaded successfully")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild is not None:
            try:
                stats2 = await isitenabled.find_one({"id": message.guild.id})

            except:
                newuser = {"id": message.guild.id, "type": 1}
                await isitenabled.insert_one(newuser)
            if stats2 is None:
                newuser = {"id": message.guild.id, "type": 1}
                await isitenabled.insert_one(newuser)
                a = 1
            else:
                a = stats2["type"]

            #
            if a == 0:
                #
                stats = await levelling.find_one({"id": message.author.id})
                if not message.author.bot:
                    #
                    if stats is None:
                        newuser = {"id": message.author.id, "xp": 100}
                        levelling.insert_one(newuser)

                    else:
                        xp = stats["xp"] + 5
                        levelling.update_one(
                            {"id": message.author.id}, {"$set": {"xp": xp}}
                        )

                        lvl = 0

                        while True:
                            if xp < ((50 * (lvl ** 2)) + (50 * (lvl))):
                                break
                            lvl += 1
                        xp -= (50 * ((lvl - 1) ** 2)) + (50 * (lvl - 1))

                        if xp == 0:
                            await message.channel.send(
                                f"Well done {message.author.mention} You levelled up to **level: {lvl}**"
                            )

        else:
            pass

    @commands.command(aliases=["xp", "r"], description="Shows your xp and global rank")
    async def rank(self, ctx):
        stats2 = await isitenabled.find_one({"id": ctx.guild.id})
        if stats2 is None:
            newuser = {"id": ctx.guild.id, "type": 1}
            await isitenabled.insert_one(newuser)
            a = 1
        else:
            a = stats2["type"]

        if a == 0:
            #

            stats = await levelling.find_one({"id": ctx.author.id})
            if stats is None:
                embed = discord.Embed(
                    description=f"You haven't sent any messages, no rank !!!"
                )

                await ctx.channel.send(embed=embed)

            else:
                xp = stats["xp"]
                lvl = 0
                rank = 0

                while True:
                    if xp < ((50 * (lvl ** 2)) + (50 * (lvl))):
                        break
                    lvl += 1
                xp -= (50 * ((lvl - 1) ** 2)) + (50 * (lvl - 1))

                boxes = int((xp / (200 * ((1 / 2) * lvl))) * 20)
                rankings = levelling.find().sort("xp", -1)

                async for x in rankings:
                    rank += 1
                    if stats["id"] == x["id"]:
                        break

                embed = discord.Embed(
                    timestamp=ctx.message.created_at,
                    title=f"{ctx.author.name}'s Level stats",
                    color=0xFF0000,
                )
                embed.add_field(name="Name", value=f"{ctx.author.mention}", inline=True)
                embed.add_field(
                    name="XP", value=f"{xp}/{int(200* ((1/2)*lvl))}", inline=True
                )
                embed.add_field(name="Global Rank", value=f"{rank}", inline=True)
                embed.add_field(name="Level", value=f"{lvl}", inline=True)
                embed.add_field(
                    name="Progress Bar [lvl]",
                    value=boxes * ":blue_square:"
                    + (20 - boxes) * ":white_large_square:",
                    inline=False,
                )
                embed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.channel.send(embed=embed)

        else:
            await ctx.send("**Levelling is disabled here**")

    @commands.command(
        aliases=["db", "leaderboard", "lb"], description="Shows server leaderboard"
    )
    async def dashboard(self, ctx):
        stats2 = await isitenabled.find_one({"id": ctx.guild.id})
        if stats2 is None:
            newuser = {"id": ctx.guild.id, "type": 1}
            await isitenabled.insert_one(newuser)
            a = 1
        else:
            a = stats2["type"]

        if a == 0:
            #
            rankings = levelling.find().sort("xp", -1)
            i = 1
            embed = discord.Embed(
                timestamp=ctx.message.created_at, title="Rankings", color=0xFF0000
            )
            async for x in rankings:
                try:
                    temp = ctx.guild.get_member(x["id"])
                    tempxp = x["xp"]
                    embed.add_field(
                        name=f"{i} : {temp.name}", value=f"XP: {tempxp}", inline=False
                    )
                    i += 1
                except:
                    pass
                if i == 11:
                    break

            embed.set_footer(
                text=f"Requested By: {ctx.author.name}",
                icon_url=f"{ctx.author.avatar_url}",
            )

            await ctx.channel.send(embed=embed)

        else:
            await ctx.send("**Levelling is disabled here**")


def setup(client):
    client.add_cog(Levelsys(client))
