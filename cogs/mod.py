import asyncio
import os

import discord
from discord.ext import commands


class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Mod Cog Loaded Succesfully")

    @commands.command(description="Bans a member")
    @commands.has_permissions(ban_members=True)
    async def ban(
        self, ctx, member: discord.Member, *, reason=None, delete_message_days=7
    ):
        guild = ctx.guild
        if member == self.client.user:

            await ctx.send("**Haha, i am immortal**")

        elif guild.me.top_role < member.top_role:
            await ctx.send("**Member is higher than me in hierarchy**")
        elif member.bot:
            await ctx.send("**You cannot ban bot**")
        elif member == ctx.author:
            await ctx.send("**You cannot ban yourself**")
        else:

            await member.ban(reason=reason)
            embed = discord.Embed(
                title="Ban",
                description=f"{member.name} has been banned by {ctx.author.name}",
                color=0xFF000,
            )
            await ctx.send(embed=embed)

    @commands.command(aliases=["unban"], description="Unbans a member")
    @commands.has_permissions(ban_members=True)
    async def _unban(self, ctx, id: int):
        user = await self.client.fetch_user(id)
        await ctx.guild.unban(user)
        embed = discord.Embed(
            title="Unban",
            description=f"{id} has been unbanned by {ctx.author.name}",
            color=0xFF000,
        )
        await ctx.send(embed=embed)

    @commands.command(
        aliases=["del", "p"], description="Deletes the given amount of messages"
    )
    @commands.has_permissions(manage_channels=True)
    async def clear(self, ctx, amount=4):
        if amount > 200:
            await ctx.send("**Currently due to bot hosting we support only 200 limit**")
        else:
            await ctx.channel.purge(limit=amount + 1)
            msg = await ctx.send(f"**Purged {amount} messages**")
            await asyncio.sleep(2)
            await msg.delete()

    @commands.command(description="Kicks a member")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        guild = ctx.guild
        if member == self.client.user:
            await ctx.send("**Haha, i am immortal**")
        elif guild.me.top_role < member.top_role:
            await ctx.send("**Member is higher than me in hierarchy**")
        elif member.bot:
            await ctx.send("**You cannot kick bot**")
        elif member == ctx.author:
            await ctx.send("**You cannot kick yourself**")
        else:

            if member.top_role < ctx.author.top_role:
                await member.kick(reason=reason)
                embed = discord.Embed(
                    title="Kick",
                    description=f"{member.name} has been kicked by {ctx.author.name}",
                    color=0xFF000,
                )
                await ctx.send(embed=embed)

    @commands.command(
        description="Softbans a member ( Unban after ban to clear chat , to clear chat )"
    )
    @commands.has_permissions(kick_members=True)
    async def softban(self, ctx, member: discord.Member):
        guild = ctx.guild
        if member == self.client.user:
            await ctx.send("**Haha, i am immortal**")
        elif guild.me.top_role < member.top_role:
            await ctx.send("**Member is higher than me in hierarchy**")
        elif member.bot:
            await ctx.send("**You cannot ban bot**")
        elif member == ctx.author:
            await ctx.send("**You cannot ban yourself**")
        else:

            await member.ban(reason=None, delete_message_days=7)

            await ctx.guild.unban(member, reason=None)

            embed = discord.Embed(
                title="SoftBan",
                description=f"{member.name} has been softbanned by {ctx.author.name}",
                color=0xFF000,
            )
            await ctx.send(embed=embed)

    @commands.command(description="Mutes a member")
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, user: discord.Member, reason=None):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        guild = ctx.guild
        if user == self.client.user:
            await ctx.send("**Haha, i am immortal**")
        elif guild.me.top_role < user.top_role:
            await ctx.send("**Member is higher than me in hierarchy**")
        elif user.bot:
            await ctx.send("**You cannot mute bot**")
        elif user == ctx.author:
            await ctx.send("**You cannot mute yourself**")
        else:
            if not role:
                try:
                    muted = await ctx.guild.create_role(
                        name="Muted", reason="To use for muting"
                    )
                    for channel in ctx.guild.channels:
                        await channel.set_permissions(
                            muted,
                            send_messages=False,
                            read_message_history=False,
                            view_channels=True,
                            read_messages=False,
                        )
                except discord.Forbidden:
                    return await ctx.send(
                        "I have no permissions to make a muted role"
                    )  # self-explainatory
                await user.add_roles(muted)
                embed = discord.Embed(
                    title="Muted",
                    description=f"{user.name} has been muted",
                    color=0xFF000,
                )
                await ctx.send(embed=embed)

            elif role in user.roles:
                embed = discord.Embed(
                    title="Invalid usage",
                    description="User is already muted",
                    color=0xFF000,
                )
                await ctx.send(embed=embed)
            else:
                await user.add_roles(role)
                embed = discord.Embed(
                    title="Muted",
                    description=f"{user.name} has been muted",
                    color=0xFF000,
                )
                await ctx.send(embed=embed)

    @commands.command(description="Unmute the muted member")
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, user: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        guild = ctx.guild
        if guild.me.top_role < user.top_role:
            await ctx.send("**Member is higher than me in hierarchy**")
        elif role not in user.roles:
            embed = discord.Embed(
                title="Invalid usage",
                description="User is already unmuted",
                color=0xFF000,
            )
            await ctx.send(embed=embed)

        else:
            await user.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted"))
            embed = discord.Embed(
                title="Unmuted",
                description=f"{user.name} has been unmuted",
                color=0xFF000,
            )
            await ctx.send(embed=embed)

        ####################

    @commands.command(description="Adds the mentioned to role to mentioned/id memebr")
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, member: discord.Member, rolename: discord.Role):
        guild = ctx.guild
        if guild.me.top_role < member.top_role:
            await ctx.send("**Member is higher than me in hierarchy**")
        elif rolename in ctx.guild.roles:
            await member.add_roles(rolename)
            embed = discord.Embed(
                title="Add Role",
                description=f"Added {rolename} role to {member.name}",
                color=0xFF000,
            )
            embed.set_footer(
                text=f"Requested By: {ctx.author.name}",
                icon_url=f"{ctx.author.avatar_url}",
            )

            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                title="Error", description="Role not found", color=0xFF000
            )
            await ctx.send(embed=embed)

    @commands.command(description="Removed the mentioned role from mentioned user/id")
    @commands.has_permissions(manage_roles=True)
    async def unrole(self, ctx, member: discord.Member, rolename: discord.Role):
        guild = ctx.guild
        if guild.me.top_role < member.top_role:
            await ctx.send("**Member is higher than me in hierarchy**")
        elif rolename in ctx.guild.roles:

            await member.remove_roles(rolename)
            embed = discord.Embed(
                title="Remove role",
                description=f"Removed {rolename} role from {member.name}",
                color=0xFF000,
            )
            embed.set_footer(
                text=f"Requested By: {ctx.author.name}",
                icon_url=f"{ctx.author.avatar_url}",
            )

            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(
                title="Error", description="Role not found", color=0xFF000
            )
            await ctx.send(embed=embed)

    @commands.command(description="Locks the channel")
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel: discord.TextChannel = None):
        channel = ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        if overwrite.send_messages == False:
            embed = discord.Embed(
                title="Invalid usage",
                description="This channel is already locked",
                color=0xFF000,
            )
            embed.set_footer(
                text=f"Requested By: {ctx.author.name}",
                icon_url=f"{ctx.author.avatar_url}",
            )
            await ctx.send(embed=embed)
        else:
            channel = ctx.channel
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            embed = discord.Embed(
                title="Channel Locked",
                description="This channel is now Locked",
                color=0xFF000,
            )
            embed.set_footer(
                text=f"Requested By: {ctx.author.name}",
                icon_url=f"{ctx.author.avatar_url}",
            )
            await ctx.send(embed=embed)

    @commands.command(description="Unlocks the locked channel")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        channel = ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        if overwrite.send_messages == True:
            embed = discord.Embed(
                title="Invalid usage",
                description="This channel is already unlocked",
                color=0xFF000,
            )
            embed.set_footer(
                text=f"Requested By: {ctx.author.name}",
                icon_url=f"{ctx.author.avatar_url}",
            )
            await ctx.send(embed=embed)
        else:
            channel = ctx.channel
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.send_messages = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            embed = discord.Embed(
                title="Channel Unlocked",
                description="This channel is now unlocked",
                color=0xFF000,
            )
            embed.set_footer(
                text=f"Requested By: {ctx.author.name}",
                icon_url=f"{ctx.author.avatar_url}",
            )
            await ctx.send(embed=embed)

    @commands.command(description="Blocks a user from sending message in that channel")
    @commands.has_permissions(kick_members=True)
    async def block(self, ctx, member: discord.Member):
        guild = ctx.guild
        if member == self.client.user:
            await ctx.send("**Haha, i am immortal**")
        elif guild.me.top_role < member.top_role:
            await ctx.send("**Member is higher than me in hierarchy**")
        elif member.bot:
            await ctx.send("**You cannot block bot**")
        elif member == ctx.author:
            await ctx.send("**You cannot block yourself**")
        else:
            if member.permissions_in(ctx.channel).send_messages == False:
                embed = discord.Embed(
                    title="Invalid usage",
                    description=f"{member.mention} is already blocked",
                    color=0xFF000,
                )
                await ctx.send(embed=embed)
            else:
                #
                await ctx.channel.set_permissions(member, send_messages=False)
                embed = discord.Embed(
                    title="Block",
                    description=f"{member.mention} is blocked by {ctx.author.name}",
                    color=0xFF000,
                )
                await ctx.send(embed=embed)

    @commands.command(description="Unblocks the blocked user")
    @commands.has_permissions(kick_members=True)
    async def unblock(self, ctx, member: discord.Member):
        if member.permissions_in(ctx.channel).send_messages == True:
            embed = discord.Embed(
                title="Invalid usage",
                description=f"{member.mention} is already unblocked",
                color=0xFF000,
            )
            await ctx.send(embed=embed)

        else:
            await ctx.channel.set_permissions(member, send_messages=True)
            embed = discord.Embed(
                title="Unblock",
                description=f"{member.mention} is unblocked by {ctx.author.name}",
                color=0xFF000,
            )
            await ctx.send(embed=embed)

    @commands.command(description="Nukes a channel ( Clone and delete ) ")
    @commands.has_permissions(manage_channels=True)
    async def nuke(self, ctx, channel_name):
        channel_id = int("".join(i for i in channel_name if i.isdigit()))
        existing_channel = self.client.get_channel(channel_id)
        if existing_channel:
            await existing_channel.clone(reason="Has been nuked")
            await existing_channel.delete()
            embed = discord.Embed(
                title=f"Channel nuked || {ctx.author.name} || ", color=0x00FFFF
            )
            embed.set_image(
                url="https://media.tenor.com/images/e138ef6dcfc0f227e9ba27faf027c6ee/tenor.gif"
            )
            await ctx.author.send(embed=embed)
        else:
            await ctx.send(f"No channel named **{channel_name}** was found")


def setup(client):
    client.add_cog(Mod(client))
