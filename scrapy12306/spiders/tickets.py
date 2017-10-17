#!/usr/bin/env python
"""
获取余票信息
"""
import datetime
import json

import pymysql.cursors

import scrapy
from scrapy.http.request import Request
from ..items import BriefDeltaItem
from ..items import TicketItem
from ..items import CommitItem


class TicketsSpider(scrapy.Spider):
    name = 'TicketsSpider'

    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy12306.pipelines.TicketSQLPipeline': 300,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy12306.middlewares.DownloaderMiddleware': 500,
        },
        'DUPEFILTER_CLASS': "scrapy12306.filter.URLTurnFilter",
        'JOBDIR': "s/Tickets",
    }

    def __init__(self, *a, **kw):
        super(TicketsSpider, self).__init__(self.name, **kw)
        self.turn = a[0]
        self.logger.info("%s. this turn %d" % (self.name, self.turn))

    def start_requests(self):
        url = "https://kyfw.12306.cn/otn/leftTicket/query?"
        f = 'leftTicketDTO.'
        t = (datetime.datetime.now() + datetime.timedelta(days=3)).strftime("%Y-%m-%d")

        stationcodes = TicketsSpider.fetch_stationcodes()
        routes = TicketsSpider.fetch_routes()

        for s in routes:
            if s in stationcodes:
                code_s = stationcodes[s]
            else:
                self.logger.warning("code miss " + s)
                continue
            for e in routes[s]:
                if e in stationcodes:
                    code_e = stationcodes[e]
                else:
                    self.logger.warning("code miss " + e)
                    continue

                params = f + "train_date=" + t + "&" + f + "from_station=" + code_s + "&" + f + "to_station=" + code_e + "&purpose_codes=ADULT"
                s_url = url + params
                self.logger.debug("start url " + s_url)
                yield Request(s_url, callback=self.parse, meta={"t": t, "turn": self.turn})

    @staticmethod
    def fetch_routes():
        conn = pymysql.connect(host='localhost',
                               port=3306,
                               user='12306',
                               passwd='12306',
                               db='12306',
                               charset='utf8')

        select = "SELECT * FROM train_infos"

        schedules = {}
        with conn.cursor() as cursor:
            cursor.execute(select)
            for results in cursor.fetchall():
                if results[0] not in schedules:
                    schedules[results[0]] = {results[1]: results[2]}
                else:
                    schedules[results[0]][results[1]] = results[2]

        routes = {}
        for key in schedules:
            route = schedules[key]

            seq = sorted(route)
            len1 = len(seq)
            for i in range(0, len1):
                if route[seq[i]] not in routes:
                    tmp = set()
                    routes[route[seq[i]]] = tmp
                else:
                    tmp = routes[route[seq[i]]]
                for j in range(i + 1, len1):
                    tmp.add(route[seq[j]])
        return routes

    @staticmethod
    def fetch_stationcodes():
        conn = pymysql.connect(host='localhost',
                               port=3306,
                               user='12306',
                               passwd='12306',
                               db='12306',
                               charset='utf8')

        select = "SELECT * FROM stations_code"

        stationcodes = {}
        with conn.cursor() as cursor:
            cursor.execute(select)
            for results in cursor.fetchall():
                if results not in stationcodes:
                    stationcodes[results[0]] = results[1]
                else:
                    pass
        return stationcodes

    def parse(self, response):
        datas = json.loads(response.body.decode('utf-8'))

        results = datas["data"]["result"]

        if not results:
            self.logger.info("there is no result " + response.meta["s"] + " " + response.meta["e"])
            return

        for result in results:
            data = result.split("|")

            deltaItem = BriefDeltaItem()

            deltaItem["code"] = data[3]
            deltaItem["seat_type"] = data[35]
            deltaItem["turn"] = response.meta["turn"]
            yield deltaItem

            item = TicketItem()
            item["train_no"] = data[2]
            item["start"] = data[4]
            item["end"] = data[7]
            item["turn"] = response.meta["turn"]

            item["swz"] = data[32]
            if not item["swz"]:
                item["swz"] = "-"
            item["tz"] = data[25]
            if not item["tz"]:
                item["tz"] = "-"
            item["zy"] = data[31]
            if not item["zy"]:
                item["zy"] = "-"
            item["ze"] = data[30]
            if not item["ze"]:
                item["ze"] = "-"
            item["gr"] = data[21]
            if not item["gr"]:
                item["gr"] = "-"
            item["rw"] = data[23]
            if not item["rw"]:
                item["rw"] = "-"
            item["yw"] = data[28]
            if not item["yw"]:
                item["yw"] = "-"
            item["rz"] = data[24]
            if not item["rz"]:
                item["rz"] = "-"
            item["yz"] = data[29]
            if not item["yz"]:
                item["yz"] = "-"
            item["wz"] = data[26]
            if not item["wz"]:
                item["wz"] = "-"
            item["qt"] = data[22]
            if not item["qt"]:
                item["qt"] = "-"
            yield item
        yield CommitItem()
