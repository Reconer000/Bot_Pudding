import os
import re
import json
import asyncio
import discord
import requests
from discord import utils
from discord.ext import commands, tasks

config_file_location = "config/config.json"
sc_file_location = "config/secret_config.json"

with open(config_file_location, "r") as config_file:
    config = json.load(config_file)

with open(sc_file_location, "r") as sc_file:
    sc = json.load(sc_file)

client_id = sc["osu!api"][0]
client_secret = sc["osu!api"][1]

data = {
    'client_id': client_id,
    'client_secret': client_secret,
    'grant_type': 'client_credentials',
    'scope': 'public'
}


class osu(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.get_ranks.start()


    @commands.command(name="reg", brief="register your osu profile with the bot. -reg <osu id>", pass_context=True)
    async def reg(self, ctx, input: str):

        # Stop get_ranks loop to avoid exceptions
        self.get_ranks.cancel()
        server_id = str(ctx.guild.id)

        # Check for -s and member permissions
        if input == "-s":
            perms = discord.abc.GuildChannel.permissions_for(ctx, ctx.message.author)
            if perms.manage_roles == True:
                if server_id not in config["osu_config"]["servers"]:
                    try:

                        # Add server object to config.json
                        new_data = {"users": {}}
                        config["osu_config"]["servers"][server_id] = new_data
                        os.remove(config_file_location)
                        with open(config_file_location, 'w') as config_file:
                            json.dump(config, config_file, indent=2)

                            await ctx.send("Successfully registered {}.".format(ctx.guild.name))
                    except:
                        await ctx.send("Failed.")
                else:
                    await ctx.send("Current server already registered.")
            else:
                await ctx.send("You dont have the manage roles permission.")

        # Check for -d
        elif input == "-d":
            try:

                # Remove object from config.json
                if str(ctx.message.author.id) in config["osu_config"]["servers"][server_id]["users"]:
                    tmp = config["osu_config"]["servers"][server_id]["users"]
                    del tmp[str(ctx.message.author.id)]
                    config["osu_config"]["servers"][server_id]["users"] = tmp
                    os.remove(config_file_location)
                    with open(config_file_location, 'w') as config_file:
                        json.dump(config, config_file, indent=2)

                    await ctx.send("Successfully removed {}.".format(ctx.message.author.name))
                else:
                    await ctx.send("User not found.")
            except:
                await ctx.send("Failed.")

        # Check for osu id
        elif "https://osu.ppy.sh/users/" in input:
            try:
                users = config["osu_config"]["servers"][server_id]["users"]
                if str(ctx.message.author.id) not in users:
                    try:

                        # Add user's discord and osu id to server object
                        config["osu_config"]["servers"][server_id]["users"][str(ctx.message.author.id)] = int(re.sub("[https://osu.ppy.sh/users/]", "", input))
                        os.remove(config_file_location)
                        with open(config_file_location, 'w') as config_file:
                            json.dump(config, config_file, indent=2)

                        await ctx.send("{} successfully registered as {}.".format(ctx.message.author.name, input))
                    except Exception as e:
                        await ctx.send("Failed. "+e)
                else:
                    await ctx.send("You're already registered.")
            except:
                await ctx.send("Current server not registered. -reg -s (with manage roles perms) WARNING: this will make 10 new roles")

        # User didnt send osu profile or use -s 
        else:
            await ctx.send("Please use your osu profile link.")

        self.get_ranks.start()


    @tasks.loop(minutes=10.0)
    async def get_ranks(self):

        # Used for users who are in multiple servers with
        # this bot.
        cache = {
        }

        # Get osu!api oauth2 token
        auth = requests.post("https://osu.ppy.sh/oauth/token", data=data).json()
        token = auth.get('access_token')


        async def set_roles(rank):
            for name in role_names:
                role = utils.get(guild.roles, name = name)

                # Add roles to server if they dont exist
                if role == None:
                    await guild.create_role(name = name, hoist = True)

                # Convert role names into ints to determine what role to give each user
                rank_ranges = [int(j) for j in re.sub("[k]", '', name).split("-")]
                if rank_ranges[0] <= rank <= rank_ranges[1]:
                    await member.add_roles(role)
                else:
                    await member.remove_roles(role)


        for server_id in config["osu_config"]["servers"]:
            server = config["osu_config"]["servers"][server_id]
            guild = self.client.get_guild(int(server_id))
            users = server.get("users")
            role_names = config["osu_config"]["roles"]
            print(guild.name)

            for discord_id in users:
                osu_id = users.get(discord_id)
                member = await guild.fetch_member(int(discord_id))

                if discord_id in cache:
                    print(" Using cache for {}.".format(member.name))
                    await set_roles(cache.get(discord_id))
                else:
                    print(" Getting {} stats.".format(member.name))

                    # Limit osu requests to make sure you dont get 
                    # yelled at by peppy. Dont remove this. 
                    # Rate limits exist for a reason
                    await asyncio.sleep(1.2)

                    # Get user rank from osu.ppy.sh with oauth2 token
                    user_data = requests.get("https://osu.ppy.sh/api/v2/users/{}/osu".format(osu_id), headers={"Authorization": "Bearer {}".format(token)}).json()
                    user_stats = user_data.get("statistics")
                    rank = user_stats.get("global_rank") // 1000

                    cache[discord_id] = rank
                    await set_roles(rank)


def setup(client):
    client.add_cog(osu(client))
