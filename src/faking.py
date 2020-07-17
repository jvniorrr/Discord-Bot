import os, sys, json, io, random, logging
import names, time, datetime, string
from pytz import timezone
import discord


class Address:
    """4 Character address jigger, returns a list of addresses
    Parameters
    ----------
    - Address: (str) The address to be jigged, will add 3 letters in front
    - Total: (int) The number of times for the address to be jigged. Try do limit of 30 if plan on bigger scale
    """
    def __init__(self,address, total):
        self.addresses = []
        self.address = address
        self.total = total
        

    def _4char(self,stringLength=4):
        letters = string.ascii_uppercase
        return ''.join(random.choice(letters) for i in range(stringLength))
    

    def accountsTxt(self,accounts:list):
        """Writes to the txt file which should be further sent within the webhook
        Parameters
        ----------
        - Accounts: List value with accounts that were successful in being created to site
        - Site: The shopify site to create accounts on. Ex: 'undefeated.com'
        """
        est = timezone('EST')
        currentTime = datetime.datetime.now(est)
        # site = site.lower()

        directory = os.getcwd()
        newDir = os.path.join(directory, "AddressJig")
        try: 
            os.mkdir(newDir)
        except FileExistsError:
            pass

        fileDir = os.path.join(str(newDir), f"PropertyFaker.txt")
        file = open(fileDir, "w")
        fileWrite = f"Address Jigger.\nCreated: [{currentTime.strftime('%I:%M:%S %p')}]\n"
        file.write(fileWrite)
        total = len(accounts)
        for account in accounts:
            file.write(account)
        file.write("\n")
        file.close()

        return fileDir

    def main(self):
        addresses = []
        for _ in range(self.total):
            jig = self._4char()
            newAddress = f"{str(jig)} {self.address}"
            addresses.append(newAddress)
        # return addresses
        fileDir = self.accountsTxt(addresses)
        return fileDir


class gmailDot():
    def __init__(self):
        pass
        # self.email = str(email)
        # self.dot_trick(self.email)

    def write_file(self, emails):
        directory = os.getcwd()
        newDir = os.path.join(directory, "Gmails")
        try: 
            os.mkdir(newDir)
        except FileExistsError:
            pass
        
        fileDir = os.path.join(str(newDir), "FakerEmails.txt")
            
        # for account in accounts:
        file = open(fileDir, "w")
        if len(emails) > 50:
            for account in emails[:50]:
                file.write(account)
                file.write("\n")

        else:
            for account in emails:
                file.write(account)
                file.write("\n")

        file.close()

        # print(fileDir)
        return fileDir

    def dot_trick(self, username):
        emails = list()

        if '@' in  username:
            username =  username.split('@')[0]
        username_length = len(username)
        combinations = pow(2, username_length - 1)
        padding = "{0:0" + str(username_length - 1) + "b}"
        for i in range(0, combinations):
            bin = padding.format(i)
            full_email = ""

            for j in range(0, username_length - 1):
                full_email += (username[j]);
                if bin[j] == "1":
                    full_email += "."
            full_email += (username[j + 1])
            emails.append(full_email + "@gmail.com")
        # if len(e) > 50:
        try:
            e = self.write_file(emails[:50])
        except Exception:
            logging.warning('Error occured while calling the gmail dot function')
            e= None
        # else:
        # e = self.write_file(emails)
        return e


class Fees():
    def __init__(self, price):
        self.price = int(price)

    def main(self):
        price = self.price
        try:
            paypal = round((price * 0.029 + 0.30), 2)
            stockx = round((price * 0.095), 2)
            stockx2 = round((price * 0.09), 2)
            stockx3 = round((price * 0.085), 2)
            stockx4 = round((price * 0.08), 2)
            goatUS = round((price * 0.095 + 5), 2)
            goatCA = round((price * 0.095 + 20), 2)
            goatOT = round((price * 0.095 + 30), 2)
            ebay = round((price * 0.129 + 0.30), 2)
            mercari = round((price * 0.1), 2)
            bump = round((price * 0.089 + 0.30), 2)
            bumpI = round((price * 0.104 + 0.30), 2)
            grailed = round((price * 0.089 + 0.30), 2)
            grailedI = round((price * 0.104 + 0.30), 2)
        except Exception:
            print('Number must have not been recognized as a integer value.')
        try:
            embed = discord.Embed(title="Fee Calculator", color=0x4EA3F1)
            # auth = 'https://www.pinclipart.com/picdir/middle/358-3584297_gears-clipart-civil-engineering-tool-logo-mcanique-png.png'
            embed.set_author(name="Fee Calculator", icon_url='https://i.dlpng.com/static/png/268736_preview.png')
            embed.set_thumbnail(url="https://i.dlpng.com/static/png/268736_preview.png")
            embed.add_field(name="PayPal:", value="${}".format(paypal), inline=False)
            embed.add_field(name="StockX Level 1:", value="${}".format(stockx), inline=False)
            embed.add_field(name="StockX Level 2:", value="${}".format(stockx2), inline=False)
            embed.add_field(name="StockX Level 3:", value="${}".format(stockx3), inline=False)
            embed.add_field(name="StockX Level 4:", value="${}".format(stockx4), inline=False)
            embed.add_field(name="GOAT (US):", value="${}".format(goatUS), inline=False)
            embed.add_field(name="GOAT (CA):", value="${}".format(goatCA), inline=False)
            embed.add_field(name="GOAT (Other):", value="${}".format(goatOT), inline=False)
            embed.add_field(name="eBay:", value="${}".format(ebay), inline=False)
            embed.add_field(name="Mercari:", value="${}".format(mercari), inline=False)
            embed.add_field(name="BUMP:", value="${}".format(bump), inline=False)
            embed.add_field(name="BUMP (International):", value="${}".format(bumpI), inline=False)
            embed.add_field(name="Grailed:", value="${}".format(grailed), inline=False)
            embed.add_field(name="Grailed (International):", value="${}".format(grailedI), inline=False)
            file = discord.Embed.to_dict(embed)
        except Exception:
            file = None
        return file

if __name__ == '__main__':
    g = gmailDot().dot_trick('washed@gmail.com')
    print(str(g))