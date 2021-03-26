
import discord
from discord import utils
from discord.ext import commands
from utils import fileloader, logd


config = fileloader.j("config/config.json")
automod_config = config.get("Automod_config")


class Auto_Mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in automod_config.get("protected_channels"):
            try:
                if message.attachments[0].url.endswith(tuple(automod_config.get("allowed_files"))):
                    pass
                else:
                    await message.delete()
                    await message.channel.send("That filetype cannot be sent here.")
            except:
                return

        elif message.channel.id in tuple(automod_config.get("verify_channel")):
            await message.author.add_roles(utils.get(message.author.guild.roles, name = automod_config.get("member_role")))
            print(message.author.guild)
            await message.delete()


def setup(client):
    client.add_cog(Auto_Mod(client))

    #this is all fucking stupid
