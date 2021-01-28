from discord.ext import commands
import aiohttp
import os
import discord


class Pypi(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Pypi cog loaded successfully')

    @commands.command(aliases=['pip'])
    async def pypi(self, ctx,package_name=None):
        if package_name is None:
            await ctx.send('**Missing package name**')
        else:
            if len(package_name) >= 15:
                await ctx.send('**<:sus:802765928961671208> Big package name **')
            else:
                url = f"https://pypi.org/pypi/{package_name}/json"
                async with aiohttp.ClientSession() as cs:
                    async with cs.get(url) as res:
                        if res.status == 404:
                            await ctx.send('**No such package found**')
                        else:
                            r = await res.json()
                            author = r['info']['author']
                            desc = r['info']['description']
                            if len(desc) > 500:
                                d = desc[:500]
                                desc = f'{d}...'
                            else:
                                pass
                            home = r['info']['home_page']
                            name = r['info']['name']
                            summary = r['info']['summary']
                            if len(summary) > 100:
                                sum = summary[:100]
                                summary = f'{sum}...'
                            else:
                                pass

                            desc = desc.replace("#", " ")
                            project = r['info']['project_url']
                            v = r['info']['version']

                            embed = discord.Embed(
                                color=0xff0000
                            )
                            embed.add_field(
                                name = 'Name',
                                value=f'{name}',
                                inline=True
                            )
                            embed.add_field(
                                name='Version',
                                value=f'{v}',
                                inline=True
                            )
                            embed.add_field(
                                name='Author',
                                value=f'{author}',
                                inline=True
                            )
                            embed.add_field(
                                name='Summary',
                                value=f'{summary}',
                                inline=False
                            )
                            embed.add_field(
                                name='\n**Description**',
                                value=f'{desc}',
                                inline=False
                            )
                            embed.add_field(
                                name='**Links**',
                                value=f'[Home Page]({home}) \n [Page]({project})',
                                inline=False
                            )

                            embed.set_thumbnail(
                                url='https://miro.medium.com/max/1080/1*ciPCmwyO6C79SLVU5Rj50w.jpeg'
                            )

                            await ctx.send(embed=embed)




def setup(client):
    client.add_cog(Pypi(client))
