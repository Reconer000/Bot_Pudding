import json
import config
import discord
from discord import Message
from discord.ext.commands import Bot
from discord.ext import commands, tasks

config.init()

config_file_location = "config/config.json"
sc_file_location = "config/secret_config.json"

with open(config_file_location, "r") as config_file:
    config = json.load(config_file)

with open(sc_file_location, "r") as sc_file:
    sc = json.load(sc_file)

extensions = config.get("Cogs")
OWNER = config.get("Owner")
BOT_PREFIX = config.get("Prefix")

client = Bot(command_prefix=BOT_PREFIX)
version = "2.1.0-x"


@client.event
async def on_ready():
    global version
    print("Version: {}".format(version))
    print("kekbot ready")
    print("Logged in as {}".format(client.user.name))
    print("The bot id is {}".format(client.user.id))
    print("On these servers:")
    servers = list(client.guilds)
    for x in range(len(servers)):
        print(" " + servers[x - 1].name)

    for extension in extensions:
        try:
            print("loading {}".format(extension))
            client.load_extension(extension)
        except Exception as e:
            print(f"Failed to load {extension}.")

    print('------------')


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found")

    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Incorrect format")


@client.command(hidden=True)
async def ver(ctx):
    global version
    await ctx.send(version)


@client.command(hidden=True)
async def shutdown(ctx):
    if ctx.author.guild_permissions.administrator:
        await client.logout()
    elif str(ctx.message.author.id) != "":
        await ctx.send("I'm sorry, {}. I'm afraid I can't do that.".format(ctx.message.author))
    return


@client.command(hidden=True)
async def cog(ctx, method: str, extension: str):
    extension = "cogs." + extension

    if ctx.author.guild_permissions.administrator:

        if extension in extensions:
            try:
                exec("client.{}_extension(extension)".format(method))
                await ctx.send("ye")
            except:
                await ctx.send("ne")
        else:
            await ctx.send("me")
        return


@client.command(hidden=True)
async def purge(ctx, llimit: str):
    if ctx.author.guild_permissions.administrator:
        try:
            await ctx.channel.purge(limit=int(llimit))
        except:
            return


@client.command(name="info")
async def info(ctx):
    await ctx.send("https://github.com/Reconer000/Bot_Pudding")

client.run(sc["TOKEN"])
