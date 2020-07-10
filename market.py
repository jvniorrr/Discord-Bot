import requests, json, logging

class StockX():
    def __init__(self, keyword):
        self.keyword = str(keyword.lower())
        self.keywordSearch = str(self.keyword).replace(' ', '%20')
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
        logging.basicConfig(format='%(asctime)s[%(levelname)s] - %(message)s', level=logging.INFO, datefmt='[%I:%M:%S %p %Z]')
        logging.info('Searching StockX for: ' + str(self.keyword).title())


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
            response = requests.get(apiurl, headers=self.headers)
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
            response = requests.get(apiurl, headers=self.headers)
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
        return info


if __name__ == '__main__':
    keyword = 'air pods'
    keyword = 'kaws figure'
    c = StockX(keyword=keyword).main()
    print(c)