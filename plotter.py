import matplotlib.pyplot as plt
import csv
import numpy as np
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import time


def gas_plot(hours=24,prinT=False):
    from os import path, getcwd
    cur = getcwd()

    reader = csv.DictReader(open(cur + "/stored_data/gas.csv"))
    gas_list = list(reader)
    date = []
    low = []
    avg = []
    high = []
    skipper = 0
    for dictt in gas_list:
        if datetime.fromisoformat(dictt['date']) > datetime.now() - timedelta(hours=hours):
            skipper+=1
            if skipper > 10:
                date.append(datetime.fromisoformat(dictt['date']))
                low.append(int(dictt['low']))
                avg.append(int(dictt['average']))
                high.append(int(dictt['high']))
                skipper = 0
    plt.plot(date, avg, 'b')
    plt.plot(date, low, 'g')
    plt.plot(date, high, 'r')
    if prinT:
        print("printed now: " + str(datetime.now()))
    plt.xticks(rotation= 10)
    plt.show()

def holders_plot(prod):
    from os import path, getcwd
    cur = getcwd()

    reader = csv.DictReader(open(cur + "/stored_data/" + prod + "_data.csv"))
    gas_list = list(reader)
    price = []
    holders = []
    date = []
    high = []
    skipper = 20
    for dictt in gas_list:
        if  True:#datetime.fromisoformat(dictt['date']) :
            #skipper+=1
            if skipper > 10:
                date.append(datetime.fromisoformat(dictt['date']))
                holders.append(int(dictt['holders']))
                price.append(float(dictt['cg_price']))
                #skipper = 0
    #plt.plot(date, price, 'b')
    plt.plot(date, holders, 'g')
    #plt.plot(date, high, 'r')

    plt.xticks(rotation= 10)
    plt.show()

while True:
    gas_plot(hours=24,prinT=True)
    time.sleep(300)

holders_plot('polkastarter')