import requests, json, logging, discord, os, random

class StockX():
    """Class that searches StockX using Algolia's search engine / API, using the keywords provided by user
    Parameters
    ----------
    - Keyword: Joins the keywords provided and uses those for searching the API. * (Can be multiple kwds)
    """
    def __init__(self, keyword):
        self.keyword = str(keyword.lower())
        self.keywordSearch = str(self.keyword).replace(' ', '%20')
        self.red = 0xd40000
        self.proxy = self.get_proxy()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
        logging.basicConfig(format='%(asctime)s[%(levelname)s] - %(message)s', level=logging.INFO, datefmt='[%I:%M:%S %p %Z]')
        logging.info('Searching StockX for: ' + str(self.keyword).title())

    def get_proxy(self):
        """Returns dictionary value of a proxy to use in request"""
        try:
            cwDir = os.getcwd()
            currentDir = os.path.join(str(cwDir), "proxies.txt")
            proxies = open(currentDir).read().splitlines()
        except TypeError:
            print("File path not found, provide a valid one")
            
        proxy = random.choice(proxies)
        split = proxy.split(":")
        ip = split[0]
        port = split[1]
        try:
            user = split[2]
            password = split[3]
            dict = {
            "http": f"http://{user}:{password}@{ip}:{port}",
            "https": f"https://{user}:{password}@{ip}:{port}",
            }
        except:
            dict = {
            "http": f"http://{ip}:{port}",
            "https": f"https://{ip}:{port}",
            }
        return dict


    def StreetwearInfo(self, url):
        """Grabs info from StockX for product (Streetwear) and returns a dictionary with proper info
        Parameters
        ---------
        - URL: urlKey should be passed from Algolia Search API which returns a json file with a url key, which is passed here then parsed
        """
        # grab prod info from StockX
        try:
            apiurl = f"https://stockx.com/api/products/{url}?includes=market,360&currency=USD"
            response = requests.get(apiurl, headers=self.headers)
            if response.ok:
                response = response.json()
                response = response['Product']
        except Exception:
            logging.debug('Error retrieving info from StockX.')

        info = dict()
        info['category'] = 'streetwear'
        try:
            info['name'] = response['title']
        except Exception:
            info['name'] = 'N/A'
        try:
            info['picture'] = response['media']['imageUrl']
        except Exception:
            info['picture'] = 'https://stockx-assets.imgix.net/logo/stockx_homepage_logo_dark.svg?auto=compress,format'
        try:
            info['release'] = response['releaseDate']
        except Exception:
            info['release'] = 'N/A'
        try:
            for item in response['traits']:
                if item['name'] == 'Retail':
                    info['retail'] = f"${item['value']}"
        except Exception:
            info['retail'] = 'N/A'
        try:
            info['brand'] = response['brand']
        except Exception:
            info['brand'] = 'N/A'
        try:
            info['url'] = f"https://stockx.com/{response['urlKey']}"
        except Exception:
            info['url'] = "https://stockx.com/"

        info['lowestask'] = f"${response['market']['lowestAsk']}"
        info['highestbid'] = f"${response['market']['highestBid']}"


        try:
            lastSale = dict()
            lastSale['price'] = f"${response['market']['lastSale']}"
            lastSale['size'] = response['market']['lastSaleSize']
            lastSale['date'] = str(response['market']['lastSaleDate'])[:19].replace('T', ' • ')
            info['lastsale'] = lastSale
        except Exception:
            info['lastsale'] = None

        # grab the lowest asks in the children key
        # try to retrieve recent sales
        sizes = []
        try:
            for key, value in response['children'].items():
                sizeInfo = dict()
                sizeInfo['retail'] = info['retail']

                try:
                    sizeInfo['size'] = value['market']['lowestAskSize']
                except Exception:
                    sizeInfo['size'] = 'N/A'
                try:
                    sizeInfo['lowestask'] = f"${value['market']['lowestAsk']}"
                except Exception:
                    sizeInfo['lowestask'] = 'N/A'

                if sizeInfo['lowestask'] != '$0':
                    sizes.append(sizeInfo)
            info['asks'] = sizes
            
        except Exception:
            info['asks'] = None

        return info

    def SneakerInfo(self, url):
        """Grabs info from StockX for product (Sneaker) and returns a dictionary with proper info
        Parameters
        ---------
        - URL: urlKey should be passed from Algolia Search API which returns a json file with a url key, which is passed here then parsed
        """
        
        
        # grab prod info from StockX
        try:
            apiurl = f"https://stockx.com/api/products/{url}?includes=market,360&currency=USD"
            response = requests.get(apiurl, headers=self.headers,proxies=self.proxy)
            if response.ok:
                response = response.json()
                response = response['Product']
        except Exception:
            logging.debug('Error retrieving info from StockX.')

        info = dict()
        info['category'] = 'sneakers'

        try:
            info['name'] = response['title']
        except Exception:
            info['name'] = 'N/A'
        try:
            info['picture'] = response['media']['imageUrl']
        except Exception:
            info['picture'] = 'https://stockx-assets.imgix.net/logo/stockx_homepage_logo_dark.svg?auto=compress,format'
        try:
            info['release'] = response['releaseDate']
        except Exception:
            info['release'] = 'N/A'
        try:
            info['retail'] = f"${response['retailPrice']}"
        except Exception:
            info['retail'] = 'N/A'
        try:
            info['brand'] = f"{response['styleId']}"
        except Exception:
            info['brand'] = 'N/A'
        try:
            info['url'] = f"https://stockx.com/{response['urlKey']}"
        except Exception:
            info['url'] = "https://stockx.com/"

        info['lowestask'] = f"${response['market']['lowestAsk']}"
        info['highestbid'] = f"${response['market']['highestBid']}"


        try:
            lastSale = dict()
            lastSale['price'] = f"${response['market']['lastSale']}"
            lastSale['size'] = response['market']['lastSaleSize']
            lastSale['date'] = str(response['market']['lastSaleDate'])[:19].replace('T', ' • ')
            info['lastsale'] = lastSale
        except Exception:
            info['lastsale'] = None

        # grab the lowest asks in the children key
        # try to retrieve recent sales
        sizes = []
        try:
            for key, value in response['children'].items():
                sizeInfo = dict()
                sizeInfo['retail'] = info['retail']
                try:
                    sizeInfo['size'] = value['market']['lowestAskSize']
                except Exception:
                    sizeInfo['size'] = 'N/A'
                try:
                    sizeInfo['lowestask'] = f"${value['market']['lowestAsk']}"
                except Exception:
                    sizeInfo['lowestask'] = 'N/A'
                if sizeInfo['lowestask'] != '$0':
                    sizes.append(sizeInfo)
            info['asks'] = sizes
            
        except Exception:
            info['asks'] = None
    
        return info

    def CollectibleInfo(self, url):
        """Grabs info from StockX for product (Sneaker) and returns a dictionary with proper info
        Parameters
        ---------
        - URL: urlKey should be passed from Algolia Search API which returns a json file with a url key, which is passed here then parsed
        """
        
        # grab prod info from StockX
        try:
            apiurl = f"https://stockx.com/api/products/{url}?includes=market,360&currency=USD"
            response = requests.get(apiurl, headers=self.headers, proxies=self.proxies)
            if response.ok:
                response = response.json()
                response = response['Product']
        except Exception:
            logging.debug('Error retrieving info from StockX.')

        info = dict()
        info['category'] = 'collectibles'

        try:
            info['name'] = response['title']
        except Exception:
            info['name'] = 'N/A'
        try:
            info['picture'] = response['media']['imageUrl']
        except Exception:
            info['picture'] = 'https://stockx-assets.imgix.net/logo/stockx_homepage_logo_dark.svg?auto=compress,format'
        try:
            info['release'] = response['releaseDate']
        except Exception:
            info['release'] = 'N/A'
        try:
            for item in response['traits']:
                if item['name'] == 'Retail':
                    info['retail'] = f"${item['value']}"
        except Exception:
            info['retail'] = 'N/A'

        for item in response['traits']:
            if item['name'] == 'size':
                info['sizes'] = item['value']

        try:
            info['brand'] = response['brand']
        except Exception:
            info['brand'] = 'N/A'
        try:
            info['url'] = f"https://stockx.com/{response['urlKey']}"
        except Exception:
            info['url'] = "https://stockx.com/"

        info['lowestask'] = f"${response['market']['lowestAsk']}"
        info['highestbid'] = f"${response['market']['highestBid']}"


        try:
            lastSale = dict()
            lastSale['price'] = f"${response['market']['lastSale']}"
            if info['sizes']:
                lastSale['size'] = info['sizes']
            else:
                lastSale['size'] = response['market']['lastSaleSize']
            lastSale['date'] = str(response['market']['lastSaleDate'])[:19].replace('T', ' • ')
            info['lastsale'] = lastSale
        except Exception:
            info['lastsale'] = None

        # grab the lowest asks in the children key
        # try to retrieve recent sales
        sizes = []
        try:
            for key, value in response['children'].items():
                sizeInfo = dict()
                sizeInfo['retail'] = info['retail']
                try:
                    if info['sizes']:
                        sizeInfo['size'] = info['sizes']
                    elif value['market']['lowestAskSize'] != None:
                        sizeInfo['size'] = value['market']['lowestAskSize']
                    else:
                        sizeInfo['size'] = 'N/A'
                except Exception:
                    sizeInfo['size'] = 'N/A'
                try:
                    sizeInfo['lowestask'] = f"${value['market']['lowestAsk']}"
                except Exception:
                    sizeInfo['lowestask'] = 'N/A'
                if sizeInfo['lowestask'] != '$0':
                    sizes.append(sizeInfo)
            info['asks'] = sizes
            
        except Exception:
            info['asks'] = None
    
        return info

    def set_embed(self, info):
        if info != None:
            embed = discord.Embed(color=0x09A05E)
            authURL = 'https://media.discordapp.net/attachments/661223352115003402/730649326338048000/stockX.png'
            embed.set_author(name='StockX', url='https://www.stockx.com', icon_url=authURL)
            embed.set_thumbnail(url=info['picture'])
            name = f"[{info['name']}]({info['url']})"
            embed.add_field(name='**Title**', value=name, inline=False)
            if info['category'] == 'streetwear' or info['category'] == 'collectibles':
                snkrInfo = f"__**Retail**__: `{info['retail']}`\n__**Brand**__: {info['brand']}\n__**Release**__: `{info['release']}`"
            elif info['category'] == 'sneakers':
                snkrInfo = f"__**Retail**__: `{info['retail']}`\n__**SKU**__: {info['brand']}\n__**Release**__: `{info['release']}`"
            
            embed.add_field(name='**Info**', value=snkrInfo, inline=False)
            if info['lastsale'] != None:
                recentSale = f"**__Sale Price__**: {info['lastsale']['price']}\n**__Sale Date__**: {info['lastsale']['date']}\n**__Size__**: {info['lastsale']['size']}"
                embed.add_field(name='**Recent Sale**', value=recentSale, inline=False)
            embed.add_field(name='\u200B', value='\u200B',inline=False)
            try: 
                embed.add_field(name='**Highest Bid**', value=f"{info['highestbid']}", inline=True)
                embed.add_field(name='**Lowest Ask**', value=f"{info['lowestask']}", inline=True)
            except Exception:
                pass
            embed.add_field(name='\u200B', value='\u200B',inline=False)

            try:
                if len(info['asks']) > 7:
                    asks1 = ''
                    for ask in info['asks'][:7]:
                        asks1 += f"[**{str(ask['size'])}** • ({ask['lowestask']})]({info['url']})\n"
                    try:
                        if asks1 != '':
                            embed.add_field(name='**Asks**', value=asks1)
                    except Exception:
                        pass

                    asks2 = ''
                    try:
                        for ask in info['asks'][7:14]:
                            asks2 += f"[**{str(ask['size'])}** • ({ask['lowestask']})]({info['url']})\n"
                        try:
                            if asks2 != '':
                                embed.add_field(name='**Asks**', value=asks2)
                        except Exception:
                            pass
                    except Exception:
                        pass

                    asks3 = ''
                    try:
                        for ask in info['asks'][14:21]:
                            asks3 += f"[**{str(ask['size'])}** • ({ask['lowestask']})]({info['url']})\n"
                        try:
                            if asks3 != '':
                                embed.add_field(name='**Asks**', value=asks3, inline=True)
                        except Exception:
                            pass
                    except Exception:
                        pass
                else:
                    asks1 = ''
                    for ask in info['asks']:
                        asks1 += f"[**{str(ask['size'])}** • ({ask['lowestask']})]({info['url']})\n"
                    try:
                        if asks1 != '':
                            embed.add_field(name='**Asks**', value=asks1)
                    except Exception:
                        pass
            except Exception:
                pass
        else:
            title = '**No results were found. Please use the appropiate format and keywords. Examples below**'
            embed = discord.Embed(color=0xd40000, title=title)
            authURL = 'https://media.discordapp.net/attachments/661223352115003402/730649326338048000/stockX.png'
            embed.set_author(name='StockX', url='https://www.stockx.com', icon_url=authURL)
        embed = embed.to_dict()
        return embed

    
    def main(self):
        """My method but doesnt seem to return all the info about the shoe like lowest asks / bids per size."""

        data = {"params":f"query={self.keywordSearch}&facets=*&filters="}
        # url = 'https://xw7sbct9v6-1.algolianet.com/1/indexes/products/query?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%203.32.1&x-algolia-application-id=XW7SBCT9V6&x-algolia-api-key=6bfb5abee4dcd8cea8f0ca1ca085c2b3'

        # this link is one that I retrieved manually with requests, above is used by git code. 
        url = 'https://xw7sbct9v6-dsn.algolia.net/1/indexes/products/query?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%203.32.1&x-algolia-application-id=XW7SBCT9V6&x-algolia-api-key=6bfb5abee4dcd8cea8f0ca1ca085c2b3'

        # try / exception block in case error when utilizing proxies
        try:
            response = requests.post(url, headers=self.headers, json=data)
        except Exception:
            logging.debug('Error retrieving info from Algolia.')
            info = None
            return info

        # parse the page if ok
        if response.ok:
            response = response.json()
            if len(response["hits"]) != 0:
                hits = response["hits"][0]
                if hits['product_category'] == 'streetwear':
                    info = self.StreetwearInfo(hits['url'])
                    logging.info(f'Product found: {info["name"]}')
                elif hits['product_category'] == 'sneakers':
                    info = self.SneakerInfo(hits['url'])
                    logging.info(f'Product found: {info["name"]}')
                elif hits['product_category'] == 'collectibles':
                    info = self.CollectibleInfo(hits['url'])
                    logging.info(f'Product found: {info["name"]}')
                else:
                    info = None
            else:
                logging.info(f'No products found matching {str(self.keyword).title()}')
                info = None
        i = self.set_embed(info)
        return i

class GOAT():
    """Class that searches GOAT (AirGOAT) using Algolia's search engine / API, using the keywords provided by user.
    Returns an embed dictionary to be passed to discord bot.
    Parameters
    ----------
    - Keyword: Joins the keywords provided and uses those for searching the API. * (Can be multiple kwds)
    """
    def __init__(self, keyword):
        self.keyword = str(keyword.lower())
        self.proxies = self.get_proxy()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
        logging.basicConfig(format='%(asctime)s[%(levelname)s] - %(message)s', level=logging.INFO, datefmt='[%I:%M:%S %p %Z]')
        logging.info(f'Searching GOAT for: {str(self.keyword).title()}')

    def get_proxy(self):
        """Returns dictionary value of a proxy to use in request"""
        try:
            cwDir = os.getcwd()
            currentDir = os.path.join(str(cwDir), "proxies.txt")
            proxies = open(currentDir).read().splitlines()
        except TypeError:
            print("File path not found, provide a valid one")
            
        proxy = random.choice(proxies)
        split = proxy.split(":")
        ip = split[0]
        port = split[1]
        try:
            user = split[2]
            password = split[3]
            dict = {
            "http": f"http://{user}:{password}@{ip}:{port}",
            "https": f"https://{user}:{password}@{ip}:{port}",
            }
        except:
            dict = {
            "http": f"http://{ip}:{port}",
            "https": f"https://{ip}:{port}",
            }
        return dict

    def asksAPI(self, slug):
        """Gets ask info on product requested by user
        Parameters
        ----
        - Slug: the urlKey passed from algolia API
        """
        # asks API from goat
        try:
            asksAPI = f'https://www.goat.com/web-api/v1/product_variants?productTemplateId={slug}'
            bids = requests.get(asksAPI, headers=self.headers).json()

            sizes = []
            for size in bids:
                if size['shoeCondition'] == 'new_no_defects' and size['boxCondition'] == 'good_condition':
                    if size['size'] not in sizes:
                        option = dict()
                        option['size'] = size['size']
                        option['lowestprice'] = f"${str(float(size['lowestPriceCents']['amount']) * .01)[:-2]}"
                        sizes.append(option)
            return sizes
        except Exception:
            return None

    def neg_embed(self):
        """Negative embed for response that return None / nothing. Only thing to do is set footer the way I like it in bot & the description key"""
    
        # desc = 'na'
        title = '**No results were found. Please use the appropiate format and keywords. Examples below**'
        embed = discord.Embed(color=0xd40000, title=title)
        authUrl = 'https://cdn.discordapp.com/attachments/661223352115003402/731014001885970502/goat.png'
        embed.set_author(name='GOAT', url='https://www.goat.com', icon_url=authUrl)
        i = embed.to_dict()
        return i

    def set_embed(self, info):
        if info != None:
            try:
                embed = discord.Embed(color=0x2F3136)
                authUrl = 'https://cdn.discordapp.com/attachments/661223352115003402/731014001885970502/goat.png'
                embed.set_author(name='GOAT', url='https://www.goat.com', icon_url=authUrl)
                embed.set_thumbnail(url=info['picture'])
                embed.add_field(name='**Title**', value=f"[{info['name']}]({info['url']})",inline=False)
                snkrInfo = f"__**Retail**__: `{info['retail']}`\n__**SKU**__: {info['sku']}\n__**Release**__: `{info['release']}`"
                embed.add_field(name='**Info**', value=snkrInfo, inline=False)
                embed.add_field(name='\u200B', value='\u200B',inline=False)
            except Exception:
                pass
            if len(info['asks']) != 0:
                if len(info['asks']) >= 7:
                    try:
                        asks1 = ''
                        for ask in info['asks'][:7]:
                            asks1 += f"[**{str(ask['size'])}** • {ask['lowestprice']}]({info['url']})\n"
                        if asks1 != '':
                            embed.add_field(name='**Asks**', value=asks1)
                    except Exception:
                        pass
                    try:
                        asks2 = ''
                        for ask in info['asks'][7:14]:
                            asks2 += f"[**{str(ask['size'])}** • {ask['lowestprice']}]({info['url']})\n"
                        if asks2 != '':
                            embed.add_field(name='**Asks**', value=asks2)
                    except Exception:
                        pass
                    try:
                        asks3 = ''
                        for ask in info['asks'][14:21]:
                            asks3 += f"[**{str(ask['size'])}** • {ask['lowestprice']}]({info['url']})\n"
                        if asks3 != '':
                            embed.add_field(name='**Asks**', value=asks3, inline=True)
                    except Exception:
                        pass
                    
                else:
                    try:
                        asks1 = ''
                        for ask in info['asks']:
                            asks1 += f"[**{str(ask['size'])}** • {ask['lowestprice']}]({info['url']})\n"
                        if asks3 != '':
                            embed.add_field(name='**Asks**', value=asks1)
                    except Exception:
                        pass
            newFile = embed.to_dict()
        else:
            title = '**No results were found. Please use the appropiate format and keywords. Examples below**'
            embed = discord.Embed(color=0xd40000, title=title)
            authUrl = 'https://cdn.discordapp.com/attachments/661223352115003402/731014001885970502/goat.png'
            embed.set_author(name='GOAT', url='https://www.goat.com', icon_url=authUrl)
            newFile = embed.to_dict()
        return newFile
        

    # def offersAPI(self, id):
    #     asksAPI = f'https://www.goat.com/api/v1/highest_offers?productTemplateId={id}'
    #     bids = requests.get(asksAPI, headers=self.headers).json()
    #     # print(bids)


    def info(self,slug):
        """Grabs info about the product being polled
        Parameters
        --------
        - Slug: the urlKey passed from algolia API
        """
        # general info about the product
        try:
            generalAPI = f"https://www.goat.com/api/v1/product_templates/{slug}/show_v2"
            general = requests.get(generalAPI, headers=self.headers, proxies=self.proxies).json()
            info = dict()
            info['name'] = general['name']
            info['release'] = str(general['releaseDate'])[:10]
            info['picture'] = general['pictureUrl']
            info['url'] = f'https://www.goat.com/sneakers/{general["slug"]}/available-sizes'
            info['sku'] = str(general['sku']).replace(' ', '-')
            info['retail'] = f"${str(int(general['specialDisplayPriceCents']) * .01)[:-2]}"
            info['lowestprice'] = f"${str(int(general['lowestPriceCents']) * .01)[:-2]}"
            asks = self.asksAPI(general['slug'])
            if asks != None:
                info["asks"] = asks

            return info
        except Exception:
            return None

    def main(self):
        """My method but doesnt seem to return all the info about the shoe like lowest asks / bids per size."""

        # set the search parameters
        data = {"params":f"query=&query={self.keyword}&facetFilters=(product_category%3Ashoes)&page=0&hitsPerPage=5"}

        # set the url already set with the parameters passed. 
        url = 'https://2fwotdvm2o-dsn.algolia.net/1/indexes/product_variants_v2_trending_purchase/query?x-algolia-agent=Algolia%20for%20vanilla%20JavaScript%203.25.1&x-algolia-application-id=2FWOTDVM2O&x-algolia-api-key=ac96de6fef0e02bb95d433d8d5c7038a'

        # make a post request to the API and have info returned for GOAT.com website. (info on products)
        response = requests.post(url, headers=self.headers, proxies=self.proxies,json=data)
        # make sure the request recieved a proper response / ok status
        if response.ok:
            response = response.json()
            if len(response["hits"]) != 0:
                hits = response['hits'][0]
                if hits['product_type'] == 'sneakers':
                    tempName = hits['name']
                    slug = hits["slug"]
                    # prodID = hits["product_template_id"]
                    # info on the product
                    info = self.info(slug)

                    # offers = self.offersAPI(prodID)
                    if info != None:
                        logging.info(f"{info['name']} was found")
                    else:
                        logging.debug("Error parsing GOAT API")

                    newDict = self.set_embed(info)

                
            else:
                logging.info(f"No results found for {str(self.keyword)}...")
                newDict = self.set_embed(info=None)
        else:
            logging.error("Error retrieving a valid response from Algolia")
            newDict = None

        return newDict


if __name__ == '__main__':
    keyword = 'air pods'
    keyword = 'yeezy'
    c = GOAT(keyword=keyword).main()
    print(c)