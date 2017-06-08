#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
import sqlite3
import json

app = Flask(__name__)
coins=["doge", "met", "plc", "jbc", "skt", "tfc"]
coins_name={"doge":u"狗狗币", "met":u"美通币", "plc":u"保罗币", "jbc":u"聚宝币",
    "skt":u"鲨之信", "tfc":u"传送币", "mtc":u"侯宝币",
    "ifc":u"无限币", "dnc":u"暗网币", "xrp":u"瑞波币", "max":u"最大币"}
def get_coin_state_by_period(period):
    conn = sqlite3.connect('coins.db')
    coins_stat={}

    cursor = conn.execute("select name, price from coins group by name")
    for row in cursor:
        coins_stat[row[0]]= {"price":row[1], "max":0, "min":0}
    cursor = conn.execute("select name, max(price), min(price) from coins group by name")
    for row in cursor:
        coins_stat[row[0]]["max"] = row[1]
        coins_stat[row[0]]["min"] = row[2]

    conn.close()
    return coins_stat


@app.route('/stat')
def coin_stat():
    stats = get_coin_state_by_period("1h")
    coins = []
    for name in stats.keys():
        coins.append({"name":coins_name[name], "price":stats[name]["price"],
            "percent":float('%0.2f' % (((stats[name]["price"] * 100)/stats[name]["min"]) - 100)), 
            "max":stats[name]["max"], "min":stats[name]["min"]})
    return render_template("stat.html", coins=coins)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True)
