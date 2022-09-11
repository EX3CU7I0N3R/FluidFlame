import datetime
import random
import asyncio
import mysql.connector as Mysql
import nextcord
from nextcord import ChannelType, Interaction, SlashOption
from nextcord.ext import commands
from collections import OrderedDict

"""
THE FOLLOWING FUNCTIONS REQUIRED TO MAINTAIN AND USE THE ECONOMY PART OF THE FLUIDFLAME BOT ,

INFOMATION

?   MySQL
*   DB_HOST = "localhost"
*   DB_USER = "root"
*   DB_PASSWD = "root"
!   DB_NAME = "discordBot_db"

SOURCE/CREDITS
https://github.com/CODING-PALACE/economy-bot-discord.py/tree/main/economy%20with%20MYSQL
"""


DB_HOST = "localhost" # or your selected port/id address
DB_USER = "root"# Enter the user name which you created / added in your database (or) just use root as username
DB_PASSWD = "root" # Enter the password of your added user or the root user ( default )
DB_NAME = "discordBot_db" # Enter your Database Name which you created !


def convert_str_to_number(x):
    total_stars = 0
    num_map = {'K':1000, 'M':1000000, 'B':1000000000}
    if x.isdigit():
        total_stars = int(x)
    else:
        if len(x) > 1:
            total_stars = float(x[:-1]) * num_map.get(x[-1].upper(), 1)
    return int(total_stars)

async def open_bank(user):
    columns = ["wallet", "bank"] # You can add more Columns in it !

    db = Mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, database=DB_NAME)
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM economy WHERE userID = {user.id}")
    data = cursor.fetchone()
    if data is None:
        cursor.execute(f"INSERT INTO economy(userID) VALUES({user.id})")
        db.commit()
        for name in columns:
            cursor.execute(f"UPDATE economy SET {name} = 0 WHERE userID = {user.id}")
        db.commit()
        cursor.execute(f"UPDATE economy SET wallet = 5000 WHERE userID = {user.id}")
        db.commit()
    cursor.close()
    db.close()


async def get_bank_data(user):
    db = Mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, database=DB_NAME)
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM economy WHERE userID = {user.id}")
    users = cursor.fetchone()
    cursor.close()
    db.close()
    return users


async def update_bank(user, amount=0, mode="wallet"):
    db = Mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, database=DB_NAME)
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM economy WHERE userID = {user.id}")
    data = cursor.fetchone()
    if data is not None:
        cursor.execute(f"UPDATE economy SET {mode} = {mode} + {amount} WHERE userID = {user.id}")
        db.commit()
    cursor.execute(f"SELECT {mode} FROM economy WHERE userID = {user.id}")
    users = cursor.fetchone()
    cursor.close()
    db.close()
    return users

async def get_lb():
    db = Mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, database=DB_NAME)
    cursor = db.cursor()
    cursor.execute("SELECT userID, wallet + bank FROM economy ORDER BY wallet + bank DESC")
    users = cursor.fetchall()
    cursor.close()
    db.close()
    return users


rshop = {
    #TODO   alt + shift + up/down arrow
    "watch" : {"cost":100 , "key":1 , "info":"It's a watch"},
    "mobile" : {"cost":1000 , "key":2 , "info":"It's a mobile"},
    "laptop" : {"cost":10000 , "key":3 , "info":"It's a laptop"},
    "airpods" : {"cost":400 , "key":4 , "info":"They are airpods"},
    "burger" : {"cost":10 , "key":5 , "info":"It's a burgurr"},
    "sandwich" : {"cost":5 , "key":6 , "info":"It's a sandwich"},
}

async def invdata_dict(user):
    db = Mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, database=DB_NAME)
    cursor = db.cursor()
    temp1 = []
    temp2 = []
    zipp  = {}
    await open_inv(user)
    await update_invDB()
    users = await get_inv_data(user)
    for i in range(1,len(users)):
        temp1.append(users[i])
    cursor.execute(f"DESC inventory;")
    data = cursor.fetchall()
    for i in range(1, len(data)):
        ndata = data[i][0]
        temp2.append(ndata)
    zipp = dict(zip(temp2,temp1))
    return zipp

async def update_invDB():
    db = Mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, database=DB_NAME)
    cursor = db.cursor()
    list1 =[]
    for j in rshop:
        list1.append(j)

    list2 = []
    cursor.execute(f"DESC inventory;")
    data = cursor.fetchall()
    for i in range(1, len(data)):
        ndata = data[i][0]
        list2.append(ndata)

    #* Missing items
    ntA = set(list1).difference(list2)
    for k in ntA:
        query = f"ALTER TABLE inventory \
            ADD {k} INT DEFAULT 0"
        cursor.execute(query)
    
    return ntA



async def open_inv(user):
    db = Mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, database=DB_NAME)
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM inventory WHERE userID = {user.id}")
    data = cursor.fetchone()
    if data is None:
        cursor.execute(f"INSERT INTO inventory(userID) VALUES({user.id})")
        for item in rshop:
            item_name = item
            cursor.execute(f"UPDATE inventory SET {item_name} = 0 WHERE userID = {user.id}")
        db.commit()
    cursor.close()
    db.close()

async def get_inv_data(user):
    db = Mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, database=DB_NAME)
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM inventory WHERE userID = {user.id}")
    users = cursor.fetchone()
    cursor.close()
    db.close()
    return users

async def update_inv(user, amount: int, mode):
    db = Mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, database=DB_NAME)
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM inventory WHERE userID = {user.id}")
    data = cursor.fetchone()
    if data is not None:
        cursor.execute(f"UPDATE inventory SET {mode} = {mode} + {amount} WHERE userID = {user.id}")
        db.commit()
    cursor.execute(f"SELECT `{mode}` FROM inventory WHERE userID = {user.id}")
    users = cursor.fetchone()
    cursor.close()
    db.close()
    return users

async def add_inventory(user,item,amount):
    db = Mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, database=DB_NAME)
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM inventory WHERE userID = {user.id}")
    data = cursor.fetchone()
    if data is not None:
        cursor.execute(f"UPDATE inventory SET {item} = {item} + {amount} WHERE userID = {user.id}")
        db.commit()
    cursor.execute(f"SELECT {item} FROM inventory WHERE userID = {user.id}")
    finalData = cursor.fetchone()
    cursor.close()
    db.close()
    return finalData


class Economy(commands.Cog, name="Economy"):
    """Economy is ruined irl , so try not to ruin it here as well"""

    COG_EMOJI = "📈"

    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.command(aliases=["bal","wallet"])
    async def balance(self, ctx, user:nextcord.Member = None):
        """Take a look into your current status in terms of , *moneeey*"""
        
        if not user : user = ctx.author 
        await open_inv(user)
        await open_bank(user)
        users = await get_bank_data(user)
        wallet_amt = users[1]
        bank_amt = users[2]
        net_amt = int(wallet_amt + bank_amt)
        em = nextcord.Embed(
                title= f"{user.name}'s Balance",
                timestamp=datetime.datetime.utcnow(),
                description= f"**Wallet**:$ {wallet_amt}\n**Bank**:$ {bank_amt}\n**Net-worth**:$ {net_amt}",
                color=nextcord.Color.from_rgb(236, 41, 36),
            )
        em.set_footer(text="💰")
        await ctx.send(embed=em)


    @commands.guild_only()
    @commands.command(aliases=["with"])
    async def withdraw(self,ctx, *,amount= None):
        """Withdraw some cash from the bank for useage.
        You can't always give cheque to buy from candy store"""
        user = ctx.author
        await open_inv(user)
        await open_bank(user)
        users = await get_bank_data(user)
        bank_amt = users[2]
        if amount.lower() == "all" or amount.lower() == "max":
            await update_bank(user, +1*bank_amt)
            await update_bank(user, -1*bank_amt, "bank")
            await ctx.send(f"{user.mention} you withdrew **{bank_amt}** in your wallet")

        else:
            if type(amount) is str and amount.endswith(('k', 'm', 'b','K','M','B')):
                ty = convert_str_to_number(amount)
                amount = int(ty)
            else:
                amount = int(amount)
            bank = users[2]
            if amount > bank:
                await ctx.send(f"{user.mention} You don't have that enough money!")
                return
            if amount < 0:
                await ctx.send(f"{user.mention} enter a valid amount !")
                return
            await update_bank(user, +1 * amount)
            await update_bank(user, -1 * amount, "bank")
            await ctx.send(f"{user.mention} you withdrew **{amount}** from your **Bank!**")


    @commands.guild_only()
    @commands.command(aliases=["dep"])
    async def deposit(self,ctx, *,amount= None):
        """Deposit cash in to a bank account.
        Its always not the best idea to carry money in fat wallets *eh*"""
        user = ctx.author
        await open_inv(user)
        await open_bank(user)
        users = await get_bank_data(user)
        wallet_amt = users[1]
        if amount.lower() == "all" or amount.lower() == "max":
            await update_bank(user, -1*wallet_amt)
            await update_bank(user, +1*wallet_amt, "bank")
            await ctx.send(f"{user.mention} you deposited **{wallet_amt}**")
        else:
            if type(amount) is str and amount.endswith(('k', 'm', 'b','K', 'M', 'B')):
                ty = convert_str_to_number(amount)
                amount= int(ty)
            else:
                amount = int(amount)
            if amount > wallet_amt:
                await ctx.send(f"{user.mention} You don't have that enough money!")
                return
            if amount < 0:
                await ctx.send(f"{user.mention} try using `withdraw` command if you want to reduce your bank balance!")
                return
            await update_bank(user, -1 * amount)
            await update_bank(user, +1 * amount, "bank")
            await ctx.send(f"{user.mention} you deposited **{amount}** from your **Bank!**")

    @commands.guild_only()
    @commands.command()
    async def shop(self,ctx,item = None):
        """Incase you were living under the rock, shop is a place where you buy *stuff*.... 
        Nope not an shady alleyway *(or is it?)*"""
        user = ctx.author
        await open_inv(user)
        await open_bank(user)
        em = nextcord.Embed(title="Marketplace")
        for itm in OrderedDict(sorted(rshop.items())):
            em.add_field(name=itm.capitalize()+' — $ **'+ str(rshop[itm]['cost'])+'**',value=rshop[itm]['info'],inline= False)
        await ctx.send(embed=em)
    
    @commands.guild_only()
    @commands.command(aliases=["inv"])
    async def inventory(self,ctx,user:nextcord.Member = None):
        """Take a look into the stuff you have.
        Anyway *how do you carry this stuff?*"""
        if not user : user = ctx.author
        await open_inv(user)
        await open_bank(user)
        data = await invdata_dict(user)
        data = OrderedDict(sorted(data.items()))
        keys = [k for k, v in data.items() if v != 0]
        if keys == []:
            await ctx.send("You have NO items in your inventory!")
        else:
            inve = nextcord.Embed(title=f"{user}'s inventory")
            for hj in keys:
                inve.add_field(name=hj.capitalize()+" - "+str(data[hj]), value=rshop[hj]['info'],inline=False)
            await ctx.send(embed=inve)

    @commands.guild_only()
    @commands.command()
    async def buy(self,ctx,item,amount=1):
        """Purchase some item from the shop.
        **NOTE**
        Prices may vary depending on the item , either due to experimental change or balancing things out"""
        user = ctx.author
        await open_inv(user)
        await open_bank(user)
        users = await get_bank_data(user)
        if item in rshop:
            cost = rshop[item]['cost'] * amount
            if amount < 0 or amount == 0:
                await ctx.reply("Pls buy more that 0 , you are not broke *(are you?)*")
            elif cost > users[1]:
                await ctx.reply("You don't have enough money to buy this item'")
            else:
                await update_bank(user,-1*cost)
                await add_inventory(user,item,+1*amount)
                await ctx.reply(f"You bought {item} for `{cost}`")
        else:
            await ctx.reply("It doesn't matter what you want, mostly imaginary")
    @commands.guild_only()
    @commands.command()
    async def sell(self,ctx,item,amount=1):
        """Sell items back in exchage of some cash .
        The return value is less than the original amount.
        Resell rate is decreased by `0.75%` or that of Selling price """
        user = ctx.author
        await open_inv(user)
        await open_bank(user)
        users = await invdata_dict(user)
        print(users)
        if item in rshop:
            cost = round(rshop[item]['cost']*0.75) * amount
            if amount < 0 or amount == 0:
                await ctx.send("Pls sell more that 0 ,*(Have SOME common sense yeh?)*")
            elif amount > users[item]:
                await ctx.send("You don't have **enough items** to sell these many")
            else:
                await update_bank(user,+1*cost)
                await add_inventory(user,item,-1*amount)
                await ctx.send(f"Selling... {item} for `{cost}`")
        else:
            await ctx.send("It doesn't matter what you want, mostly imaginary")
    
    @commands.guild_only()
    @commands.command()
    async def beg(self,ctx):
        """Beg from some people to get money.
        So, you have taken desperate measures I see.
        *Wait, you can get up to $1000?*"""
        user = ctx.author
        await open_inv(user)
        await open_bank(user)
        Names=['Abraham Lincoln ','Bill Gates','J.K.Rowling','Hitler','Big Chungus','Charles Dickens','Einstine','Cristiano','Lady Gaga','Tony Stark','Captain America','Thanos','"The Rock"','Jackie Chan','The person who You slept with yesterday']
        Responses=['We worked for living','Money doent grow on trees','Go Away!!','Shall i call the Police ?','I wish there were two of me','I have work to do jobless','NOOOOOO!!','That’s such a funny joke! HAHAHAHA!','I’m busy, scram!','I wasn’t born for this.',]
        winRate = random.choice(("win","loss"))
        if winRate == "win":
            winAmt=random.randint(10,1000)
            await update_bank(user,+1*winAmt)
            await ctx.send(f"You have won {winAmt}")
        else: 
            await ctx.send(f"{random.choice(Names)}\n'{random.choice(Responses)}'")



    """
    
    
    Use the items from your backpack
    
    
    """


    @commands.group()
    async def use(self, ctx):
        """Use your Items from your inventory"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help("use")

    @use.command()
    async def laptop(self, ctx):
        """Use laptop"""
        await ctx.send("Using laptop...")
        






    @commands.guild_only()
    @commands.command()
    async def gamble(self, ctx, amount):
        """Visit a Casino and gamble off some *moneeey*.
        All the rolls are 100% random and there are no weights from win or lose.
        Try not to get addicted to it"""

        user = ctx.author
        await open_inv(user)
        await open_bank(user)
        data = await get_bank_data(user)

        min_amount = 200
        max_amount = 100000
        cash_in_wallet = data[1]
        botroll = random.randint(1,6)
        userroll = random.randint(1,6)
        amount = int(amount)


        if amount is None:
            await ctx.reply("Enter how much you are willing to bet,*smh*")
        elif amount == 0 or amount < min_amount:
            await ctx.reply(f"Minimun amount to gamble is `{min_amount}`")
        elif amount > max_amount:
            await ctx.reply(f"Maximum amount to gamble is capped to `{max_amount}`")
        else:
            if amount > cash_in_wallet:
                await ctx.reply("You don't have enough cash in your wallet !")
            else:
                if botroll < userroll:
                    await update_bank(user,+1* amount)
                    e = nextcord.Embed(
                        title=f' Gamble - **YOU WON** `{amount}`',
                        color= nextcord.Color.green(),
                        timestamp=datetime.datetime.utcnow()
                    )
                    e.add_field(name='Bot Rolled', value=botroll,inline=False)
                    e.add_field(name='**You Rolled**', value=userroll,inline=False)
                    await ctx.send(embed=e)
                elif botroll > userroll:
                    e = nextcord.Embed(
                        title=f' Gamble - **YOU LOST** `{amount}`',
                        color= nextcord.Color.from_rgb(236, 41, 36),
                        timestamp=datetime.datetime.utcnow()
                    )
                    e.add_field(name='**Bot Rolled**', value=botroll,inline=False)
                    e.add_field(name='You Rolled', value=userroll,inline=False)
                    await ctx.send(embed=e)



    @commands.is_owner()
    @commands.command(hidden=True)
    async def uInv(self,ctx):
        db = Mysql.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWD, database=DB_NAME)
        cursor = db.cursor()
        list2 = []
        cursor.execute(f"DESC inventory;")
        data = cursor.fetchall()
        for i in range(1, len(data)):
            ndata = data[i][0]
            list2.append(ndata)
            print(list2)
            # await asyncio.sleep(10)
        for x in rshop:
            if x not in list2:
                print(x)
                newItem=f"ALTER TABLE inventory ADD {x} INT NULL DEFAULT (0)"
        cursor.execute(newItem)
        await ctx.send(f"Added {x}")
        # await cursor.execute(f"UPDATE inventory SET {x}=0")


def setup(bot):
    bot.add_cog(Economy(bot))
