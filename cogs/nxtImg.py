import os
import random
import textwrap
from distutils import command
from io import BytesIO

import asyncpraw
import nextcord
from dotenv import load_dotenv
from nextcord import File
from nextcord.ext import commands
from PIL import Image, ImageChops, ImageDraw, ImageFont
# from pilmoji import Pilmoji

load_dotenv()


def circle(pfp, size=(215, 215)):

    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")

    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp


async def generate_meme():
    subreddits = [
        "dankmemes",
        "memes",
        "meme",
        "wholesomememes",
        "comedyheaven",
        "pewdiepiesubmissions",
        "KidsAreFuckingStupid",
        "cursedcomments",
        "HolUp",
        "blursedimages",
        "rareinsults",
    ]
    reddit = asyncpraw.Reddit(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        user_agent="Spacebot",
    )
    subreddit = await reddit.subreddit(random.choice(subreddits))
    all_subs = []
    async for submission in subreddit.hot(limit=20):
        if not submission.over_18:
            all_subs.append(submission)
    random_sub = random.choice(all_subs)
    name = random_sub.title
    url = random_sub.url
    em = nextcord.Embed(
        colour=nextcord.Colour.blurple(),
        title=name,
        url=f"https://reddit.com/{random_sub.id}",
    )
    em.set_image(url=url)
    #    em.set_author(name=f"Taken from r/{subreddit}, Score = {random_sub.score}")
    em.set_footer(text="Tip: If the interaction fails , try using >meme")
    await reddit.close()
    return em


class Nxtimages(commands.Cog, name="Images"):
    """Image commands"""

    COG_EMOJI = "🖼"

    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=["ps"])
    async def photoshop(self, ctx):
        """Photoshop's Images"""
        if ctx.invoked_subcommand is None:
            # await ctx.send("Photoshop's images \n **Tip : Try using** `>help photoshop`")
            await ctx.send_help("ps")

    @photoshop.command()
    async def wanted(self, ctx, user: nextcord.Member = None):
        """Atleast feel wanted by someone"""
        user = ctx.author if not user else user

        wanted = Image.open("utilites/photos/wanted.jpg")
        asset = user.avatar.with_format("jpg")
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((252, 252))
        wanted.paste(pfp, (106, 247))
        wanted.save("wanted-edited.jpg")
        try:
            await ctx.send(file=nextcord.File("wanted-edited.jpg"))
            wanted.close()
            os.remove("wanted-edited.jpg")
        except:
            await ctx.send("Error!")

    #!wanted error
    @wanted.error
    async def wanted_error(self, ctx, error):
        error = error
        if isinstance(error, commands.MissingRequiredArgument):
            arg = error.param.name
            await ctx.send(f"Argument `{arg}` is missing!!")
        else:
            message = f"Raised error\n```md\n<{error}>```"
            await ctx.send(message)
            await ctx.message.delete(delay=5)
            raise error

    @photoshop.command()
    async def kill(self, ctx, user: nextcord.Member = None):
        """Mudrder without trouble"""
        user = ctx.author if not user else user
        amogusimage = Image.open(f"utilites/photos/kill2.jfif")
        asset1 = user.avatar.with_format("jpg")
        asset2 = ctx.author.avatar.with_format("jpg")
        data1 = BytesIO(await asset1.read())
        data2 = BytesIO(await asset2.read())
        pfp = Image.open(data1)
        author = Image.open(data2)

        pfp = pfp.resize((55, 55))
        author = author.resize((55, 55))
        amogusimage.paste(author, (54, 58))
        amogusimage.paste(pfp, (170, 40))
        amogusimage.save("kill.jpg")
        try:
            await ctx.send(file=nextcord.File("kill.jpg"))
            amogusimage.close()
            os.remove("kill.jpg")
        except:
            await ctx.send("Error!")

    #!wanted error
    @wanted.error
    async def wanted_error(self, ctx, error):
        error = error
        if isinstance(error, commands.MissingRequiredArgument):
            arg = error.param.name
            await ctx.send(f"Argument `{arg}` is missing!!")
        else:
            message = f"Raised error\n```md\n<{error}>```"
            await ctx.send(message)
            await ctx.message.delete(delay=5)
            raise error

    @photoshop.command()
    async def disfine(self, ctx, user: nextcord.Member = None):
        """Short Visualization of your life."""
        user = ctx.author if not user else user

        wanted = Image.open("utilites/photos/finelol.jpeg")
        asset = user.avatar.with_format("jpg")
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((350, 350))
        wanted.paste(pfp, (730, 335))
        wanted.save("finelol.jpg")
        try:
            await ctx.send(file=nextcord.File("finelol.jpg"))
            wanted.close()
            os.remove("finelol.jpg")
        except:
            await ctx.send("Error!")

    #!disfine error
    @disfine.error
    async def disfine_error(self, ctx, error):
        error = error
        if isinstance(error, commands.MissingRequiredArgument):
            arg = error.param.name
            await ctx.send(f"Argument `{arg}` is missing!!")
        else:
            message = f"Raised error\n```md\n<{error}>```"
            await ctx.send(message)
            await ctx.message.delete(delay=5)
            raise error

    @commands.command()
    async def meme(self, ctx):
        """Gets a random meme from various subreddits"""

        class MemeView(nextcord.ui.View):
            def __init__(self):
                super().__init__(timeout=10)

            @nextcord.ui.button(label="Next Meme", emoji="⏩", style=nextcord.ButtonStyle.blurple)
            async def next_meme(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
                await interaction.message.edit(embed=await generate_meme())


            async def on_timeout(self):
                self.message.edit(embed=await generate_meme(),view=None)
        await ctx.send(embed=await generate_meme(), view=MemeView())

    @commands.command(aliases=["twt"])
    async def twitter(
        self,
        ctx,
        # member:nextcord.Member=None,
        *,
        message,
    ):
        """
        Express your opinions on twitter
        Either it being good or bad( _well not bad_ )
        In your made up twitter account cuz you dont have courage to post it your original one,
        """
        member = ctx.author
        img = Image.open("utilites/photos/twt.jpg")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("helveticaneue.ttf", 45)
        midfont = ImageFont.truetype("helveticaneue.ttf", 30)
        smlfont = ImageFont.truetype("helveticaneue.ttf", 20)
        #! Avatar
        pfp = member.avatar.with_size(256)
        data = BytesIO(await pfp.read())
        pfp = Image.open(data).convert("RGBA")
        pfp = circle(pfp, size=(90, 90))
        img.paste(pfp, (20, 22), pfp)  # 20,20
        #! Username
        member_name, member_discriminator = str(member).split("#")
        draw.text((140, 20), str(member_name), (0, 0, 0), font=midfont)
        draw.text((160, 55), str(member), (0, 0, 0), font=smlfont)
        #! Text
        msg = "".join(message)
        cx, cy = (30, 130)
        lines = textwrap.wrap(msg, width=50)
        y_offset = (len(lines)) / 2
        y_text = cy - y_offset

        for line in lines:
            w, h = font.getsize(line)
            draw.text((cx, y_text), line, (0, 0, 0), font=font)
            img.save("twt-edited.jpg")
            y_text += h

        with open("twt-edited.jpg", "rb") as f:
            img = File(f)
            await ctx.channel.send(file=img)
        img.close()
        os.remove("twt-edited.jpg")

    @twitter.error
    async def twitter_error(self, ctx, error):
        if isinstance(error, FileNotFoundError):
            await ctx.send("Please enter the `message`")
        elif isinstance(error, commands.MissingRequiredArgument):
            arg = error.param.name
            await ctx.send(f"Argument `{arg}` is missing!!")
        else:
            message = f"Raised error\n```{error}```"
            await ctx.send(message)
            await ctx.message.delete(delay=5)
            raise error


def setup(bot):
    bot.add_cog(Nxtimages(bot))


# Archives
# @commands.command(name='twt')
# async def twt(self ,ctx, *args):

#     msg = " ".join(args)
#     font = ImageFont.truetype("helveticaneue.ttf", 50)
#     img = Image.open("utilites/photos/twt.jpg")
#     # cx, cy = (350, 230)
#     cx, cy = (100, 200)

#     lines = textwrap.wrap(msg, width=20)
#     print(lines)
#     w, h = font.getsize(msg)
#     y_offset = (len(lines)*h)/2
#     y_text = cy-(h/2) - y_offset

#     for line in lines:
#         draw = ImageDraw.Draw(img)
#         w, h = font.getsize(line)
#         draw.text((cx-(w/2), y_text), line, (0, 0, 0), font=font)
#         img.save("twt-edited.jpg")
#         y_text += h

#     with open("twt-edited.jpg", "rb") as f:
#         img = File(f)
#         await ctx.channel.send(file=img)


# @commands.command(name='twt')
# async def twt(self ,ctx, *args):

#     msg = " ".join(args)
#     font = ImageFont.truetype("helveticaneue.ttf", 50)
#     img = Image.open("utilites/photos/twt.jpg")
#     # cx, cy = (350, 230)
#     cx, cy = (100, 200)

#     lines = textwrap.wrap(msg, width=20)
#     print(lines)
#     w, h = font.getsize(msg)
#     y_offset = (len(lines)*h)/2
#     y_text = cy-(h/2) - y_offset

#     for line in lines:
#         draw = ImageDraw.Draw(img)
#         w, h = font.getsize(line)
#         draw.text((cx-(w/2), y_text), line, (0, 0, 0), font=font)
#         img.save("twt-edited.jpg")
#         y_text += h

#     with open("twt-edited.jpg", "rb") as f:
#         img = File(f)
#         await ctx.channel.send(file=img)
