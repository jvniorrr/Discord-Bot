import os, sys, json, io, random, logging
import names, time, datetime, string
from pytz import timezone
import requests
from fake_headers import Headers
from bs4 import BeautifulSoup


global  currentTime
est = timezone('America/New_York')
currentTime = datetime.datetime.now(est)


class AccountCreator:
    def __init__(self, site: str, email:str, total: int):
        """Class instance for creating accounts on shopify sites, input all the info
        Parameters
        ----------
        - Site: Shopify Site to create sites on Ex:'undefeated.com'
        - Email: Email to create accounts from, only accepts catchall and gmail currently
        - PWD: Password for accounts being created, preferably something secure as well
        - Proxy: True or False (Boolean), choose to use proxies or not when running script
        - Webhook: Discord Webhook to send files when Accounts are created
        - Total: Integer value of accounts to be created on site. 
        """
        if 'http://' in site:
            self.site = str(site).replace('http://', '')
        elif 'https://' in site:
            self.site = str(site).replace('https://', '')
        elif 'https' in site:
            self.site = str(site).replace('https', '')
        elif 'http' in site:
            self.site = str(site).replace('http', '')
        elif '//' in site:
            self.site = str(site).split('//')[1]
        else:
            self.site = site
        # self.site = site
        self.proxies = self.get_proxy()
        self.email = email
        self.proxy = True
        self.total = total
        self.headers = Headers(browser="chrome", os="mac").generate()
        logging.basicConfig(format='%(asctime)s[%(levelname)s] - %(message)s', level=logging.INFO, datefmt='[%I:%M:%S %p %Z]')

    def check_ecommerce(self):
        
        returnVal = None
        try:
            r = requests.get(f'https://{self.site}/meta.json', headers=self.headers, proxies=self.proxies, timeout=15)
            if (str(r.status_code) == '200'):
                logging.info("Site user requested does seem to be Shopify based.")
                returnVal = True
            else:
                logging.info("Site user requested does not seem to be Shopify based.")
                returnVal = False
        except Exception:
            logging.error("There was an issue checking if the site thuser requested was shopify based or not.")
            

        return returnVal 

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

    def passwordCreate(self,stringLength=10):
        lettersAndDigits = string.ascii_letters + string.digits
        return ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))

    def emailGen(self):
        """Creates random info to create account based on gmail or catchall"""     
        email = self.email
        password = self.passwordCreate()

        # get random Info for the account creation
        # firstName = names.get_first_name(gender='Male')
        # lastName = names.get_last_name()
        # info["firstName"] = firstName
        # info["lastName"] = lastName

        try:
            newEmail = email.split('@')
            # emailUser = newEmail[0]
            emailProvider = newEmail[-1]
            info = dict()

            if ('yahoo.com' in emailProvider) or ('hotmail.com' in emailProvider):
                info = None
                # return  None
            else:

                info["firstName"] = names.get_first_name(gender='Male')
                info["lastName"] = names.get_last_name()

                if 'gmail.com' in emailProvider:
                     jigEmail = f"{newEmail[0]}+{random.randint(0, 989899)}@{emailProvider}"
                else:
                    jigEmail = f"{info['firstName']}{random.randint(0, 989899)}@{emailProvider}"
                info["email"] = jigEmail
                info["password"] = password

            return info

        except Exception:
            logging.warning('User did not provide a proper email string value.')
            return None

    def accountsTxt(self,accounts:list, site:str):
        """Writes to the txt file which should be further sent within the webhook
        Parameters
        ----------
        - Accounts: List value with accounts that were successful in being created to site
        - Site: The shopify site to create accounts on. Ex: 'undefeated.com'
        """
        est = timezone('EST')
        # currentTime = datetime.datetime.now(est).strftime("%m-%d-%y | %I:%M:%S %p")
        site = site.lower()

        directory = os.getcwd()
        newDir = os.path.join(directory, "shopifyAccounts")
        try: 
            os.mkdir(newDir)
        except FileExistsError:
            pass

        fileDir = os.path.join(str(newDir), f"{site}accounts.txt")
        file = open(fileDir, "w")
        fileWrite = f"Site: [{site}]\nCreated: [{currentTime.strftime('%I:%M:%S %p')}]\n"
        file.write(fileWrite)
        total = len(accounts)
        for account in accounts:
            file.write(account)
        file.write("\n")
        file.close()

        return fileDir

    def make_account(self):
        """Makes accounts on most shopify accounts. Main function
        Parameters
        ----------
        Site: The site the user wants the accounts created on. Ex: ('undefeated.com')
        Amount: The ammount of sites to be created, should be an integer value
        Proxy: Chance to True if want to use proxies, to avoid being banned locally.
        """
        logging.info(f"Initializing Account creator for {self.site}:")
        accountsCreated = []

        boool = self.check_ecommerce()
        # boool = True
        if boool == True:
            if self.total > 25:
                self.total = 25
            for _ in range(self.total):

                info = self.emailGen()
                email = info["email"]
                password = info["password"]
                # proxy = accounts["proxyUse"]

                payload = {
                'form_type': 'create_customer',
                'utf8': '✓',
                'customer[first_name]': info["firstName"],
                'customer[last_name]': info["lastName"],
                'customer[email]': email,
                'customer[password]': password
                    }

                # create the accounts asked for by use
                t = True
                while t:
                    try:
                        url = f"https://{self.site}/account/"
                        if self.proxy:
                            proxy = self.get_proxy()
                            r = requests.post(url, data=payload, headers=self.headers, proxies=proxy, timeout=6)
                        else:
                            r = requests.post(url, data=payload, headers=self.headers)

                        # check if response is ok              
                        if r.ok:
                            account = f"{email}:{password}"
                            accountsCreated.append(account + "\n")
                            t = False
                        else:
                            print("Retrying account.")
                    except Exception as e:
                        print(e)
                        break
            SiteCr = (self.site).replace(".com","")
            if len(accountsCreated) != 0:
                filePath = self.accountsTxt(accounts=accountsCreated,site=SiteCr)
                logging.info(f"Finished making {self.total} accounts.")
            else:
                filePath = None

        elif boool == False:
            logging.info('The site the user provided does not seem to be Shopify based')
            filePath = 'False'

        
        elif boool == None:
            logging.error('There was an issue trying to see if the site the user requested was Shopify based or not: Connection Error.')
            filePath = 'None'
        return filePath
        





if __name__ == "__main__":
    c = AccountCreator('undefeated.com', 'jvniorrr.com', 1).make_account()