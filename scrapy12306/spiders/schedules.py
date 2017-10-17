#!/usr/bin/env python
"""
获取所有车次
"""
import datetime
import json
import urllib.parse

import scrapy
from scrapy.http.request import Request
from ..items import BriefItem
from ..items import InfoItem
from ..items import CommitItem


class SchedulesSpider(scrapy.Spider):
    name = 'SchedulesSpider'

    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy12306.pipelines.TrainSQLPipeline': 300,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy12306.middlewares.DownloaderMiddleware': 500,
        },
        'DUPEFILTER_CLASS': "scrapy12306.filter.URLTurnFilter",
        'JOBDIR': "s/Schedules",
    }

    def __init__(self, *a, **kw):
        super(SchedulesSpider, self).__init__(self.name, **kw)
        self.turn = a[0]
        self.logger.info("%s. this turn %d" % (self.name, self.turn))

    def start_requests(self):
        url = "https://kyfw.12306.cn/otn/queryTrainInfo/getTrainName?"

        t = (datetime.datetime.now() + datetime.timedelta(days=3)).strftime("%Y-%m-%d")
        params = {"date": t}

        s_url = url + urllib.parse.urlencode(params)
        self.logger.debug("start url " + s_url)
        yield Request(s_url, callback=self.parse, meta={"t": t, "turn": self.turn})

    def parse(self, response):
        datas = json.loads(response.body.decode("utf-8"))
        url = "https://kyfw.12306.cn/otn/czxx/queryByTrainNo?"
        for data in datas["data"]:
            item = BriefItem()
            briefs = data["station_train_code"].split("(")
            item["train_no"] = data["train_no"]
            item["code"] = briefs[0]
            briefs = briefs[1].split("-")
            item["start"] = briefs[0]
            item["end"] = briefs[1][:-1]
            item["turn"] = response.meta["turn"]
            yield item

            params = u"train_no=" + data[
                "train_no"] + u"&from_station_telecode=BBB&to_station_telecode=BBB&depart_date=" + response.meta["t"]

            yield Request(url + params, callback=self.parse_train_schedule,
                          meta={"train_no": data["train_no"], "turn": response.meta["turn"]})

    def parse_train_schedule(self, response):
        stations = json.loads(response.body.decode("utf-8"))

        datas = stations["data"]["data"]
        size = len(datas)
        for i in range(0, size):
            data = datas[i]

            info = InfoItem()
            info["train_no"] = response.meta["train_no"]
            info["no"] = int(data["station_no"])
            info["station"] = data["station_name"]
            info["turn"] = response.meta["turn"]

            if i == 0:
                info["type"] = 0
            elif i == size - 1:
                info["type"] = 1
            else:
                info["type"] = 2

            if data["start_time"] != "----":
                info["start_time"] = data["start_time"] + ":00"
            else:
                info["start_time"] = None

            if data["arrive_time"] != "----":
                info["arrive_time"] = data["arrive_time"] + ":00"
            else:
                info["arrive_time"] = None

            if data["stopover_time"] != "----":
                info["stopover_time"] = data["stopover_time"]
            else:
                info["stopover_time"] = None

            yield info
        yield CommitItem()
