import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import psutil
import os
from pymongo import MongoClient
import motor.motor_asyncio
import nest_asyncio
nest_asyncio.apply()

mongo_url = os.environ.get('MONGO_URL')

cluster = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
predb = cluster["discord"]["prefix"]

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('New help Cog Loaded Succesfully')

    @commands.command()
    async def help(self, ctx, choice=None):
        stats = await predb.find_one({"guild": ctx.guild.id})
        if stats is None:
            a = '--'
        else:
            a = stats['prefix']
        if choice is None:
            embed = discord.Embed(
                timestamp=ctx.message.created_at,
                description=
                f'```Please choose any one```\n`{a}help general`\n`{a}help mod`\n`{a}help fun`\n`{a}help info`\n`{a}help music`\n`{a}help setup`\n`{a}help extra`\n',
                color=0xff0000
            )
            embed.set_author(
                name=f"Leafy Help Commands",
                icon_url=self.client.user.avatar_url)
            
            embed.set_footer(
                text=f'Requested By: {ctx.author.name}',
                icon_url=f'{ctx.author.avatar_url}')

            await ctx.send(embed=embed)

        elif choice == 'general':
            embed = discord.Embed(
                timestamp=ctx.message.created_at,
                description=
                f'```Here are the general commands```\n`{a}rank - To know your rank`\n`{a}lb - To see the leaderboard`\n`{a}ping - To know bot latency`\n`{a}avatar <user/id>- See the avatar`\n`{a}wiki <msg> - Search on wikipedia`\n`{a}search <msg> - See top results`\n`{a}note <msg> - Make a note for you and save it`\n`{a}notes - See your note(s)`\n`{a}trash - Delete your note(s)`\n`{a}poll <question> - Creates an interactive poll`\n`{a}quickpoll <*question , options>`\n`{a}remind/reminder/notify <time s/m/h/d> <*msg>`\n`{a}pip/pypi <name>`\n',
                color=0xff0000
            )
            embed.set_author(
                name=f"Leafy General Commands",
                icon_url=self.client.user.avatar_url)
            
            embed.set_footer(
                text=f'Requested By: {ctx.author.name}',
                icon_url=f'{ctx.author.avatar_url}')

            await ctx.send(embed=embed)

        elif choice =='mod':
            embed = discord.Embed(
                timestamp=ctx.message.created_at,
                description=
                f'```Here are the mod commands```\n`{a}kick <user/id>`\n`{a}ban <user/id>`\n`{a}unban <id>`\n`{a}softban <user/id> - Ban and then unban (to clear messages)`\n`{a}clear <num> - Clear the given amount of messages`\n`{a}warn <user/id> <num> <reason> - Warns a user and generates a case id`\n`{a}warns - To see your warns`\n`{a}case <user/id> - Show the warns of a user`\n`{a}clearwarns/cw <user/id> - Clears all the warns`\n`{a}mute - Mute a user`\n`{a}unmute - Unmute the muted user`\n`{a}slow <time(in s )> - Set slowmode to given time`\n`{a}rslow - Reset the slowmode back to 0`\n`{a}block <user/id> - Block user from sending message in that channel`\n`{a}unblock <user/id> - Unblock the blocked user`\n`{a}lock - Lock a channel`\n`{a}unlock - Unlocks the locked channel`\n`{a}addrole <user/id> <role> - Adds the given role`\n`{a}unrole <user/id> <role> - Removes the given role`\n',
                color=0xff0000
            )
            embed.set_author(
                name=f"Leafy Moderation Commands",
                icon_url=self.client.user.avatar_url)
            
            embed.set_footer(
                text=f'Requested By: {ctx.author.name}',
                icon_url=f'{ctx.author.avatar_url}')

            await ctx.send(embed=embed)

        elif choice=='fun':
            embed = discord.Embed(
                timestamp=ctx.message.created_at,
                description=
                f"```Here are the fun commands```\n`{a}ascii <text>`\n`{a}ga <name> - Guess the age of given name`\n`{a}cat`\n`{a}dog`\n`{a}password <length>`\n`{a}ly <song_name>`\n`{a}sendnuke <user/id>`\n`{a}roast <user/id>`\n`{a}8ball <question>`\n`{a}choose <*args>`\n`{a}choosebestof <*args>`\n`{a}lenny`\n`{a}meme`\n`{a}joke`\n`{a}ipinfo <ip/website>`\n`{a}calc <expression>`\n`{a}activity <num> - Tells activity for given number of persons`\n`{a}remind <time> <type> <*msg> - To set a timer`\n`{a}guess - Guess the person you thought`\n`{a}bird`\n`{a}fml`\n`{a}sadcat`\n`{a}say <*msg>`\n{a}bj`\n",
                color=0xff0000
            )
            embed.set_author(
                name=f"Leafy Fun Commands",
                icon_url=self.client.user.avatar_url)
            
            embed.set_footer(
                text=f'Requested By: {ctx.author.name}',
                icon_url=f'{ctx.author.avatar_url}')

            await ctx.send(embed=embed)

        elif choice == 'info':
            embed = discord.Embed(
                timestamp=ctx.message.created_at,
                description=
                f"```Here are the info commands```\n`{a}bot - Info about bot`\n`{a}user/ui <user/id> - Info about user`\n`{a}server/si - Info about server`\n`{a}mem/memcount - Total members in server`\n",
                color=0xff0000
            )
            embed.set_author(
                name=f"Leafy Info Commands",
                icon_url=self.client.user.avatar_url)
            
            embed.set_footer(
                text=f'Requested By: {ctx.author.name}',
                icon_url=f'{ctx.author.avatar_url}')

            await ctx.send(embed=embed)
        
        elif choice == 'music':
            embed = discord.Embed(
                timestamp=ctx.message.created_at,
                description=
                f"```Here are music commands```\n`{a}join - Join the voice channel`\n`{a}play <song_name> - Plays the given song`\n`{a}stop - Stops the playing song`\n`{a}pause - Pause the song`\n`{a}resume - Resume the paused song`\n`{a}skip - Skip the song`\n`{a}queue - Shows the queue`\n`{a}shuffle - Shuffles the queue`\n`{a}remove <num> - Removes the givem index number of song`\n`{a}leave - Leaves the voice channel`\n",
                color = 0xff0000
            )
            embed.set_author(
                name=f"Leafy Music Commands",
                icon_url=self.client.user.avatar_url)
            
            embed.set_footer(
                text=f'Requested By: {ctx.author.name}',
                icon_url=f'{ctx.author.avatar_url}')

            await ctx.send(embed=embed)

        elif choice == 'setup':
            embed = discord.Embed(
                timestamp=ctx.message.created_at,
                description=
                f"```Here are setup commands```\n`{a}level enable/disable - Enable or disable levelling`\n`{a}setprefix <new_prefix>`\n",
                color = 0xff0000
            )
            embed.set_author(
                name=f"Leafy Setup Commands",
                icon_url=self.client.user.avatar_url)
            
            embed.set_footer(
                text=f'Requested By: {ctx.author.name}',
                icon_url=f'{ctx.author.avatar_url}')

            await ctx.send(embed=embed)

        elif choice =='extra':
            embed = discord.Embed(
                timestamp=ctx.message.created_at,
                description=
                f"```Here are extra commands```\n`{a}invite - Invite leafy to your server or join our support server`\n`{a}vote - Vote leafy!`\n`{a}suggest <*msg> - Suggest directly into our support server`",
                color = 0xff0000
            )
            embed.set_author(
                name=f"Leafy Extra Commands",
                icon_url=self.client.user.avatar_url)
            
            embed.set_footer(
                text=f'Requested By: {ctx.author.name}',
                icon_url=f'{ctx.author.avatar_url}')

            await ctx.send(embed=embed)

        else:
            await ctx.send(f'**Not found! Use {ctx.prefix}help for more info**')



def setup(client):
    client.add_cog(Help(client))
