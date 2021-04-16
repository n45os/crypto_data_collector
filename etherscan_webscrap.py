import requests
from datetime import datetime
from bs4 import BeautifulSoup
from lxml import html

from selenium import webdriver
import time

"""url = "https://etherscan.io/token/0x83e6f1E41cdd28eAcEB20Cb649155049Fac3D5Aa"
driver.get(url)

tree = html.fromstring(driver.page_source)
results = tree.xpath('/html/body/div[1]/main/div[4]/div[1]/div[1]/div/div[2]/div[3]/div/div[2]/div/div')[0].text
# soup = BeautifulSoup(content ,  "html.parser")
driver.refresh()
"""
"""url = "https://etherscan.io/gastracker"
r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")
soupp = soup.prettify()
spans = soup.find("span")

tree = html.fromstring(r.content)
smth= tree.xpath('/html/body/div[1]/main/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/span/span')
"""


class Eth_scrapper:
    def __init__(self):
        from os import path, getcwd
        cur = getcwd()
        self.driver = webdriver.Chrome(cur+'/chromedriver')


    def gas_price(self):
        gas = {}
        url = "https://etherscan.io/gastracker"
        self.driver.get(url)
        time.sleep(2)
        tree = html.fromstring(self.driver.page_source)
        xpath_avg = '/html/body/div[1]/main/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/span/span'
        xpath_low = '/html/body/div[1]/main/div[3]/div/div[1]/div/div/div[2]/div[1]/div/div[1]/div[1]/span/span'
        xpath_high = '/html/body/div[1]/main/div[3]/div/div[1]/div/div/div[2]/div[3]/div/div[1]/span/font/span'
        avg_price = tree.xpath(xpath_avg)[0].text
        low_price = tree.xpath(xpath_low)[0].text
        high_price = tree.xpath(xpath_high)[0].text
        gas['average'] = int(avg_price)
        gas['low'] = int(low_price)
        gas['high'] = int(high_price)
        gas['date'] = datetime.now().isoformat()
        return gas

    def get_holders_and_num_of_transactions_of(self, contract_address):
        data = {"contract_address": contract_address}
        url = "https://etherscan.io/token/" + contract_address
        self.driver.get(url)
        tree = html.fromstring(self.driver.page_source)
        xpath_holders = '/html/body/div[1]/main/div[4]/div[1]/div[1]/div/div[2]/div[3]/div/div[2]/div/div'
        xpath_transactions = '/html/body/div[1]/main/div[4]/div[1]/div[1]/div/div[2]/div[4]/div/div[2]/span'
        holders = tree.xpath(xpath_holders)[0].text
        txns = tree.xpath(xpath_transactions)[0].text
        #print(txns)
        # to vgazei me \n mprosta kai keno sto telos ara
        holders = holders[1:-1]
        # to bgazei me komma kai eiani str kai den to pairnei o int ara
        holders = holders.replace(",", '')
        txns = txns.replace(",", '')

        data["holders"] = holders
        data["transactions"] = txns
        data["last_update"] = datetime.now().isoformat()
        return data


"""def get_num_of_transactions_of(driver, contract_address):
    url = "https://etherscan.io/token/" + contract_address
    driver.get(url)
    tree = html.fromstring(driver.page_source)
    xpath_holders = '/html/body/div[1]/main/div[4]/div[1]/div[1]/div/div[2]/div[3]/div/div[2]/div/div'
    num = tree.xpath(xpath_holders)[0].text
    # to vgazei me \n mprosta kai keno sto telos ara
    num = num[1:-1]
    # to bgazei me komma kai eiani str kai den to pairnei o int ara
    num = num.replace(",", '')
    return int(num)
"""

# gas = gas_price(driver)