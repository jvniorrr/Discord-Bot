import discord
# from shopify import AccountCreator, Address, BotBroker
# from market import GOAT, StockX
from src import market
import random, datetime, time, logging
from discord.ext import commands
import asyncio
import os

prefixes = ['.', '!']
prefixes = '.'
client = commands.Bot(command_prefix=prefixes)


# EVENTS
@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game(name='Monitoring Server'))
    print(f'{client.user} bot is now online.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await client.process_commands(message)



# COMMANDS
@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")

@client.command(aliases=['sx', 'stock'])
async def stockx(ctx, *search):
    # fix this, would be wise to store all this in a class, and creating a function for it. 
    userImage = ctx.author.avatar_url
    x = datetime.datetime.now()
    month = x.strftime("%m")
    day = x.strftime("%d")
    year = x.strftime("%Y")
    footerDate = f"{month}-{day}-{year}"
    user = f"Requested by {str(ctx.author)} • {footerDate}"
    keywords = ' '.join(search)
    embed = discord.Embed(color=0x09A05E, title=f'Searching for {keywords.title()}')
    authURL = 'https://media.discordapp.net/attachments/661223352115003402/730649326338048000/stockX.png'
    embed.set_author(name='StockX', url='https://www.stockx.com', icon_url=authURL)
    msg = await ctx.channel.send(embed=embed)

    newEmbed = market.StockX(keyword=keywords).main()
    # print(newEmbed)
    # if newEmbed['description']:
    if newEmbed['color'] == 13893632:
        newEmbed['description'] = f"{prefixes}Stockx zebra yeezy\n{prefixes}Stockx CP9654\n{prefixes}Stockx box logo\n"
        newEmbed = discord.Embed.from_dict(newEmbed)
    else:
        newEmbed = discord.Embed.from_dict(newEmbed)
        newEmbed.set_footer(text=user, icon_url=userImage)


    await msg.edit(embed=newEmbed)

@client.command()
async def goat(ctx, *search):
    keywords = ' '.join(search)

    userImage = ctx.author.avatar_url
    x = datetime.datetime.now()
    month = x.strftime("%m")
    day = x.strftime("%d")
    year = x.strftime("%Y")
    footerDate = f"{month}-{day}-{year}"
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
        else:
            newEmbed = discord.Embed.from_dict(newEmbed)
            newEmbed.set_footer(text=user, icon_url=userImage)

        # print(newEmbed.fields[5])
        await msg.edit(embed=newEmbed)
    else:
        await msg.edit('Beep Bop. Error within bot. Try again in a few.')

client.run('NzI0MDMzODM3MjY4NTk4ODM1.Xu6unw.T9JJFxn1YIDt9Qfgy86sgLdYVIc')
