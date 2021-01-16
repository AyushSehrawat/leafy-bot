from discord.ext import commands
import random as rng
from collections import Counter
from typing import Optional


class plural:
    def __init__(self, value):
        self.value = value

    def __format__(self, format_spec):
        v = self.value
        singular, sep, plural = format_spec.partition('|')
        plural = plural or f'{singular}s'
        if abs(v) != 1:
            return f'{v} {plural}'
        return f'{v} {singular}'


class RNG(commands.Cog):
    """Utilities that provide pseudo-RNG."""

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('MG cog loaded successfully')

    @commands.command(description="Shows a random lenny")
    async def lenny(self, ctx):
        """Displays a random lenny face."""
        lenny = rng.choice([
            "( ͡° ͜ʖ ͡°)", "( ͠° ͟ʖ ͡°)", "ᕦ( ͡° ͜ʖ ͡°)ᕤ", "( ͡~ ͜ʖ ͡°)",
            "( ͡o ͜ʖ ͡o)", "͡(° ͜ʖ ͡ -)", "( ͡͡ ° ͜ ʖ ͡ °)﻿", "(ง ͠° ͟ل͜ ͡°)ง",
            "ヽ༼ຈل͜ຈ༽ﾉ"
        ])
        await ctx.send(lenny)

    @commands.command(
        description="Chooses a random val from given inputs")
    async def choose(self, ctx, *choices: commands.clean_content):
        """Chooses between multiple choices.
        To denote multiple choices, you should use double quotes.
        """
        if len(choices) < 2:
            return await ctx.send('Not enough choices to pick from.')

        await ctx.send(rng.choice(choices))

    @commands.command(
        aliases=["cbo"],
        description="Roll and chooses the best of given choices")
    async def choosebestof(self, ctx, times: Optional[int],
                           *choices: commands.clean_content):
        """Chooses between multiple choices N times.
        To denote multiple choices, you should use double quotes.
        You can only choose up to 10001 times and only the top 10 results are shown.
        """
        if len(choices) < 2:
            return await ctx.send('Not enough choices to pick from.')

        if times is None:
            times = (len(choices)**2) + 1

        times = min(10001, max(1, times))
        results = Counter(rng.choice(choices) for i in range(times))
        builder = []
        if len(results) > 10:
            builder.append('Only showing top 10 results...')
        for index, (elem, count) in enumerate(
                results.most_common(10), start=1):
            builder.append(
                f'{index}. {elem} ({plural(count):time}, {count/times:.2%})')

        await ctx.send('\n'.join(builder))


def setup(client):
    client.add_cog(RNG(client))
