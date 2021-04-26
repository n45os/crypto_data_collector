from coingecko import CGapi
from etherscan_webscrap import Eth_scrapper as Es
from product_dict import Product_dict as pd

from datetime import datetime, timedelta
import json
import csv
import os
import time


"""
stored data format

{
id : "p_id"
platform : "eth" or None
address : "hash" or None if not in eth 
date_created = "creation_date"
data :
    {
    date: "measurement_date" (last_update from coingecko)
    price : 
    m_cap :
    24h_vol:
    24h_change:
    
    coingecko_top7trending : boolean
    
    
    }
}
    
"""




"""prod_dict = {}
prod_dict["vs_currency"] = 'usd'
prod_dict["products"] = "bitcoin", "ethereum", "polkastarter"
# kathe posh wra tha ginetai to update
prod_dict["interval_time_secs"] = 40
prod_dict["gas_price_interval"] = 40
# prod_dict = {"vs_currency": {'usd'}, "products": {"bitcoin", "ethereum", "polkastarter"}, "interval_time_secs": 300}
"""
import requests
"""from os import path, getcwd
cur = getcwd()
with open(cur + "/info/product_dict.dat", "w") as f:
    json.dump(prod_dict, f, indent=4)"""
#data = {"data": {"price", "m_cap", "24h_vol"}}


if os.uname().nodename == 'raspberrypi':
    #yellow @ pin23, green @ pin17
    from gpiozero import LED

    green_led = LED(17)
    green_led.off()
    yellow_led = LED(23)
    yellow_led.off()

eth_scpr = Es()
pd = pd()
prod_dict = pd.prod_dict

cg = CGapi()


def collect_if_available(prod_dict, schedule):
    date_now = datetime.now()
    if date_now > schedule['gas_time']:
        update_gas()
        schedule['gas_time'] += timedelta(seconds=prod_dict["gas_price_interval"])
        return None
    for prod in prod_dict['products']:
        if date_now > schedule[prod]:
            its_time_for = prod
            schedule[prod] += timedelta(seconds=prod_dict["interval_time_secs"])
            return its_time_for


def collect_in_file(prod, prod_dict):
    cg_data = cg.product_now(prod, prod_dict["vs_currency"])
    info = get_info_json_of(prod)
    if info['platform'] == 'eth':
        eth = eth_scpr.get_holders_and_num_of_transactions_of(info['address']['ethereum'])
    else:
        eth = {"holders": None, 'transactions': None, 'last_update': None}

    from os import path, getcwd
    cur = getcwd()
    path = cur + "/stored_data/" + prod + "_data.csv"
    is_new = not os.path.exists(path)
    # csv header of type:
    # "date,cg_vs_cur,cg_price,cg_m_cap,cg_24h_vol,cg_24h_change,holders,transactions,etherscan_upd_time"
    write = f"\n{cg_data['last_update']},{cg_data['vs_curr']},{cg_data['price']},{cg_data['market_cap']}," \
            f"{cg_data['24h_vol']},{cg_data['24h_change']},{eth['holders']},{eth['transactions']},{eth['last_update']}"
    with open(path, "a") as f:
        f.write(write)


def get_info_json_of(prod):
    from os import path, getcwd
    cur = getcwd()
    with open(cur + "/stored_data/" + prod + "_info.json", "r") as f:
        return json.load(f)


def update_gas():
    gas = eth_scpr.gas_price()
    from os import path, getcwd
    cur = getcwd()
    write = f"\n{gas['date']},{gas['low']},{gas['average']},{gas['high']}"
    with open(cur + '/stored_data/gas.csv', 'a') as f:
        f.write(write)


def init_schedule(prod_dict):
    schedule = {}
    now = datetime.now()
    products_num = len(prod_dict["products"])
    # xwrizei ton xrono mesa sta available gia na yparxoun oi ligotero dynates kathisteriseis
    secs_for_next = prod_dict["interval_time_secs"] / products_num
    schedule["gas_time"] = now
    idx = 1
    for prod in prod_dict["products"]:
        schedule[prod] = now + idx * timedelta(seconds=secs_for_next) + timedelta(seconds=1)
        idx += 1
    return schedule


def init_files(prod_dict):
    from os import path, getcwd
    cur = getcwd()

    for prod in prod_dict["products"]:
        ad_exist, address = cg.get_address_if_exists(prod)
        if not path.exists(cur + "/stored_data/" + prod + "_data.csv"):
            if ad_exist:
                new_dict = {"id": prod, 'platform': 'eth', "address": address,
                            "creation_date": str(datetime.isoformat(datetime.now()))}
            else:
                new_dict = {"id": prod, 'platform': None, "address": None,
                            "creation_date": str(datetime.isoformat(datetime.now()))}

            data_dict = {"data": {}}

            data_header = "date,cg_vs_cur,cg_price,cg_m_cap,cg_24h_vol,cg_24h_change,holders,transactions,etherscan_upd_time"
            # to_json = json.dumps(new_dict)
            # make the data file
            with open(cur + "/stored_data/" + prod + "_data.csv", "w") as new_file:
                new_file.write(data_header)
                # new_file.write(json.dump(new_dict,fp=new_file))
            # make the info file
            with open(cur + "/stored_data/" + prod + "_info.json", "w") as new_file:
                json.dump(new_dict, new_file, indent=4)
                # new_file.write(json.dump(new_dict,fp=new_file))


def address_from_id(prod_id):
    i = 0
    for prod in prod_dict["products"]:
        if prod == prod_id:
            return prod_id["platforms"]
        i += 1


def run(quick = False):
    if not quick:
        pd.ask_for_verification()
    schedule = init_schedule(prod_dict)
    init_files(prod_dict)


    while True:
        try:
            prodd = collect_if_available(prod_dict, schedule)
            if prodd is not None:
                collect_in_file(prodd, prod_dict)
            time.sleep(1)
        except:
            yellow_led.on()
            continue


run()

# collect_cg(prod_dict, data, datetime.now(), 'bitcoin')
