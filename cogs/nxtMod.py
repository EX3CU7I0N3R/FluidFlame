import datetime
from io import BytesIO

import nextcord
from dotenv import load_dotenv
from nextcord import ButtonStyle
from nextcord.ext import commands
from nextcord.ui import Button, View
from PIL import Image, ImageChops, ImageDraw, ImageFont

load_dotenv()

"""
                +   Notes   +

* Image Profile UI command   https://youtu.be/A0VNsgkO7CA
TODO: Advanced User Info With Button for moderators
"""


class BanConfirm(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @nextcord.ui.button(label="Confirm", style=nextcord.ButtonStyle.red)
    async def confirm(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await interaction.response.send_message("Confirming", ephemeral=True)
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @nextcord.ui.button(label="Cancel", style=nextcord.ButtonStyle.blurple)
    async def cancel(
        self, button: nextcord.ui.Button, interaction: nextcord.Interaction
    ):
        await interaction.response.send_message("Cancelling", ephemeral=True)
        self.value = False
        self.stop()


async def bAn(ctx, member: nextcord.Member, *, reason=None):
    """
    Ban a member from the respected guild
    """
    view = BanConfirm()
    await ctx.send(f"Do you want to ban `{member}`?", view=view)
    # Wait for the View to stop listening for input...
    await view.wait()
    if view.value is None:
        await ctx.send("Timed out...")
    elif view.value:
        if ctx.author == member:
            await ctx.send("Why Do you want to ban yourself?")
        # elif member == ctx.guild_owner:
        #     await ctx.send(f"Don't even bother... `{member}` is the owner of this guild")

        else:
            await member.ban(reason=reason)
            roles = [role for role in member.roles]
            abc = " Too many roles ,(DAMN!!)"
            embed = nextcord.Embed(
                title="Banned",
                description=f"`{member.name}` at {datetime.datetime.now()} was banned ",
                color=nextcord.Color.from_rgb(236, 41, 36),
                timestamp=datetime.datetime.utcnow(),
            )
            embed.add_field(name="ID: ", value=member.id, inline=True)
            embed.add_field(
                name="Created account at: ",
                value=member.created_at.strftime("%a, %d %#B %Y, %I:%M %p UTC"),
            )
            embed.add_field(
                name="Joined server at: ",
                value=member.joined_at.strftime("%a, %d %#B %Y, %I:%M %p UTC"),
            )
            embed.add_field(
                name=f"Roles ({len(roles)})",
                value="Too many roles"
                if len(roles) > 10
                else " ".join([role.mention for role in roles]),
                inline=True,
            )
            embed.add_field(
                name="Top role:", value=member.top_role.mention, inline=True
            )
            embed.add_field(name="Bot? ", value=member.bot, inline=True)
            embed.set_thumbnail(
                url="https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.pngfind.com%2Fmpng%2FmRhwww_banned-logo-png-banned-transparent-png%2F&psig=AOvVaw3FWTH_n8sMiGye54rOACSq&ust=1607403201664000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCICn2N-Ju-0CFQAAAAAdAAAAABAD"
            )
            embed.set_footer(text="FluidFlame")
            await ctx.send(embed=embed)
            print(
                f"Banned \nMember Name:{member.name}\nMember Id:{member.id}\nIn Channel Id:{ctx.channel}\nIn Server Id:{ctx.server}\nDateTime:{datetime.datetime.now()}"
            )
    else:
        await ctx.send("Cancelled...")


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


class Nxtmoderation(commands.Cog, name="Moderation"):
    """Great responsibility"""

    COG_EMOJI = "👮‍♂️"

    def __init__(self, bot):
        self.bot = bot

    # *Clear Command
    @commands.command(aliases=["purge"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        """
        Delete's a specified amount of content from a channel
        """
        if amount is None:
            amount = 1
        embed = nextcord.Embed(
            title="Clearing.....",
            description="",
            color=nextcord.Color.from_rgb(236, 41, 36)
        )
        # embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)
        await ctx.send(embed=embed)
        await ctx.channel.purge(limit=amount + 2)

    #!clear error
    @clear.error
    async def clear_error(self, ctx, error):
        error = error
        # if isinstance(error, commands.MissingRequiredArgument):
        #     arg = error.param.name
        #     await ctx.send(f"Argument `{arg}` is missing!!")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"YOU STOP RIGHT THERE\nYou Are Missing Permision")
        else:
            message = f"Raised error\n```md\n<{error}>```"
            await ctx.send(message)
            await ctx.message.delete(delay=5)
            raise error

    # *Ban
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: nextcord.Member, *, reason=None):
        """
        Ban a member from the respected guild
        """
        await bAn(ctx, member=member, reason=reason)

    #!ban error
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            emba = nextcord.Embed(
                title="Ban Error",
                description="Missing permissons",
                color=nextcord.Color.from_rgb(236, 41, 36),
            )
            await ctx.send(embed=emba)
        elif isinstance(error, commands.MissingRequiredArgument):
            arg = error.param.name
            await ctx.send(f"Argument `{arg}` is missing!!")
        elif isinstance(error.__cause__, nextcord.Forbidden):
            await ctx.send(
                f"Forbidden, You are trying to ban the owner ??\n\*_InValid Error?? Ask The Dev_*"
            )
        else:
            message = f"Raised error\n```md\n<{error}>```"
            await ctx.send(message)
            raise error

    # *Unban
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        """
        Unbans a user from the respected guild. Usage >unban [xyz#1234]
        """
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"Unbanned {user.name}#{user.discriminator}")

    #!unban error
    @unban.error
    async def unban_error(self, ctx, error):
        error = error
        if isinstance(error, commands.MissingRequiredArgument):
            arg = error.param.name
            await ctx.send(f"Argument `{arg}` is missing!!")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"YOU STOP RIGHT THERE\nYou Are Missing Permision")
        else:
            message = f"Raised error\n```md\n<{error}>```"
            await ctx.send(message)
            await ctx.message.delete(delay=5)
            raise error

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: nextcord.Member, *, reason=None):
        guild = ctx.message.guild
        mutedRole = nextcord.utils.get(guild.roles, name="Muted")

        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")

            for channel in guild.channels:
                await channel.set_permissions(
                    mutedRole,
                    speak=False,
                    send_messages=False,
                    read_message_history=True,
                    read_messages=False,
                )
        embed = nextcord.Embed(
            title="muted",
            description=f"{member.mention} was muted ",
            colour=nextcord.Colour.light_gray(),
        )
        embed.add_field(name="reason:", value=reason, inline=False)
        await ctx.send(embed=embed)
        await member.add_roles(mutedRole, reason=reason)
        await member.send(f" you have been muted from: {guild.name} reason: {reason}")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, user: nextcord.Member):
        """Unmutes a user."""
        rolem = nextcord.utils.get(ctx.guild.roles, name="Muted")
        if rolem not in user.roles:
            return await ctx.send("User is not muted.")
        embed = nextcord.Embed(
            title=f"User {user.name} has been unmuted.", color=0x00FF00
        )
        embed.add_field(name="Welcome back!", value=":open_mouth:")
        # embed.set_thumbnail(url= user.avatar.url)
        await ctx.send(embed=embed)
        await user.remove_roles(rolem)
        await self.bot.mongoIO.unmuteUser(user, ctx.guild)

    @commands.command(aliases=["manageuser", "usermanage", "um"])
    async def usermanager(self, ctx, member: nextcord.Member = None):
        """
        Take actions from requested user's information
        """

        if not member:
            member = ctx.author
        Name, Nick, Id, Status, Top_role, Bot = (
            str(member),
            member.display_name,
            str(member.id),
            str(member.status),
            str(member.top_role),
            str(member.bot),
        )
        created_at = member.created_at.strftime("%a %b\n%B %Y")
        joined_at = member.joined_at.strftime("%a %b\n%B %Y")
        # TODO : banner

        base = Image.open("utilites/photos/base2.png").convert("RGBA")
        background = Image.open("utilites/photos/bg.png").convert("RGBA")
        pfp = member.avatar.with_size(256)
        data = BytesIO(await pfp.read())
        pfp = Image.open(data).convert("RGBA")
        Name = f"{Name[:16]}.." if len(Name) > 16 else Name
        Nick = f"AKA - {Name[:17]}.." if len(Nick) > 17 else f"AKA - {Nick}"
        draw = ImageDraw.Draw(base)
        pfp = circle(pfp, size=(140, 140))
        font = ImageFont.truetype("helveticaneue.ttf", 23)
        akafont = ImageFont.truetype("helveticaneue.ttf", 17)
        subfont = ImageFont.truetype("helveticaneue.ttf", 17)

        base.paste(pfp, (30, 98), pfp)
        draw.text((175, 155), Name, font=font)
        draw.text((175, 200), Nick, font=akafont)

        draw.text((42, 310), Id, font=subfont)
        draw.text((300, 310), Status.upper(), font=subfont)
        draw.text((42, 400), Bot, font=subfont)
        draw.text((250, 400), Top_role, font=subfont)
        draw.text((42, 480), created_at, font=subfont)
        draw.text((250, 480), joined_at, font=subfont)
        background.paste(base, (0, 0), base)
        with BytesIO() as a:
            background.save(a, "PNG")
            a.seek(0)
            banBnt = Button(
                label="You can't ban yourself Ban(Disabled) "
                if member == ctx.author
                else f"Ban {member}",
                style=ButtonStyle.danger,
                disabled=True if member == ctx.author else False,
            )

            async def hi_callback(interaction):
                await bAn(ctx, member)

            banBnt.callback = hi_callback
            myvieW = View(timeout=20)
            myvieW.add_item(banBnt)

            await ctx.send(
                "placeholder msg", view=myvieW, file=nextcord.File(a, "profile.png")
            )

    @commands.has_permissions(manage_messages=True)
    @commands.command()
    async def clean(self, ctx):
        """Cleans the chat of the bot's messages."""

        def is_me(m):
            return m.author == self.bot.user

        await ctx.message.channel.purge(limit=100, check=is_me)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def softban(self, ctx, member: nextcord.Member, *, reason=None):
        """Kicks a members and deletes their messages."""
        await member.ban(reason=f"Softban - {reason}")
        await member.unban(reason="Softban unban.")
        await ctx.send(f"Done. {member.name} was softbanned.")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, user: nextcord.Member, *, reason: str):
        """Warn a member via DMs"""
        warning = (
            f"🔴**WARNING ISSUED**🔴 \n> In **{ctx.guild}**\n> From **{ctx.author}**\n> For *{reason}*"
        )
        if not reason:
            warning = f"You have been **warned**\n> In **{ctx.guild}**\nFrom **{ctx.author}**"
        try:
            await user.send(warning)
        except nextcord.Forbidden:
            return await ctx.send(
                "The user has disabled DMs for this guild or blocked the bot."
            )
        await ctx.send(f"**{user}** has been **warned**")


# """


#!                                 Archives                                   !


# """


# @commands.command()
# @commands.is_owner()
# async def profile(self,ctx,member:nextcord.member = None):
#     if not member:
#         member = ctx.author
#     Name , Nick , Id , Status , Top_role , Bot = str(member) ,member.display_name , str(member.id) ,str(member.status) ,str(member.top_role) ,str(member.bot)
#     created_at = member.created_at.strftime("%a %b\n%B %Y")
#     joined_at = member.joined_at.strftime("%a %b\n%B %Y")
#     #TODO : banner

#     base =Image.open("utilites/photos/base.png").convert("RGBA")
#     background = Image.open("utilites/photos/bg.png").convert("RGBA")

#     pfp = member.avatar.with_size(256)
#     data = BytesIO(await pfp.read())
#     pfp = Image.open(data).convert("RGBA")
#     Name = f"{Name[:16]}.." if len(Name) > 16 else Name
#     Nick = f"AKA - {Name[:17]}.." if len(Nick) > 17 else f"AKA - {Nick}"
#     draw = ImageDraw.Draw(base)
#     pfp = circle(pfp,size=(215,215))
#     font = ImageFont.truetype("helveticaneue.ttf",38)
#     akafont = ImageFont.truetype("helveticaneue.ttf",30)
#     subfont = ImageFont.truetype("helveticaneue.ttf",25)

#     draw.text((280,240),Name,font = font)
#     draw.text((270,315),Nick,font = akafont)
#     draw.text((65,490),Id,font = subfont)
#     draw.text((405,490),Status,font=subfont)
#     draw.text((65,635),Top_role,font=subfont)
#     draw.text((405,635),Bot,font =subfont)
#     draw.text((65,770),created_at,font=subfont)
#     draw.text((405,770),joined_at,font =subfont)
#     base.paste(pfp,(56,158),pfp)
#     background.paste(base,(0,0),base)
#     with BytesIO() as a:
#         background.save(a,"PNG")
#         a.seek(0)
#         await ctx.send(file=nextcord.File(a,"profile.png"))


# @commands.command()
# async def setprefix(self,ctx,prefix = None):
#     if prefix is None:
#         return
#     async with aiosqlite.connect("prefixs.db") as db:
#         async with db.cursor() as cursor:
#             await cursor.execute('SELECT prefix FROM prefixs WHERE guild = ?',(ctx.guild.id,))
#             data = await cursor.fetchone()
#             if data is None:
#                 await cursor.execute('UPDATE prefixs SET prefix = ? WHERE guild = ?',(ctx.prefix,ctx.guild.id,))
#                 await ctx.send(f"Updated prefix to `{prefix}`")
#             else:
#                 await cursor.execute('INSERT INTO prefixs(prefix, guild) VALUES (?,?)',(">",ctx.guild.id,))
#                 await cursor.execute('SELECT prefix FROM prefixs WHERE guild = ?',(ctx.guild.id,))
#                 data = await cursor.fetchone()
#                 if data is None:
#                     await cursor.execute('UPDATE prefixs SET prefix = ? WHERE guild = ?',(ctx.prefix,ctx.guild.id,))
#                     await ctx.send(f"Updated prefix to `{prefix}`")
#                 else:
#                     return
#         await db.commit()


def setup(bot):
    bot.add_cog(Nxtmoderation(bot))
