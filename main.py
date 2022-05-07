import os
import discord
import discord.ext
from datetime import datetime
from discord import ActivityType
from discord.ext import commands, tasks

intents = discord.Intents().all()
client = discord.Client()
client = commands.Bot(intents=intents, command_prefix='~', help_command=None)


async def game_check():
    general = client.get_channel(760150471351992330)
    now = datetime.now().timestamp()
    for guild in client.guilds:
        for member in guild.members:
            try:
                if len(member.activities) != 0:
                    print(member)
                    for s in member.activities:
                        if s.type == ActivityType.playing:
                            time_playing = now - s.start.timestamp()
                            print(s.name+", playing for "+str(round(time_playing/60, 2))+" minutes")
                            if s.application_id == 356869127241072640:
                                # the application ID seems to change with different game states, so unsure how this
                                # works long enough to send ban message 
                                if time_playing < 70:
                                    pass
                                    # This section somehow never gets triggered

                                    # await general.send(member.mention+" you have been detected doing a prohibited "
                                    #                                  "activity: desist immediately. You have 5 "
                                    #                                  "minutes to cease your actions before you are "
                                    #                                  "displaced.")
                                elif time_playing > 300:
                                    # Properly sends message, but doesn't ban, causing spam

                                    # await general.send(member.mention+"for refusing to desist with prohibited "
                                    #                                  "activities (partaking in League of Legends for "
                                    #                                  "more than 5 minutes), you are now being "
                                    #                                  "displaced. ")
                                    member.ban(reason="Playing League of Legends for more than 5 minutes.")
                            elif s.application_id == 432980957394370572:
                                if time_playing < 70:
                                    pass
                                    # This section somehow never gets triggered

                                    # await general.send(member.mention+" you have been detected doing a prohibited "
                                    #                                  "activity: desist immediately. You have 15 "
                                    #                                  "minutes to cease your actions before you are "
                                    #                                  "displaced.")
                                elif time_playing > 900:
                                    # Properly sends message, but doesn't ban, causing spam

                                    # await general.send(member.mention+"for refusing to desist with prohibited "
                                    #                                  "activities (partaking in Fortnite for "
                                    #                                  "more than 15 minutes), you are now being "
                                    #                                  "displaced. ")
                                    member.ban(reason="Playing Fortnite for more than 15 minutes.")
                            print("Application ID: "+str(s.application_id))
            except AttributeError:
                print("Attribute Error")
            except Exception as e:
                print(e)


@tasks.loop(minutes=1)
async def run_check_auto():
    print("-------[Auto Game Check]--["+str(datetime.now().strftime("%B %d, %H:%M"))+"]--")
    await game_check()


@client.event
async def on_ready():
    print("bot ready")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="~help"))
    run_check_auto.start()


@client.command()
async def ping(ctx):
    await ctx.send("received")


@client.command()
async def help(ctx, arg=None):
    if arg is not None:
        arg = str(arg).lower()
    match arg:
        case "help":
            embed = discord.Embed(title="help Command",
                                  description="",
                                  color=0x00a82a)
        case "roulette":
            embed = discord.Embed(title="roulette Command",
                                  description="",
                                  color=0x00a82a)
        case "kick":
            embed = discord.Embed(title="kick Command",
                                  description="",
                                  color=0x00a82a)
        case "ban":
            embed = discord.Embed(title="ban Command",
                                  description="",
                                  color=0x00a82a)
        case "info":
            embed = discord.Embed(title="info Command",
                                  description="",
                                  color=0x00a82a)
        case _:
            embed = discord.Embed(title="Commands",
                                  description="",
                                  color=0x00a82a)
            embed.add_field(name="Prefix", value="~ (Tilde)", inline=True)
            embed.add_field(name="Arguments", value="<optional> [required]", inline=True)
            embed.add_field(name="Help", value="help <command>    - A list of all Commands: You are already here!",
                            inline=False)
            embed.add_field(name="Roulette", value="not yet implemented", inline=False)
            embed.add_field(name="Kick", value="kick [Member ID]    - Kick a user while letting them join back",
                            inline=False)
            embed.add_field(name="Ban", value="ban [Member ID]    - Ban a user, permanently stopping them from "
                                              "joining the server.", inline=False)
            embed.add_field(name="Info", value="info <Member ID>    - Basic information panel on the user",
                            inline=False)
            embed.set_footer(text="for a detailed description on each command, use ~help [command].")
    embed.set_author(name=str(datetime.now().strftime("%Y %m %d")))
    await ctx.send(embed=embed)


# TODO implement timeout roulette


@client.command()
async def kick(ctx, member: discord.Member):
    if ctx.message.author.guild_permissions.kick_members:
        await member.kick(reason=None)
        await ctx.send("Fuck you, "+member.mention+", get kicked.")
    else:
        await ctx.send("Not enough perms to kick...")


@client.command()
async def ban(ctx, member: discord.Member):
    if ctx.message.author.guild_permissions.ban_members:
        await member.ban(reason=None)
        await ctx.send("Fuck you, "+member.mention+", get banned.")
    else:
        await ctx.send("Not enough perms to banned...")


@client.command()
async def arg_test(ctx, arg):
    await ctx.channel.send(arg)


@client.command()
async def force_check(ctx):
    await ctx.channel.send("forcing check, check the console for details.")
    print("----------------------------------[Forced Game Check]----------------------------------")
    await game_check()


@client.command()
async def info(ctx, arg=None):
    user: discord.member = ctx.author
    try:
        user = await ctx.guild.fetch_member(int(arg))
    except Exception as e:
        print(e)
        await ctx.channel.send("error getting user, using author instead...")
    embed = discord.Embed(title="Info Panel",
                          description="A short information panel on the specified user",
                          color=user.colour)
    embed.set_author(name=user.name, icon_url=user.avatar_url)
    embed.add_field(name="Status", value=user.raw_status, inline=False)
    embed.add_field(name="User", value=user, inline=True)
    embed.add_field(name="Joined", value=user.joined_at.strftime("%Y %B %d"), inline=True)
    embed.add_field(name="Highest Role", value=user.top_role, inline=False)
    embed.set_footer(text="Requested by: {}".format(ctx.author.display_name))
    await ctx.send(embed=embed)


@client.command()
async def check(ctx, arg: int = None):
    user: discord.member = ctx.author
    try:
        user = await ctx.guild.get_member(arg)
    except Exception as e:
        print(str(arg)+", type: "+str(type(arg)))
        print(e)
        await ctx.channel.send("Could not get user")
    print(user.activities)
    await ctx.channel.send(user.activities)


client.run(os.getenv("TOKEN"))
