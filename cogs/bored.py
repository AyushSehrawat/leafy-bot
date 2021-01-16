from discord.ext import commands
import requests
import discord


class Boring(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bored cog loaded successfully')

    @commands.command(
        description="Sends you a activity which you can do while you are bored"
    )
    async def activity(self, ctx, persons=1):
        if persons == None:
            await ctx.send('You forgot person value')
        else:
            persons = str(persons)
            URL = f'https://www.boredapi.com/api/activity/?participants={persons}'

            def check_valid_status_code(request):
                if request.status_code == 200:
                    return request.json()

                return False

            def get_activity():
                request = requests.get(URL)
                data = check_valid_status_code(request)

                return data

            activity = get_activity()
            temp_check = int(persons)
            if not activity or temp_check > 8:
                await ctx.channel.send(
                    "Couldn't get activity from API. Try again later.")

            else:
                acti = activity['activity']
                typee = activity['type'].capitalize()
                embed = discord.Embed(
                    timestamp=ctx.message.created_at,
                    title='Bored?',
                    description='I am here to tell something you can do :)',
                    color=0xff0000)
                embed.add_field(name='Activity', value=f'{acti}', inline=False)
                embed.add_field(name='Type', value=f'{typee}', inline=False)
                embed.set_footer(
                    text=f'Requested By: {ctx.author.name}',
                    icon_url=f'{ctx.author.avatar_url}')
                await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Boring(client))
