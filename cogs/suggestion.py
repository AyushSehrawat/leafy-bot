from discord.ext import commands
import requests
import discord
from discord.ext.commands import cooldown, BucketType


class Suggestion(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Suggestion cog loaded successfully')

    @commands.command(
        cooldown_after_parsing=True,description="Suggest Us :) ")
    @cooldown(1, 7200, BucketType.user)
    async def suggest(self,ctx,*,msg):
        channel_only = self.client.get_channel(793713329582768149)
        up = "\U0001f44d"
        down = "\U0001f44e"

        embed= discord.Embed(
            timestamp=ctx.message.created_at,
            title=f'Suggestion By {ctx.author}')
        embed.add_field(name='Suggestion',value=msg)
        embed.set_footer(
                text=f'Wait until your suggestion is approved',
                icon_url=f'{ctx.author.avatar_url}')
        message = await channel_only.send(embed=embed)
        await message.add_reaction(up)
        await message.add_reaction(down)
        await ctx.message.delete()
        await ctx.send('**Your Suggestion Has Been Recorded**')
        

    



def setup(client):
    client.add_cog(Suggestion(client))