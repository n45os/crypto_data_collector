import json

from pycoingecko import CoinGeckoAPI

from datetime import time
from datetime import datetime
import time


class CGapi:

    def __init__(self):
        self.cg = CoinGeckoAPI()

    def product_now(self, ids, vs_currency):
        for errors in range(0,100):
            try:
                info_dict = {}
                feed_dict = self.cg.get_price(ids=ids, vs_currencies=vs_currency, include_market_cap='true',
                                         include_24hr_vol='true', include_24hr_change='true',
                                         include_last_updated_at='true')
                info_dict["id"] = ids
                info_dict["vs_curr"] = vs_currency
                info_dict["price"] = feed_dict[ids][vs_currency]
                info_dict["market_cap"] = feed_dict[ids][vs_currency + "_market_cap"]
                info_dict["24h_vol"] = feed_dict[ids][vs_currency + "_24h_vol"]
                info_dict["24h_change"] = feed_dict[ids][vs_currency + "_24h_change"]
                info_dict["last_update"] = datetime.isoformat(datetime.fromtimestamp(feed_dict[ids]["last_updated_at"]))
                return info_dict
            except:
                if errors > 5:
                    time.sleep(30)
                time.sleep(2)
                continue



    def get_address_if_exists(self, prod, update=True):
        import requests

        address = {}

        if update:
            coin_list = self.update_coingecko_coinlist()
        else:
            coin_list = self.retrieve_coinlist_from_file()

        idx = next(i for i, item in enumerate(coin_list) if item["id"] == prod)
        platforms = coin_list[idx]["platforms"]

        try:
            if platforms["ethereum"] != "":
                address["ethereum"] = platforms["ethereum"]
                return True, address
        except:
            return False, {}

    def update_coingecko_coinlist(self, ):
        import requests
        from os import path, getcwd
        cur = getcwd()
        try:
            self.coinlist = requests.get("https://api.coingecko.com/api/v3/coins/list?include_platform=true").json()
            with open(cur + "/info/coinlist.dat", "w") as f:
                json.dump(self.coinlist, f, indent=4)
            return self.coinlist
        except:
            print('could update the coinlist')

    def find_new_product_in_coinlist(self, prod, update=True):
        if update:
            coin_list = self.update_coingecko_coinlist()
        else:
            coin_list = self.retrieve_coinlist_from_file()
        try:
            idx = next(i for i, item in enumerate(coin_list) if item["id"] == prod)
        except:
            print("could not find the product with this name.")
            print("search the coilist.dat file to find the product code of your product")
            return False, None

        prod_dict = coin_list[idx]
        prod_dict_formated = {}
        return True, prod_dict

    def retrieve_coinlist_from_file(self):
        from os import path, getcwd
        cur = getcwd()
        with open(cur + "/info/coinlist.dat", "r") as f:
            return json.load(f)



c = CGapi()
c.update_coingecko_coinlist()

"""ret = product_now('ethereum', 'usd')
test = cg.get_price(ids='bitcoin', vs_currencies='usd', include_market_cap='true', include_24hr_vol='true',
                    include_24hr_change='true', include_last_updated_at='true')
# var = list(test.keys())[0]
print(ret)

print(datetime.now())
"""
