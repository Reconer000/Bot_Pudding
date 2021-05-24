import json
import discord
from discord import utils
from discord.ext import commands


config_file_location = "config/config.json"

with open(config_file_location, "r") as config_file:
    config = json.load(config_file)


class Auto_Mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if str(message.channel.id) in config["automod"]["verify_channels"]:
            await message.author.add_roles(utils.get(message.author.guild.roles, id = int(config["automod"]["member_role"])))
            await message.delete()

def setup(client):
    client.add_cog(Auto_Mod(client))
