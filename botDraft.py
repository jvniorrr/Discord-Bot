import discord
from src.shopifyImports import *
from src.faking import *
from discord import ActivityType, Activity
# from shopify import AccountCreator, Address, BotBroker
# from market import GOAT, StockX
from src import market
from src.botbroker import BotBroker
import random, datetime, time, logging
from pytz import timezone
from discord.ext import commands
import asyncio
import os

global failEmbedColor
failEmbedColor = 0xd40000

global logging
logging.basicConfig(format='%(asctime)s[%(levelname)s] - %(message)s', level=logging.INFO, datefmt='[%I:%M:%S %p %Z]')
 
global est
est = timezone('America/New_York')

prefixes = ['.', '!']
prefixes = '.'
client = commands.Bot(command_prefix=prefixes)
client.remove_command('help')

# EVENTS
@client.event
async def on_ready():
    # await client.change_presence(activity = discord.Game(name='Monitoring Server'))
    # actType = discord.ActivityType().watching
    await client.change_presence(activity= Activity(
        name="Users & Awaiting commands",
        type=ActivityType.watching
        ))
    logging.info(f'\n{str(client.user).upper()} bot is now online!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await client.process_commands(message)



# COMMANDS
@client.command()
async def help(ctx):
    logging.info(f'"help" Command Called by {ctx.author}.')
    user = ctx.author
    title = f"The prefix for {ctx.guild} is `{prefixes}`"
    embed = discord.Embed(color=0x4EA3F1,title=title)
    embed.set_author(name='Help')
    embed.add_field(name='__stockx__', value='Searches StockX for query provided by user (Searches collectibles, streetwear, and sneakers)', inline=False)
    embed.add_field(name='__goat__', value='Searches Goat for query provided by user (Searches sneakers)', inline=False)
    bbMSG = f'''CyberAIO: "Cyba", "Cyber", "CyberAIO", "Cyber AIO"\nPrismAIO: "Prism", "PrismAIO", "Prism AIO"\nBalko:"Balko","Balko AIO", "BalkoAIO\nPhantom:"Phantom", "Phantom AIO", "PhantomAIO"\nDashe:"Dashe","Dashe AIO", "DasheAIO"
Splashforce:"Splash", "Splashforce", "SF", "Splash Force"\nProject Destroyer: "PD", "Project Destroyer", "ProjectDestroyer"\nWrath:"Wrath", "WrathAIO", "Wrath AIO"\nMekPreme:"Mek", "MekPreme", "Mek Preme"\nAdept:"Adept", "AdeptPreme", "Adept Preme"\nVelox:"Velox", "Vox"
ScottBot:"Scottbot", "Scottbt", "Scott bot"\nSwftAIO:"Swift", "SwiftAIO", "Swift"\nTohru:"Tohru", "Tohru AIO", "TohruAIO"\nGhost:"Ghost", "GhostSNKRS"\nSneakercopter:"SC", "Sneakercopter",\nHastey:"Hastey", "Hasty"\nSoleAIO:"SoleAIO", "Sole"'''
    embed.add_field(name='__botbroker__', value=f'Searches botbroker for a bot and returns its info\n**Valid search parameters:**```{bbMSG}```\n__Example__`.botbroker cyber aio`', inline=False)
    embed.add_field(name='__accounts__', value=f'Attempts to create an account on a shopify based site (Max of 25), 80% ish success rate currently:\n__Example__: `{prefixes}accounts undefeated.com catchall.com 5` **or** `{prefixes}accounts undefeated.com myemail@gmail.com 5`', inline=False)
    embed.add_field(name='__address__', value='Creates j¡gged properties (Max of 30) for you to avoid cancellations (4 Character j¡g)\n__Example__: `.address`', inline=False)
    embed.add_field(name='__dottrick__', value='Creates j¡gged emails (50) using Googles dot trick for you to avoid cancellations.\n__Example__`.dot example@gmail.com`', inline=False)

    await user.send(embed=embed)
    await ctx.channel.send(f'{ctx.author.mention} Check your DM for information on the Help Command.')
    logging.info('"help" Command was successfully called with no erorrs.')
    
# @client.command()
# async def kick(ctx, member: discord.Member, *, reason=None):
#     logging.info(f'"kick" Command called by {ctx.author}')
#     if member != client.user:
#         await member.send(content=f'You are being kicked from {str(ctx.guild)} for reason: {reason}')
#         await member.kick(reason=reason)
#         await ctx.message.delete(delay=5)
#         await ctx.channel.send(f"User {member} has been kicked for: {reason}", delete_after=60.0)
#         logging.info(f"{member} was kicked by {ctx.author} for reason: {reason}")
#     else:
#         await ctx.channel('Are you a clown :clown:. Why are you trying to kick me.')
# @kick.error
# async def kick_error(ctx, error):
#     if isinstance(error, commands.MissingRequiredArgument):
#         await ctx.send("Member is a required argument that is missing.")
#     elif isinstance(error, commands.errors.CommandInvokeError):
#         await ctx.send("That member isnt in this guild. Provide a member in this channel.")
#     elif isinstance(error, commands.errors.BadArgument):
#         await ctx.send(f"Member not found.")

@client.command(aliases=["avi"])
async def avatar(ctx, member: discord.Member):
    x = datetime.datetime.now(est).strftime("%I:%M:%S %p")
    # footerDate = f"{x.strftime('%m')}-{x.strftime('%d')}-{x.strftime('%Y')}"
    show_Avi =  discord.Embed(color=0x4EA3F1)
    show_Avi.set_image(url='{}'.format(member.avatar_url))
    show_Avi.set_footer(text=f"Requested by {ctx.author} • {x}", icon_url=f"{ctx.author.avatar_url}")

    await ctx.send(embed=show_Avi)
@avatar.error
async def avatar_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Member is a required argument that is missing.\n__Example__: `.avatar @user#1234`")
    elif isinstance(error, commands.errors.CommandInvokeError):
        await ctx.send("That member isnt in this guild. Provide a member in this channel.")
    elif isinstance(error, commands.errors.BadArgument):
        await ctx.send(f"Member not found.")

@client.command()
async def ping(ctx):
    logging.info(f'"ping" Command Called by {ctx.author}.')
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")

@client.command()
async def fees(ctx, fee):
    x = datetime.datetime.now(est).strftime("%I:%M:%S %p")
    fee = int(fee)
    # if fee != int:
    #     await ctx.channel.send(f'please provide an integer value to use the fee command')
    # else:
    c = Fees(fee).main()
    if c != None:
        embed = discord.Embed.from_dict(c)
        embed.set_footer(text=f"Requested by {ctx.author} • {x}", icon_url=f"{ctx.author.avatar_url}")
        await ctx.channel.send(embed=embed)
    else:
        await ctx.channel.send('Please send an integer value')
    

@client.command(aliases=['sx', 'stock'])
async def stockx(ctx, *search):
    logging.info(f'"stockx" Command Called by {ctx.author}.')
    # fix this, would be wise to store all this in a class, and creating a function for it. 
    userImage = ctx.author.avatar_url
    x = datetime.datetime.now(est)
    footerDate = x.strftime("%I:%M:%S %p")
    # day = x.strftime("%d")
    # year = x.strftime("%Y")
    # footerDate = f"{month}-{day}-{year}"
    user = f"Requested by {str(ctx.author)} • {footerDate}"
    keywords = ' '.join(search)
    embed = discord.Embed(color=0x09A05E, title=f'Searching for {keywords.title()}')
    authURL = 'https://media.discordapp.net/attachments/661223352115003402/730649326338048000/stockX.png'
    embed.set_author(name='StockX', url='https://www.stockx.com', icon_url=authURL)
    msg = await ctx.channel.send(embed=embed)
    try:
        newEmbed = market.StockX(keyword=keywords).main()
        # print(newEmbed)
        # if newEmbed['description']:
        if newEmbed['color'] == 13893632:
            newEmbed['description'] = f"{prefixes}Stockx zebra yeezy\n{prefixes}Stockx CP9654\n{prefixes}Stockx box logo\n"
            newEmbed = discord.Embed.from_dict(newEmbed)
            logging.info(f'"stockx" Command returned an EMPTY embed called by {ctx.author}: No results found for query search')
        else:
            newEmbed = discord.Embed.from_dict(newEmbed)
            newEmbed.set_footer(text=user, icon_url=userImage)
            logging.info(f'"stockx" Command successfully returned an embed when called by {ctx.author}')



        await msg.edit(embed=newEmbed)
        # logging.info('"stockx" Command was successfully called with no erorrs')
    except Exception:
        await msg.edit('Beep Bop. Error within bot. Try again in a few or contact the dev.')
        logging.error(f'"stockx" Command had an error returning an Embed to {ctx.author}')

@client.command()
async def goat(ctx, *search):
    logging.info(f'"goat" Command Called by {ctx.author}.')
    keywords = ' '.join(search)

    userImage = ctx.author.avatar_url
    footerDate = datetime.datetime.now(est).strftime("%I:%M:%S %p")
    # month = x.strftime("%m")
    # day = x.strftime("%d")
    # year = x.strftime("%Y")
    # footerDate = f"{month}-{day}-{year}"
    user = f"Requested by {str(ctx.author)} • {footerDate}"

    embed = discord.Embed(color=0x2F3136, title=f'Searching for {keywords.title()}')
    authUrl = 'https://cdn.discordapp.com/attachments/661223352115003402/731014001885970502/goat.png'

    embed.set_author(name='GOAT', url='https://www.goat.com', icon_url=authUrl)
    msg = await ctx.channel.send(embed=embed)

    newEmbed = market.GOAT(keyword=keywords).main()
    # print(newEmbed)
    if newEmbed != None:
        if newEmbed['color'] == 13893632:
            newEmbed['description'] = f"{prefixes}goat zebra yeezy\n{prefixes}goat CP9654\n{prefixes}goat jordan 1\n"
            newEmbed = discord.Embed.from_dict(newEmbed)
            logging.info(f'"goat" Command returned an EMPTY embed called by {ctx.author}: No results found for query search')
        else:
            newEmbed = discord.Embed.from_dict(newEmbed)
            newEmbed.set_footer(text=user, icon_url=userImage)
            logging.info(f'"goat" Command successfully returned an embed when called by {ctx.author}')


        # print(newEmbed.fields[5])
        await msg.edit(embed=newEmbed)
        # logging.info('"goat" Command was successfully called with no erorrs')

    else:
        await msg.edit('Beep Bop. Error within bot. Try again in a few.')
        logging.error(f'"goat" Command had an issue returning a valid embed to {ctx.author}')


@client.command(aliases=['bb', 'BotBroker', 'Botbroker'])
async def botbroker(ctx, *args):
    logging.info(f'"botbroker" command invoked by {ctx.author}')
    if len(args) != 0:
        userInput = ' '.join(args)
        bbImage = 'https://botbroker.io/favicon-96x96.png'
        embed = discord.Embed( color=0xFF2440, url='https://botbroker.io', description=f'Searching BotBroker for {userInput.title()}...')
        embed.set_author(name='Bot Broker', icon_url=bbImage, url='https://botbroker.io')
        searchMsg = await ctx.channel.send(embed=embed)

        bot = BotBroker(userInput).main()
        # est = timezone('America/New_York')
        # x = datetime.datetime.now(est).strftime("%m-%d-%y | %I:%M:%S %p")
        # x = datetime.datetime.now(est)
        # month = x.strftime("%m")
        # day = x.strftime("%d")
        # year = x.strftime("%Y")
        # footerDate = f"{month}-{day}-{year}"
        # est = timezone('EST')

        # now = datetime.datetime.now()
        # hour = now.strftime("%H")
        # mint = now.strftime("%M")
        # sec = now.strftime("%S")
        # if int(str(now.strftime('%H'))) >= 13:
        #     hour = (int(now.strftime("%H")) - 12)
        #     current_time = f"0{str(hour)}:{mint}:{sec} PM"
        # else:
        #     current_time = f"{hour}:{mint}:{sec} AM"

        current_time = datetime.datetime.now(est).strftime("%I:%M:%S %p")
        newEmbed = discord.Embed.from_dict(bot)
        newEmbed.set_footer(text=f'Requested by {ctx.author} • {current_time}', icon_url=bbImage)

        await searchMsg.edit(embed=newEmbed)
        logging.info('Sent bot info to bot / user')
        logging.info('"botbroker" Command was successfully called with no erorrs')
    else:
        await ctx.channel.send('Please provide a valid query to search for on BotBroker :mag:')
        logging.info(f'"botbroker" Command was not provided valid arguments by {ctx.author}')



@client.command(name="accounts", aliases=["shopAccounts", "Accounts"])
async def accounts(ctx, site, email, total):
    logging.info(f'"accounts" Command Called by {ctx.author}.')
    await ctx.message.delete(delay=2)
    total = int(total)
    # if total != int or total == 0:
    #     await ctx.channel.send(f'Please provide a valid integer value greater than 1 for the last argument {ctx.author.mention}')
    #     # logging.info(f'{ctx.author} did not provide valid arguments for the "accounts" command.')
    #     logging.warning(f'"accounts" Command had an error when called by {ctx.author}: Invalid argument type for total value')


    if (len(email) > 1) and (len(site) > 1):
        initMsg = await ctx.channel.send(f"{ctx.author.mention} Initialized Shopify Acc Creator.")
        logging.info(f'"accounts" Command initialized by {ctx.author}.')
        await initMsg.delete(delay=2)
        newPath = AccountCreator(str(site), str(email), int(total)).make_account()
        if newPath == 'None':
            await ctx.channel.send('There seems to have been an issue checking if the site was Shopify based or not. Retry in a few minutes.')
            logging.error('"accounts" Command had an issue checking if the site provided was shopify based or not.')
        elif newPath == 'False':
            await ctx.channel.send('The site you requested does not seem to be Shopify based. Please try with a valid Shopify based website.')
            logging.info('"accounts" Command was not provided with a valid Shopify website')
        elif newPath != None:
            await ctx.channel.send(f"{ctx.author.mention} Check your DM! :stuck_out_tongue_winking_eye:")
            await ctx.author.send("Here are your Accounts :stuck_out_tongue_closed_eyes:",file=discord.File(newPath))
            logging.info('Sent accounts successfully!')
            os.remove(newPath)
            logging.info('Removed File from dir')
            logging.info('"accounts" Command was successfully called with no erorrs.')
        else:
            await ctx.channel.send(f"Oh no, there was an issue creating the accounts. Try again in a bit or contact the dev.")
            logging.error(f'"accounts" Command had an error returning Shopify accounts to {ctx.author}')
        # await client.delete_message(ctx)
    else:
        logging.error(f'"accounts" command had an error when called by {ctx.author}: Invalid required arguments')
        await ctx.channel.send(f"Please provide proper arguements\nExample: `{prefixes}accounts undefeated.com jvnior.com 5`")
@accounts.error
async def accounts_error(ctx, error):
    await ctx.message.delete()
    if isinstance(error, commands.MissingRequiredArgument):
        # logging.info(f'"accounts" command was not provided valid arguments by {ctx.author}')
        await ctx.send(f"Please provide proper arguements.\n__Example__: `{prefixes}accounts undefeated.com catchall.com 5`")
        logging.error(f'"accounts" Command had an error when called by {ctx.author}: Missing required arguments')

@client.command()
async def address(ctx):
    logging.info(f'"address" Command invoked by {ctx.author}')
    await ctx.send("What is your address?", delete_after=20.0)
    channel = ctx.channel
    cUser = ctx.author
    # msg = ' '.join(message)
    def check(user):
        if user.author == ctx.author:
            return True
        else:
            return False

    try:
        add = await client.wait_for('message', timeout=20.0, check=check)
        address = add.content
        await add.delete(delay=0.5)
        # await channel.purge(limit=3, check=check)
        await ctx.send("How many would you like? (Provide a valid integer value between 0 - 30)", delete_after=19.0)
        total = await client.wait_for('message', timeout=20.0, check=check)
        await total.delete(delay=4)
        # await channel.purge(limit=3, check=check)
        total = int(total.content)
        if total:
            returned = Address(address, total).main()
            await ctx.channel.send(f"{ctx.author.mention} Check your DM! :stuck_out_tongue_winking_eye:")
            await ctx.author.send("Here's your file. :stuck_out_tongue_closed_eyes:",file=discord.File(returned))
            logging.info('Sent accounts successfully!')
            os.remove(returned)
            logging.info('Removed File from dir')
            logging.info('"address" Command was successfully called with no erorrs.')

    except asyncio.TimeoutError:
        await channel.send('👎')
        logging.info(f'"address" Command had an error when called by {ctx.author}: User did not respond in time.')

    else:
        pass
@address.error
async def address_error(ctx, error):
    if isinstance(error, commands.errors.CommandInvokeError):
        # logging.warning(f'"accounts" command had an error when called by {ctx.author}')
        await ctx.channel.send('Provide valid arguments and retry.')
        logging.error(f'"address" Command had an error when called by {ctx.author}: Command invoking error, likely invalid arguments')

@client.command(aliases=["dottrick"])
async def dot(ctx, email):
    logging.info(f'"dotTrick" Command invoked by {ctx.author}')
    if email != None and len(email) > 2:
        await ctx.message.delete(delay=0.5)
        info = gmailDot().dot_trick(email)
        await ctx.author.send("Here you go",file=discord.File(info))
        logging.info('Sent accounts successfully!')
        await ctx.channel.send(f"{ctx.author.mention} Check your DM! :stuck_out_tongue_winking_eye:")
        os.remove(info)
        logging.info('Removed File from dir')
        logging.info('"dotTrick" Command was successfully called with no erorrs.')
    else:
        await ctx.channel.send('Please provide a valid email to fake.')
        logging.info(f'"dotTrick" Command had an error when called by {ctx.author}: Seems to be an invalid email.')

@dot.error
async def dot_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        logging.error(f'"dotTrick" Command had an error when called by {ctx.author}: Missing required arguments')
        await ctx.channel.send("Email is a required argument that is missing. Please provide a valid gmail to be j¡gged.")


client.run('NzI0MDMzODM3MjY4NTk4ODM1.Xu6unw.T9JJFxn1YIDt9Qfgy86sgLdYVIc')
