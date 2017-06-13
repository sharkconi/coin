#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
import sqlite3
import json
import datetime
import MySQLdb



app = Flask(__name__)
coins=["doge", "met", "plc", "jbc", "skt", "tfc"]
coins_name={"doge":u"狗狗币", "met":u"美通币", "plc":u"保罗币", "jbc":u"聚宝币",
    "skt":u"鲨之信", "tfc":u"传送币", "mtc":u"侯宝币",
    "ifc":u"无限币", "dnc":u"暗网币", "xrp":u"瑞波币", "max":u"最大币",
    "bts":u"比特股", "rss":u"红贝壳", "etc":u"以太经典"}

db = MySQLdb.connect("localhost", "root", "123456", "coins")
cursor = db.cursor()

def get_coin_state_by_period():
    coins_stat={}

    cursor.execute("select name, price, amount from coins group by name")
    for row in cursor.fetchall():
        coins_stat[row[0]]= {"price":row[1], "max":0, "min":0, "60min":0, "15min":0, "30min":0,
				"volumn":row[2]}

    cursor.execute("select name, max(price), min(price) from coins group by name")
    for row in cursor.fetchall():
        coins_stat[row[0]]["max"] = row[1]
        coins_stat[row[0]]["min"] = row[2]

    sql = 'select name, max(price), min(price) from coins where time > "%s" group by name' % \
            (datetime.datetime.now() -datetime.timedelta(minutes=60))
    cursor.execute(sql)
    for row in cursor.fetchall():
        coins_stat[row[0]]["60min"] = row [2]

    sql = 'select name, max(price), min(price) from coins where time > "%s" group by name' % \
            (datetime.datetime.now() -datetime.timedelta(minutes=15))
    cursor.execute(sql)
    for row in cursor.fetchall():
        coins_stat[row[0]]["15min"] = row [2]

    sql = 'select name, max(price), min(price) from coins where time > "%s" group by name' % \
            (datetime.datetime.now() -datetime.timedelta(minutes=30))
    cursor.execute(sql)
    for row in cursor.fetchall():
        coins_stat[row[0]]["30min"] = row [2]

    return coins_stat

@app.route('/stat')
def coin_stat():
    stats = get_coin_state_by_period()
    coins = []
    for name in stats.keys():
        coins.append({"name":coins_name[name], "price":float('%0.4f' % (stats[name]["price"])),
			"volumn":float('%0.2f' % (stats[name]["volumn"]/1000000)),
            "percent":float('%0.2f' % (((stats[name]["price"] * 100)/stats[name]["min"]) - 100)),
            "max":float('%0.2f' % (stats[name]["max"])), "min":float('%.2f' % (stats[name]["min"])),
			"60min":float('%0.2f' % (stats[name]["60min"])), 
			"30min":float('%0.2f' % (stats[name]["30min"])),
			"15min":float('%0.2f' % (stats[name]["15min"])),
            "60minp":float('%0.2f' % (((stats[name]["price"] * 100)/stats[name]["60min"]) - 100)),
            "15minp":float('%0.2f' % (((stats[name]["price"] * 100)/stats[name]["15min"]) - 100)),
            "30minp":float('%0.2f' % (((stats[name]["price"] * 100)/stats[name]["30min"]) - 100))})
    return render_template("stat.html", coins=coins)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True)
