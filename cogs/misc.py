import random
import discord
from discord import utils
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="roll", brief="default 100, max 1 million", pass_context=True)
    async def roll(self, ctx):
        dice = ctx.message.content[5:].strip()
        if dice == "":
            dice = "100"
        if int(dice) > 1000000:
            dice = "1000000000"
        result = random.randint(1, int(dice))
        await ctx.send("{} rolls {}".format(ctx.message.author.mention, str(result)))

    @commands.command(name="gtfo", brief="", pass_context=True)
    async def gtfo(self, ctx, role_name: str):
        total = 0
        if '_' in role_name:
            role_name = role_name.replace('_',' ')
        for i in ctx.guild.roles:
            if i.name == role_name:
                total += 1
                await i.delete(reason = 'gtfo')
        await ctx.send('{} {} deleted'.format(role_name, total))

def setup(client):
    client.add_cog(Misc(client))
