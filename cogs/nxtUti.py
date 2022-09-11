import random

import nextcord
from dotenv import load_dotenv
from nextcord import Interaction
from nextcord.ext import commands

load_dotenv()


class InviteBnt(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        url = "https://nextcord.com/api/oauth2/authorize?client_id=822001531007008808&permissions=8&scope=bot%20applications.commands"
        self.add_item(nextcord.ui.Button(label="Invite bot", url=url))


class Nxtutility(commands.Cog, name="Utilities"):
    """Miscelanious commands are here :)"""

    COG_EMOJI = "👽"

    def __init__(self, bot):
        self.bot = bot

    # ping command
    @commands.command(
        title="ping", description="Shows you the latency between the server and the bot"
    )
    async def ping(self, ctx):
        """
        Shows you the latency between the server and the bot
        """
        embed = nextcord.Embed(
            title="Latency is",
            description=f"{round(self.bot.latency * 1000)}ms",
            color=nextcord.Color.from_rgb(236, 41, 36),
        )
        embed.set_footer(text=f"{self.bot.user}")
        await ctx.send(embed=embed)

    # whois command
    @commands.command(aliases=["userinfo", "aboutuser", "ui"])
    async def whois(self, ctx, member: nextcord.Member = None):
        """
        Displays the requested user's information
        """
        member = ctx.author if not member else member
        roles = [role for role in member.roles]
        if len(roles) > 10:
            abc = " Too many roles ,(DAMN!!)"
            embed = nextcord.Embed(colour=member.colour)
            embed.set_author(name=f"User info - {member}")
            embed.set_thumbnail(url=member.avatar)
            embed.set_footer(text=f"Requested by {ctx.author}")
            embed.add_field(name="ID: ", value=member.id, inline=True)
            embed.add_field(
                name="Created account at: ",
                value=member.created_at.strftime("%a, %d %#B %Y, %I:%M %p UTC"),
            )
            embed.add_field(
                name="Joined server at: ",
                value=member.joined_at.strftime("%a, %d %#B %Y, %I:%M %p UTC"),
            )
            embed.add_field(name=f"Roles ({len(roles)})", value=f"{abc} ", inline=True)
            embed.add_field(
                name="Top role:", value=member.top_role.mention, inline=True
            )
            embed.add_field(name="Bot? ", value=member.bot, inline=True)
            embed.add_field(name="Status", value=member.status, inline=True)
        elif len(roles) < 10:
            embed = nextcord.Embed(colour=member.color)
            embed.set_author(name=f"User info - {member}")
            embed.set_thumbnail(url=member.avatar)
            embed.set_footer(text=f"Requested by {ctx.author}")
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
                value=" ".join([role.mention for role in roles]),
                inline=True,
            )
            embed.add_field(
                name="Top role:", value=member.top_role.mention, inline=True
            )
            embed.add_field(name="Bot? ", value=member.bot, inline=True)
            embed.add_field(name="Status:", value=member.status, inline=True)
        await ctx.send(embed=embed)

    @commands.command(
        aliases=["server", "sinfo", "si"],
        pass_context=True,
        invoke_without_command=True,
    )
    async def serverinfo(self, ctx, *, msg=""):
        """Various info about the server. [p]help server for more info."""
        if msg:
            server = None
            try:
                float(msg)
                server = self.bot.get_guild(int(msg))
                if not server:
                    return await ctx.send("Server not found.")
            except:
                for i in self.bot.guilds:
                    if i.name.lower() == msg.lower():
                        server = i
                        break
                if not server:
                    return await ctx.send(
                        "Could not find server. Note: You must be a member of the server you are trying to search."
                    )
        else:
            server = ctx.message.guild

        online = 0
        for i in server.members:
            if (
                str(i.status) == "online"
                or str(i.status) == "idle"
                or str(i.status) == "dnd"
            ):
                online += 1
        all_users = []
        for user in server.members:
            all_users.append("{}#{}".format(user.name, user.discriminator))
        all_users.sort()
        all = "\n".join(all_users)

        channel_count = len(
            [x for x in server.channels if type(x) == nextcord.channel.TextChannel]
        )

        role_count = len(server.roles)
        emoji_count = len(server.emojis)
        members = server.members
        bots = filter(lambda m: m.bot, members)
        bots = set(bots)

        em = nextcord.Embed(color=0xEA7938)
        em.add_field(name="Name", value=server.name)
        em.add_field(name="Owner", value=server.owner, inline=False)
        em.add_field(name="Members", value=server.member_count)
        em.add_field(name="Currently Online", value=online)
        em.add_field(name="Text Channels", value=str(channel_count))
        em.add_field(name="Region", value=server.region)
        em.add_field(name="Verification Level", value=str(server.verification_level))
        # em.add_field(name='Highest role', value=server.rol)
        em.add_field(name="Number of roles", value=str(role_count))
        em.add_field(name="Number of emotes", value=str(emoji_count))
        # hastebin_of_users = '[List of all {} users in this server]({})'.format(server.member_count)
        em.add_field(name="Users", value=server.member_count)
        em.add_field(
            name="Created At",
            value=server.created_at.__format__("%A, %d. %B %Y @ %H:%M:%S"),
        )
        em.add_field(name="Bots Online", value=str(len(bots)))
        em.set_thumbnail(url=server.icon.url)
        em.set_author(name="Server Info", icon_url=ctx.author.avatar.url)
        em.set_footer(text="Server ID: %s" % server.id)
        await ctx.send(embed=em)

    # invite command
    @commands.command()
    async def invite(self, ctx):
        """Return Invite link for this bot"""
        view = InviteBnt()
        await ctx.send("Here's you invitation ✉", view=view)


    #huzaifa's cmd by Executioner
    @commands.command(aliases=["wih"],hidden=True)
    async def whoishot(self, ctx):
        """A command made for LostUnlost to truly let everyone know is place
        **The absolute chad , The hottest are few to go with**
        """
        phO = random.choice(["https://media.discordapp.net/attachments/860544191238242384/924256079699910676/20211225_140336.jpg",
        "https://cdn.discordapp.com/attachments/864324213850636358/901467271602511922/20210701_200611.jpg",
        "https://media.discordapp.net/attachments/824647650573811764/965145476590616646/20220417_100319.jpg"])
        await ctx.reply(phO)

def setup(bot):
    bot.add_cog(Nxtutility(bot))
