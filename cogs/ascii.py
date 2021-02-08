import aiohttp
from discord.ext import commands


class Fancy(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Ascii cog loaded successfully")

    @commands.command(description="Sends the ascii generated text of given message")
    async def ascii(self, ctx, *, ascii_text):
        if len(ascii_text) <= 12:
            words = "+".join(ascii_text)
            #
            async with aiohttp.ClientSession() as session:
                #
                async with session.get(
                    f"https://artii.herokuapp.com/make?text={words}"
                ) as response:
                    #
                    fancy_text = await response.text()
                    await ctx.send(f"```{fancy_text}```")
                    await ctx.send(f"{ctx.author.mention}")
                    await ctx.message.delete()

        elif len(ascii_text) > 12:
            await ctx.send("Bruh why more than 12 characters? Tell me why?")
        else:
            await ctx.send("Something Went Wrong")


def setup(client):
    client.add_cog(Fancy(client))
