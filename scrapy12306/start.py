#!/usr/bin/env python
"""
持续化运行爬虫脚本
"""
import os
import sys
import time
import datetime

import pymysql.cursors

project_path = os.path.dirname(os.path.abspath(__file__ + "/.."))
sys.path.insert(0, project_path)

# import the spiders you want to run
from scrapy12306.spiders.agencies import AgenciesSpider
from scrapy12306.spiders.stations import StationsSpider
from scrapy12306.spiders.stationcodes import StationcodesSpider
from scrapy12306.spiders.schedules import SchedulesSpider
from scrapy12306.spiders.tickets import TicketsSpider

# scrapy api imports
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

settings = get_project_settings()

crawler = CrawlerProcess(settings)


def sleep(secs):
    d = defer.Deferred()
    reactor.callLater(secs, d.callback, None)
    return d


@defer.inlineCallbacks
def crawl():
    conn = pymysql.connect(host='localhost', port=3306,
                           user='12306',
                           password='12306',
                           db='12306',
                           charset='utf8')

    agencie_count = 30
    stations_count = 30
    stationcodes_count = 30
    schedules_count = 5
    tickets_count = 1
    first = True

    last_turn = -1
    while True:
        n = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        s = time.time()
        turn = int(s / 86400)

        if turn == last_turn:
            sleep(5)
            continue

        print("new turn", turn, n)
        last_turn = turn

        with conn.cursor() as cursor:
            cursor.execute("INSERT IGNORE INTO `turns` VALUES (%s, %s)", (turn, n))
        conn.commit()

        if first or turn % agencie_count == 0:
            yield crawler.crawl(AgenciesSpider, turn)
        if first or turn % stations_count == 0:
            yield crawler.crawl(StationsSpider, turn)
        if first or turn % stationcodes_count == 0:
            yield crawler.crawl(StationcodesSpider, turn)
        if first or turn % schedules_count == 0:
            yield crawler.crawl(SchedulesSpider, turn)
        if first or turn % tickets_count == 0:
            yield crawler.crawl(TicketsSpider, turn)

        first = False
        e = time.time()
        left = int(86400 - e + s)

        if left > 0:
            print("sleep", left)
            sleep(left)

    print("crawler over")


crawl()
crawler.start()
