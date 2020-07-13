import os, sys, json, io, random, logging
import names, time, datetime, string
from pytz import timezone


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


if __name__ == '__main__':
    g = gmailDot().dot_trick('washed@gmail.com')
    print(str(g))