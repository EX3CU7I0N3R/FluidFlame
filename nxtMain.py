# Importing neccesary modules
import nextcord as nxc
import nextcord
import os
from nextcord.ext import commands
from dotenv import load_dotenv
from rich.traceback import install
from rich.console import Console
from rich.progress import track
from rich.theme import Theme


install()
load_dotenv()

custom_theme = Theme({"success": "green", "error": "bold red"})


intents = nextcord.Intents.all()
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(">", "ff", "ff "),
    owner_ids=[612491216793239552, 620644659441565723],
    case_insensitive=True,
    intents=intents,
)
bot.remove_command("help")


# Adding up the cogs
for fn in os.listdir("./cogs"):
    if fn.startswith("nxt") and fn.endswith(".py"):
        bot.load_extension(f"cogs.{fn[:-3]}")
        print(f"Loaded 'cogs.{fn[:-3]}'")

# Manual (un)|(re)|loading
@bot.command(aliases=["dld"],hidden=True)
@commands.is_owner()
async def load(ctx, extension):
    try:
        if extension == "all":
            for fn in os.listdir("./cogs"):
                if fn.startswith("nxt") and fn.endswith(".py"):
                    bot.load_extension(f"cogs.{fn[:-3]}")
                    await ctx.reply(f"Loaded `'cogs.{fn[:-3]}'`")
        else:
            bot.load_extension(f"cogs.{extension}")
            await ctx.reply(f"Loaded {extension}")
    except:
        pass


@load.error
async def load_error(ctx: commands.Context, error: commands.CommandError):
    """
    "Handle load errors
    :param ctx: context
    :param error: Errors(ExtensionNotFound, ExtensionAlreadyLoaded, NoEntryPoint, ExtensionFailed)
    :return: None
    """
    if isinstance(error.__cause__, commands.ExtensionNotFound):
        message = (
            f"The extension `{error.__cause__.name.strip('cogs.')}` cannot be found."
        )
    elif isinstance(error.__cause__, commands.ExtensionAlreadyLoaded):
        message = (
            f"The extension `{error.__cause__.name.strip('cogs.')}` is already loaded"
        )
    elif isinstance(error.__cause__, commands.NoEntryPointError):
        message = f"There is no entry point for the extension`{error.__cause__.name.strip('cogs.')}`"
    elif isinstance(error.__cause__, commands.ExtensionFailed):
        message = f"Can't load the extension `{error.__cause__.name.strip('cogs.')}`\nManual reload needed "
    else:
        message = f"Raised error\n```md\n<{error}>```"
    await ctx.send(message)
    await ctx.message.delete(delay=5)


@bot.command(aliases=["dunld"],hidden=True)
@commands.is_owner()
async def unload(ctx, extension):
    if extension == "all":
        for fn in os.listdir("./cogs"):
            if fn.startswith("nxt") and fn.endswith(".py"):
                bot.unload_extension(f"cogs.{fn[:-3]}")
                await ctx.reply(f"Unloaded `'cogs.{fn[:-3]}'`")
    else:
        bot.unload_extension(f"cogs.{extension}")
        await ctx.reply(f"Unloaded {extension}")


@unload.error
async def unload_error(ctx: commands.Context, error: commands.CommandError):
    """
    "Handle load errors
    :param ctx: context
    :param error: Errors(ExtensionNotFound, ExtensionAlreadyLoaded, NoEntryPoint, ExtensionFailed)
    :return: None
    """
    if isinstance(error.__cause__, commands.ExtensionNotFound):
        message = (
            f"The extension `{error.__cause__.name.strip('cogs.')}` cannot be found."
        )
    elif isinstance(error.__cause__, commands.ExtensionNotLoaded):
        message = (
            f"The extension `{error.__cause__.name.strip('cogs.')}` is already unloaded"
        )
    elif isinstance(error.__cause__, commands.NoEntryPointError):
        message = f"There is no entry point for the extension`{error.__cause__.name.strip('cogs.')}`"
    elif isinstance(error.__cause__, commands.ExtensionFailed):
        message = f"Can't load the extension `{error.__cause__.name.strip('cogs.')}`\nManual restart needed "
    else:
        message = f"Raised error\n```md\n<{error}>```"
    await ctx.send(message)
    await ctx.message.delete(delay=5)



@bot.command(aliases=["dreld", "re"],hidden=True)
@commands.is_owner()
async def reload(ctx, extension):
    if extension == "all":
        for fn in os.listdir("./cogs"):
            if fn.startswith("nxt") and fn.endswith(".py"):
                bot.reload_extension(f"cogs.{fn[:-3]}")
                await ctx.reply(f"Reloaded `'cogs.{fn[:-3]}'`")
    else:
        bot.reload_extension(f"cogs.{extension}")
        await ctx.reply(f"Reloaded {extension}")


@reload.error
async def reload_error(ctx: commands.Context, error: commands.CommandError):
    """
    "Handle load errors
    :param ctx: context
    :param error: Errors(ExtensionNotFound, ExtensionAlreadyLoaded, NoEntryPoint, ExtensionFailed)
    :return: None
    """
    if isinstance(error.__cause__, commands.ExtensionNotFound):
        message = (
            f"The extension `{error.__cause__.name.strip('cogs.')}` cannot be found."
        )
    elif isinstance(error.__cause__, commands.ExtensionNotLoaded):
        message = f"The extension `{error.__cause__.name.strip('cogs.')}` was unloaded"
    elif isinstance(error.__cause__, commands.NoEntryPointError):
        message = f"There is no entry point for the extension`{error.__cause__.name.strip('cogs.')}`"
    elif isinstance(error.__cause__, commands.ExtensionFailed):
        message = f"Can't load the extension `{error.__cause__.name.strip('cogs.')}`\nManual restart needed "
    else:
        message = f"Raised error\n```md\n<{error}>```"
    await ctx.send(message)
    await ctx.message.delete(delay=5)


bot.console = Console(theme=custom_theme)

# On Ready events
@bot.event
async def on_ready():
    game = nxc.Game("with the my code and crying")
    await bot.change_presence(status=nxc.Status.dnd, activity=game)
    print("Logged in as")
    bot.console.print(bot.user.name, style="success")
    bot.console.print(bot.user.id, style="success")
    print("---------------------------------------------")



# On command error
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        stra = str(ctx.author)
        bot.console.print(f"{error} by {stra}-{ctx.author.id}",style="error")
    elif isinstance(error, commands.NSFWChannelRequired):
        embed = nxc.Embed(
            title="Nsfw Channel Required !!",
            description=f"Nsfw is not enabled in this channel",
        )
        embed.set_image(url="https://i.imgur.com/oe4iK5i.gif")
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        arg = error.param.name
        await ctx.send(f"Argument `{arg}` is missing!!")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Uh.... Member `not` found !")
    elif isinstance(error, commands.MissingPermissions):
        emba = nextcord.Embed(
            title="Ban Error",
            description="Missing permissons",
            color=nextcord.Color.from_rgb(236, 41, 36),
        )
        await ctx.send(embed=emba)
    elif isinstance(error, commands.NotOwner):
        await ctx.send(
            f"This command is owner only...\n_Anyway how did you manage to find it ??_"
        )
    else:
        raise error


# import time
# start_time = time.time()
# #Looped functions
# async def statusUpdate():
#     import time
#     while True:
#         await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=" Watching code for - %s time -" % (time.time() - start_time)))
        
#         time.sleep(15)

bot.run(os.getenv("BOT_TOKEN"))
