import logging
import datetime, string, json, io, sys, random, os
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
# from dhooks import Embed, Webhook, File
import discord
import lxml.html


class BotBroker:
    """Instance which returns the latest info on a particular Sneaker bot, based on user choice as long as its in th nicknames"""
    def __init__(self, bot):
        self.bot = bot.lower()
        logging.basicConfig(format='%(asctime)s[%(levelname)s] - %(message)s', level=logging.INFO, datefmt='[%I:%M:%S %p %Z]')

    def set_embed(self, info):
        bbImage = 'https://botbroker.io/favicon-96x96.png'
        
        if info == None:
            embed = discord.Embed(color=0xFF2440, url='https://botbroker.io', description=f'No products found. Please refine your search keywords')
            embed.set_thumbnail(url=bbImage)
            embed.set_author(name='Bot Broker', icon_url=bbImage, url='https://botbroker.io')
            # embed.to_dict()
        elif info != None:
            botName = info['name']
            botImage = info['image']
            if 'cyber' in botName.lower():
                color = '5EF783' 
            elif 'polaris' in botName.lower():
                color = 'CFAAF3' 
            elif 'balko' in botName.lower():
                color = '252B37' 
            elif 'phantom' in botName.lower():
                color = '2F252D' 
            elif 'dashe' in botName.lower():
                color = '5182D2' 
            elif 'splashforce' in botName.lower():
                color = '0B0B0B' 
            elif 'destroy' in botName.lower():
                color = '9B54A0' 
            elif 'prism' in botName.lower():
                color = '9A68E9' 
            elif 'wrath' in botName.lower():
                color = '13598B' 
            elif 'mek' in botName.lower():
                color = 'DD3033' 
            elif 'adept' in botName.lower():
                color = 'E8CBFC' 
            elif 'velox' in botName.lower():
                color = '1E5194' 
            elif 'scott' in botName.lower():
                color = 'F28FB3' 
            elif 'swft' in botName.lower():
                color = 'FF5C5C' 
            elif 'tohru' in botName.lower():
                color = 'DB4F58'
            elif 'ghost' in botName.lower():
                color = 'F58D8E' 
            elif 'copter' in botName.lower():
                color = 'EAEAEA' 
            elif 'hastey' in botName.lower():
                color = '262628' 
            elif 'sole' in botName.lower():
                color = '6F056B'
            else:
                color = 'FF2440'

            color = int(f'0x{color}', 16)
            if info['available']:
                botBBlink = info['BBlink']
                botlink = info['botlink']
                botRetail = info['retail']

                # supported sites by the bot
                sites = info['sites']
                sitesValue = ''
                for site in sites:
                    if site.lower() != 'mek':
                        msg = f"{site.title()}\n"
                        sitesValue += msg
                
                compabilitySites = info['compatibility']
                compValue = ''
                for site in compabilitySites:
                    if site.lower() == 'mobile':
                        msg = f":mobile: {site.title()}\n"
                        compValue += msg
                    elif site.lower() == 'windows':
                        msg = f":desktop: {site.title()}\n"
                        compValue += msg
                    elif site.lower() == 'mac':
                        msg = f":computer: {site.title()}\n"
                        compValue += msg
                    else:
                        msg = f":question: {site.title()}\n"
                        compValue += msg

                # handle every recent sale, should be 3 total
                # if len(bot['recentsales']) != 0:
                try:
                    recentSaleVal = ''
                    for sale in info['recentsales']:
                        msg = f"**Type:** {sale['type']}\n**Price:** {sale['saleprice']}\n**Timestamp:** {sale['date']}\n\n"
                        recentSaleVal += msg
                except Exception:
                    pass

                # handle the ask and bid prices
                asks = info['asks']
                askPrices = ''
                for ask in asks:
                    msg = f'${str(ask)}\n'
                    askPrices += msg

                bids = info['bids']
                bidPrices = ''
                for bid in bids:
                    msg = f'${str(bid)}\n'
                    bidPrices += msg

                # more info section
                infoVal = f'{botlink}\nRetail: `{botRetail}`'

                embed = discord.Embed(title=botName, color=color, url=botBBlink)
                embed.set_thumbnail(url=botImage)
                embed.set_author(name='Bot Broker', icon_url=bbImage, url='https://botbroker.io')
                if askPrices != '':
                    embed.add_field(name='__**Ask Prices**__', value=askPrices)
                if bidPrices != '':
                    embed.add_field(name='__**Bid Prices**__', value=bidPrices)
                if recentSaleVal:
                    if len(recentSaleVal) > 2:
                        embed.add_field(name='__**Recent Sales**__', value=recentSaleVal,inline=False)
                embed.add_field(name='\u200B', value='\u200B',inline=False)
                embed.add_field(name='__**Sites Supported**__', value=sitesValue,inline=True)
                embed.add_field(name='__**Compatbility**__', value=compValue,inline=True)
                embed.add_field(name='__**More Info**__', value=infoVal, inline=True)

        elif info['available'] == False:
            des = f'{botName} is currently under maintenance on the botbroker site.'
            embed = discord.Embed(title=botName, color=color, description=des)
            embed.set_author(name='Bot Broker', icon_url=bbImage, url='https://botbroker.io')
            embed.set_thumbnail(url=botImage)

        embed = embed.to_dict()
        return embed

                

    # - GET THE BOT PAGE FROM BB, AND RETURN PRODUCTS THAT ARE AVAILABLE / UNAVAILABLE
    def getPage(self):
        """Function that just goes to bot broker.io/bots link and returns html of it"""
        try:
            url = "https://botbroker.io/bots"
            headers = Headers(browser="chrome", os="mac").generate()
            html = requests.get(url,headers=headers).text
            return html
        except Exception as e:
            html = None
            logging.error('Fatal error getting products page.')

        return html

    def products(self):
        """Grabs all the products available on the bots link, if its unavailable or available"""
        doc = self.getPage()
        soup = BeautifulSoup(doc, "lxml")
        allsPill = soup.find('div', {'id':'pills-all'})
        allBots = []

        # grab all the available bots
        try:
            allRow = allsPill.find_all('div',{'class':'col-md-4 mt-3'})
            for row in allRow:
                bots = row.div.div.a
                bot = dict()
                bot['name'] = bots.img['alt']
                bot['link'] = f"https://botbroker.io{bots['href']}"
                bot['image'] = bots.img['src']
                bot['available'] = True
                if 'cyber' in bot['name'].lower():
                    bot['nicknames'] = ['cyba', 'cyber', 'cyberaio', 'cyber aio']
                elif 'polaris' in bot['name'].lower():
                    bot['nicknames'] = ['polaris', 'polar', 'polaris aio', 'polarisaio']
                elif 'prism' in bot['name'].lower():
                    bot['nicknames'] = ['prism', 'prismaio', 'prism AIO', 'pris']
                elif 'balko' in bot['name'].lower():
                    bot['nicknames'] = ['balko', 'balko aio', 'barco', 'balkoaio']
                elif 'phantom' in bot['name'].lower():
                    bot['nicknames'] = ['phantom', 'phantom aio', 'phantomaio']
                elif 'dashe' in bot['name'].lower():
                    bot['nicknames'] = ['dashe', 'dashe aio', 'dasheaio']
                elif 'splashforce' in bot['name'].lower():
                    bot['nicknames'] = ['splash', 'Splashforce', 'sf']
                elif 'destroyer' in bot['name'].lower():
                    bot['nicknames'] = ['pd', 'project destroyer', 'projectdestroyer']
                elif 'wrath' in bot['name'].lower():
                    bot['nicknames'] = ['wrath', 'wrath aio', 'wrathaio']
                elif 'mekpreme' in bot['name'].lower():
                    bot['nicknames'] = ['mek', 'mekpreme', 'mek preme']
                elif 'adept' in bot['name'].lower():
                    bot['nicknames'] = ['adept', 'adeptpreme', 'adept preme']
                elif 'velox' in bot['name'].lower():
                    bot['nicknames'] = ['velox', 'vox']
                elif 'scottbot' in bot['name'].lower():
                    bot['nicknames'] = ['scottbot', 'scottbt','scott bot', 'sb']
                elif 'swft' in bot['name'].lower():
                    bot['nicknames'] = ['swftAIO', 'swft','swift']
                elif 'tohru' in bot['name'].lower():
                    bot['nicknames'] = ['tohru', 'tohruaio','tohru aio']
                elif 'ghost' in bot['name'].lower():
                    bot['nicknames'] = ['ghost', 'ghostsnkrs']
                elif 'sneakercopter' in bot['name'].lower():
                    bot['nicknames'] = ['sc', 'sneakercopter']
                elif 'hastey' in bot['name'].lower():
                    bot['nicknames'] = ['hastey', 'hasty']
                elif 'sole' in bot['name'].lower():
                    bot['nicknames'] = ['sole', 'soleaio', 'sole aio', 'sold']
                else:
                    bot['nicknames'] = None
                
                # add the sites supported
                sitesSupport = row.div.find_all('span')
                sites = []
                for site in sitesSupport:
                    sites.append(site.text)
                bot['sites'] = sites
                allBots.append(bot)
        except Exception as e:
            logging.error(f'Fatal Error grabbing all products available: fxn product 1\n{e}')

        try: 
            allsPill = soup.find('div', {'id':'pills-all'})
            # grab all the unavailable bots
            allRows = allsPill.find_all('div', {'class':'col-md-4 mt-3 bot-card-disabled'})
            for row in allRows:
                bots = row.div.div.a
                bot = dict()
                bot['name'] = bots.img['alt']
                bot['link'] = f"https://botbroker.io{bots['href']}"
                bot['image'] = bots.img['src']
                bot['available'] = False
                if 'cyber' in bot['name'].lower():
                    bot['nicknames'] = ['cyba', 'cyber', 'cyberaio', 'cyber aio']
                elif 'polaris' in bot['name'].lower():
                    bot['nicknames'] = ['polaris', 'polar', 'polaris aio', 'polarisaio']
                elif 'prism' in bot['name'].lower():
                    bot['nicknames'] = ['prism', 'prismaio', 'prism AIO', 'pris']
                elif 'balko' in bot['name'].lower():
                    bot['nicknames'] = ['balko', 'balko aio', 'barco', 'balkoaio']
                elif 'phantom' in bot['name'].lower():
                    bot['nicknames'] = ['phantom', 'phantom aio', 'phantomaio']
                elif 'dashe' in bot['name'].lower():
                    bot['nicknames'] = ['dashe', 'dashe aio', 'dasheaio']
                elif 'splashforce' in bot['name'].lower():
                    bot['nicknames'] = ['splash', 'Splashforce', 'sf']
                elif 'destroyer' in bot['name'].lower():
                    bot['nicknames'] = ['pd', 'project destroyer', 'projectdestroyer']
                elif 'wrath' in bot['name'].lower():
                    bot['nicknames'] = ['wrath', 'wrath aio', 'wrathaio']
                elif 'mekpreme' in bot['name'].lower():
                    bot['nicknames'] = ['mek', 'mekpreme', 'mek preme']
                elif 'adept' in bot['name'].lower():
                    bot['nicknames'] = ['adept', 'adeptpreme', 'adept preme']
                elif 'velox' in bot['name'].lower():
                    bot['nicknames'] = ['velox', 'vox']
                elif 'scottbot' in bot['name'].lower():
                    bot['nicknames'] = ['scottbot', 'scottbt','scott bot']
                elif 'swft' in bot['name'].lower():
                    bot['nicknames'] = ['swftAIO', 'swft','swift']
                elif 'tohru' in bot['name'].lower():
                    bot['nicknames'] = ['tohru', 'tohruaio','tohru aio']
                elif 'ghost' in bot['name'].lower():
                    bot['nicknames'] = ['ghost', 'ghostsnkrs']
                elif 'sneakercopter' in bot['name'].lower():
                    bot['nicknames'] = ['sc', 'sneakercopter']
                elif 'hastey' in bot['name'].lower():
                    bot['nicknames'] = ['hastey', 'hasty']
                elif 'sole' in bot['name'].lower():
                    bot['nicknames'] = ['sole', 'soleaio', 'sole aio', 'sold']
                else:
                    bot['nicknames'] = None

                # add the sites supported
                sitesSupport = row.div.find_all('span')
                sites = []
                for site in sitesSupport:
                    sites.append(site.text)
                bot['sites'] = sites
                allBots.append(bot)
                
        except Exception as e:
            logging.error(f'Fatal Error grabbing all products available: fxn product 2')

        return allBots

    # - HANDLE THE USER INPUT (THIS IS ASSOCIATED WITH NICKNAMES I'VE PUT) AND RETURN THE PROPER BOT TO SEARCH THROUGH DETAILS
    def get_bot(self, userInput):
        """Handles the user input and checks if that users input is stored in one of the bots names
        Parameters
        -----------
        - userInput: the bot the the user is requesting."""
        bots = self.products()
        if bots:
            for bot in bots:
                name = bot['name']
                nicknames = bot['nicknames']
                availability = bot['available']
                if userInput.lower() in nicknames:
                    botReturn = dict()
                    botReturn['name'] = name
                    botReturn['image'] = bot['image']
                    botReturn['link'] = bot['link']
                    botReturn['available'] = availability

                    if availability == True:
                        botReturn['sites'] = bot['sites']
                        botReturn['available'] = True
                        return botReturn
                    else:
                        return botReturn
        return None
                    

    # - HANDLE THE HTML PAGE TO GRAB INFO FROM
    def getProdPage(self,link):
        """Goes to the link of desired bot by user and returns the html content
        Parameters
        -----------
        -link: the link of the bot to be checked on the botbroker site."""
        headers = Headers(browser='chrome', os='mac').generate()
        r = requests.get(link, headers=headers).text
        return r

# - GET THE ASK PRICES AND THE BID PRICES OF THE BOT ASKED BY USER
    def get_ask_prices(self,r):  
        """Gets the Ask prices on desired bot from lowest to highest ask price
        Parameters
        -----------
        - r: should be the prodPage with link passed to prod page. r is the html text to be parsed"""  
        soup = BeautifulSoup(r, 'lxml')
        # find the prices, returns list from lowest ask to highest
        # need to add support to view renewal copies
        ASKPrices = []
        prices = soup.find_all('div', {'class':'card-body mh-50'})[0]
        try:
            askPrices = prices.find_all('a')
            for a in askPrices:
                ask = a.div.div.text.strip()
                if '$' in ask:
                    ASKPrices.append(int(str(ask.replace('$',''))))
            ASKPrices.sort(reverse=False)
            return ASKPrices
        except Exception as e:
            logging.debug('Error retrieving ASK prices: #1')

        try:
            _list = prices.text.split()
            for price in _list:
                if '$' in price:
                    ASKPrices.append(int(str(price.replace('$', ''))))
                ASKPrices.sort(reverse=False)
            return ASKPrices
        except Exception as e:
            logging.debug('Error retrieving ASK prices: #2')

        try:
            _list = prices.find_all('a')
            for p in _list:
                price = p.div.div.text.strip()
        except Exception as e:
            logging.debug('Error retrieving ASK prices: #3')

        try:
            askPrices = prices.find_all('a', {'class':'text-dark'})
            for price in askPrices:
                allAskPrices = price.find('div',class_='card-body p-0 border-0').text.strip().split()
                for p in allAskPrices:
                    if '$' in p:
                        ASKPrices.append(int(str(p.replace('$',''))))
            ASKPrices.sort(reverse=False)
            return ASKPrices
        except Exception:
            logging.debug('Error retrieving ASK prices: #4')

    def get_bid_prices(self, r):
        """Gets the bid prices on desired bot from highest to lowest bid price
        Parameters
        -----------
        - r: should be the prodPage with link passed to prod page. r is the html text to be parsed"""  
        soup = BeautifulSoup(r, 'lxml')

        # find the prices, returned in from highest bid to lowest
        BIDPrices = []
        prices = soup.find_all('div', {'class':'card-body mh-50'})[1]
        try:
            allBids = prices.find_all('div', class_='row')
            for bid in allBids:
                Bid = bid.div.text.strip()
                BIDPrices.append(int(str(Bid).replace('$', '')))
                BIDPrices.sort(reverse=True)
            if len(BIDPrices) > 1:
                return BIDPrices
        except Exception:
            pass
        try:
            _list = prices.find_all('div', class_='row')
            for price in _list:
                price = price.div.text.split()[0]
                if '$' in price:
                    BIDPrices.append(int(str(price.replace('$', ''))))
            BIDPrices.sort(reverse=True)
            if len(BIDPrices) > 1:
                return BIDPrices

        except Exception:
            pass

        try:
            _list = prices.text.split()
            for item in _list:
                if '$' in item:
                    BIDPrices.append(int(str(item.replace('$', ''))))
                BIDPrices.sort(reverse=True)
            if len(BIDPrices) > 1:
                return BIDPrices
        except Exception:
            logging.debug("Error Retrieving the BID prices.")


    # - HANDLE THE DETAILS OF THE BOT SUCH AS THE retail, store site, recent sales ETC.
    def getBotInfo(self, r):
        """Retrieve info on the bot such as retail, links, recent sales etc. Returns a dictionary with retail, compatibility, recent sales.
        Parameters
        -----------
        - r: should be the prodPage with link passed to prod page. r is the html text to be parsed"""
        soup = BeautifulSoup(r, 'lxml')
        botsInfo = soup.find_all('div',class_='col-md-4 mb-5 pr-md-4 pl-md-4')[0]
        botsCompatibility = soup.find_all('div',class_='col-md-4 mb-5 pr-md-4 pl-md-4')[1]

        bot = dict()
        bot['recentsales'] = []

        # try to get the retail and website domain of bots
        try:
            infos = botsInfo.find_all('div', class_='col-6 text-right')
            for info in infos:
                infoTab = info.find('small', class_='font-weight-normal').text
                if '$' in infoTab or '£' in  infoTab or '€' in infoTab:
                    bot['retail'] = infoTab
                    
                if info.find('a', {'target':'_blank'}) != None:
                    bot['website'] = info.find('a', {'target':'_blank'})['href']
        except Exception:
            logging.debug('Error retrieving price of bot')

        try:
            web = bot['website']
            retail = bot['retail']
        except Exception:
            info = botsInfo.find_all('div', {'class':'row mt-2'})
            for price in info:
                if '$' in price or '£' in price or '€' in price:
                    bot['retail'] = price.small.text
                elif price.find('a', {'target':'_blank'}) != None:
                    bot['website'] = (price.find('a', {'target':'_blank'})['href'])
        try:
            web = bot['website']
            retail = bot['retail']
        except Exception:
            infos = botsInfo.find_all('div', class_='row mt-2')
            for info in infos:
                # get the price
                infoTab = info.find('small', class_='font-weight-normal').text
                if '$' in infoTab or '£' in  infoTab or '€' in infoTab:
                    bot['retail'] = infoTab
                if info.find('a') != None:
                    bot['website'] = info.find('a', {'target':'_blank'})['href']
        
        web = bot['website']
        retail = bot['retail']

        try:
            botsCompatible = []
            botsCompatibility = botsCompatibility.find_all('small')
            for bots in botsCompatibility:
                if bots.find('i', class_='fab fa-windows mr-2 text-danger') != None:
                    botsCompatible.append(bots.span.text)
                elif bots.find('i', class_='fab fa-apple mr-2 text-danger') != None:
                    botsCompatible.append(bots.span.text)
                elif bots.find('i', class_='fab fa-mobile mr-2 text-danger') != None:
                    botsCompatible.append(bots.span.text)
                
                # this line is not really neccesary since im only adding in the Available bots
                elif bots.find('i', class_='fas fa-mobile mr-2 text-muted') != None:
                    unavailableBots = bots.span.text
                elif bots.find('i', class_='fab fa-windows mr-2 text-muted') != None:
                    unavailableBots = bots.span.text
                elif bots.find('i', class_='fab fa-apple mr-2 text-muted') != None:
                    unavailableBots = bots.span.text
            bot['compatible'] = botsCompatible
        except Exception:
            logging.debug('Error retrieving compatibility of bot')


        try:
            recentSales = soup.find_all('div',class_='card-body border-transparent shadow-light bg-light mt-3 pt-3 pb-3 pl-4 pr-4')
            i = 0
            for sale in recentSales:
                i += 1
                sales = sale.small.text.replace('-','').split()
                recentsalesDict = {}
                if sales[-3] == 'about':
                    recentsalesDict['timestamp'] = f'{sales[-3]} {sales[-2]} {sales[-1]}'
                    recentsalesDict['date'] = f'{sales[-6]} {sales[-5]} {sales[-4]}'
                elif sales[-5] == 'about':
                    recentsalesDict['timestamp'] = f'{sales[-5]} {sales[-4]} {sales[-3]}'
                    recentsalesDict['date'] = f'{sales[-8]} {sales[-7]} {sales[-6]}'
                else:
                    recentsalesDict['date'] = f'{sales[-5]} {sales[-4]} {sales[-3]}'
                    recentsalesDict['timestamp'] = f'{sales[-2]} {sales[-1]}'

                for sale in sales:
                    if sale.lower() == 'lifetime' or sale.lower() == 'renewal':
                        recentsalesDict['type'] = sale
                    elif '$' in sale or '£' in sale or '€' in sale:
                        recentsalesDict['saleprice'] = sale
                if '$' in sales[1]:
                    recentsalesDict['saleprice'] = sales[1]
                bot['recentsales'].append(recentsalesDict)
                
        except Exception as e:
            logging.debug('Error retrieving recent sales of bot')

        return bot

    
    # - HANDLE WHAT TO DO WITH ALL THE INFO AND HOW TO RUN THE SCRIPT
    def main(self):
        bot = self.bot.lower()
        userChoice = self.get_bot(bot)
        file = dict()
        # print(userChoice)
        if userChoice == None:
            logging.info(f"Nothing matching {bot}")
            product = None

            # return None
        elif userChoice != None:
            link = userChoice['link']
            botimage = userChoice['image']
            botName = userChoice['name']
            if userChoice['available'] == True:
                if len(link) > 1 and link != None:
                    logging.info(f'Successfully grabbed product: {userChoice["name"]}')
                    r = self.getProdPage(link)
                    sitesSupported = userChoice['sites']
                    file['available'] = True
                    # BID (BUYING) prices returned Highest bid to Lowest bid
                    bidPrices = self.get_bid_prices(r)
                    
                    # ASK (SELLING) prices returned as list from Lowest ask to Highest ask
                    askPrices = self.get_ask_prices(r)

                    # get the bot info and create a new dictionary to return to bot
                    botInfo = self.getBotInfo(r)
                    product = dict()
                    product['BBlink'] = link
                    product['botlink'] = botInfo['website']
                    product['retail'] = botInfo['retail']
                    product['name'] = botName
                    product['image'] = botimage
                    product['sites'] = sitesSupported
                    product['compatibility'] = botInfo['compatible']
                    product['available'] = userChoice['available']

                    # returned from lowest ask to highest bid
                    if len(askPrices) >= 8:
                        product['asks'] = askPrices[:7]
                    else:
                        product['asks'] = askPrices

                    # returned from highest bid to lowest bid
                    if len(bidPrices) >= 8:
                        product['bids'] = bidPrices[:7]
                    else:
                        product['bids'] = bidPrices
                    product['recentsales'] = list()
                    for p in botInfo['recentsales']:
                        prod = dict()
                        prod['type'] = p['type']
                        prod['date'] = f"{p['date']} {p['timestamp']}"
                        prod['saleprice'] = p['saleprice']
                        product['recentsales'].append(prod)
                    # return product         
            else:
                product = dict()
                product['name'] = botName
                product['image'] = botimage
                product['available'] = userChoice['available']
            logging.info('Succesfully returned a product to bot / user.')

        embed = self.set_embed(product)
        return embed




if __name__ == "__main__":
    c = BotBroker('tohru').main()
    print(c)
    # c = BotBroker('cyber').main()