#!/usr/bin/env python
"""
获取所有客运站点
"""

import scrapy
from scrapy.http.request import Request
from ..items import StationItem
from ..items import CommitItem


class StationsSpider(scrapy.Spider):
    name = 'StationsSpider'

    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy12306.pipelines.StationSQLPipeline': 300,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy12306.middlewares.DownloaderMiddleware': 500,
        },
        'DUPEFILTER_CLASS': "scrapy12306.filter.URLTurnFilter",
        'JOBDIR': "s/Stations",
    }

    def __init__(self, *a, **kw):
        super(StationsSpider, self).__init__(self.name, **kw)
        self.turn = a[0]
        self.logger.info("%s. this turn %d" % (self.name, self.turn))

    def start_requests(self):
        yield Request("http://www.12306.cn/mormhweb/kyyyz/", callback=self.parse, meta={"turn": self.turn})

    def parse(self, response):
        names = response.css("#secTable > tbody > tr > td::text").extract()
        sub_urls = response.css("#mainTable td.submenu_bg > a::attr(href)").extract()
        for i in range(0, len(names)):
            sub_url1 = response.url + sub_urls[i * 2][2:]
            yield Request(sub_url1, callback=self.parse_station,
                          meta={'bureau': names[i], 'station': True, "turn": response.meta["turn"]})

            sub_url2 = response.url + sub_urls[i * 2 + 1][2:]
            yield Request(sub_url2, callback=self.parse_station,
                          meta={'bureau': names[i], 'station': False, "turn": response.meta["turn"]})

    def parse_station(self, response):
        datas = response.css("table table tr")
        size = len(datas)
        if size <= 2:
            return
        for i in range(0, size):
            if i < 2:
                continue
            infos = datas[i].css("td::text").extract()

            item = StationItem()
            item["bureau"] = response.meta["bureau"]
            item["station"] = response.meta["station"]
            item["name"] = infos[0]
            item["address"] = infos[1]
            item["passenger"] = infos[2].strip() != ""
            item["luggage"] = infos[3].strip() != ""
            item["package"] = infos[4].strip() != ""
            item["turn"] = response.meta["turn"]
            yield item
        yield CommitItem()
