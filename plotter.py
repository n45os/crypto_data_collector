import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import csv
import numpy as np
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import time


def ema(list, ema_mins):
    ema_list = [{"ema": 0, "date": datetime.fromisoformat(list[0]['date'])}]
    ema_secs = ema_mins * 60

    for i in range(len(list) - 1):
        prev = ema_list[-1]["ema"]
        time_diff = (datetime.fromisoformat(list[i]['date']) - datetime.fromisoformat(
            list[i + 1]['date'])).total_seconds()
        fractal_n = ema_secs / time_diff
        k = 2 / (fractal_n+1)
        l = list[i + 1]['average']
        ema = int(list[i + 1]['average']) *k+prev*(1 - k)
        dictt = {"ema": ema, "date": datetime.fromisoformat(list[i]['date'])}
        ema_list.append(dictt)
    return ema_list


def gas_plot(hours=24, ema_mins=460, prinT=False):
    from os import path, getcwd
    cur = getcwd()

    reader = csv.DictReader(open(cur + "/stored_data/gas.csv"))
    gas_list = list(reader)
    date = []
    low = []
    avg = []
    high = []
    low_ema = []
    avg_ema_dates = []
    avg_ema = []
    high_ema = []

    last_ema = 0
    important_list = []
    if ema_mins != 0:
        for dictt in reversed(gas_list):
            important_list.append(dictt)
            if datetime.fromisoformat(dictt['date']) < datetime.now() - timedelta(minutes=ema_mins * 50):
                important_list.reverse()
                break
        ema_dict = ema(important_list, ema_mins)
        for one in ema_dict:
            if one['date'] > datetime.now() - timedelta(hours=hours):
                avg_ema.append(one['ema'])
                avg_ema_dates.append(one['date'])


    skipper = 20
    for dictt in gas_list:
        if datetime.fromisoformat(dictt['date']) > datetime.now() - timedelta(hours=hours):
            skipper += 1
            if skipper > 20:
                date.append(datetime.fromisoformat(dictt['date']))
                low.append(int(dictt['low']))
                avg.append(int(dictt['average']))
                high.append(int(dictt['high']))
                skipper = 0
    fig, ax = plt.subplots()

    #plt.plot(avg_ema_dates, avg_ema, 'y')
    plt.plot(date, avg, 'b')
    plt.plot(date, low, 'g')
    plt.plot(date, high, 'r')
    #ax.ylabel(ylabel="gwei")
    plt.title(label=f"gas price {hours}h chart")
    myFmt = mdates.DateFormatter('%-d/%-m %H:%M')
    ax.xaxis.set_major_formatter(myFmt)
    plt.legend(handles=[mpatches.Patch(color='red', label='high'),
                        mpatches.Patch(color='blue', label='average'),
                        mpatches.Patch(color='green', label='low')])
    if prinT:
        print("printed now: " + str(datetime.now()))
    fig.autofmt_xdate()
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
        if True:  # datetime.fromisoformat(dictt['date']) :
            # skipper+=1
            if skipper > 10:
                date.append(datetime.fromisoformat(dictt['date']))
                holders.append(int(dictt['holders']))
                price.append(float(dictt['cg_price']))
                # skipper = 0
    # plt.plot(date, price, 'b')
    plt.plot(date, holders, 'g')
    # plt.plot(date, high, 'r')

    plt.xticks(rotation=10)
    plt.show()


while True:
    gas_plot(hours=8, ema_mins=0,prinT=True)
    time.sleep(300)

holders_plot('polkastarter')
