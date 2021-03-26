import discord
from discord.ext import commands


class cog_name(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="test")
    async def test(self, context):
        await context.send("LOPEZ")


def setup(client):
    client.add_cog(cog_name(client))
