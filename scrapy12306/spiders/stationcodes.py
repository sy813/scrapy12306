#!/usr/bin/env python
"""
获取所有站点代码
"""
import scrapy

from scrapy.http.request import Request
from ..items import CommitItem
from ..items import StationCodeItem


class StationcodesSpider(scrapy.Spider):
    name = 'StationcodesSpider'

    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapy12306.pipelines.StationcodeSQLPipeline': 300,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy12306.middlewares.DownloaderMiddleware': 500,
        },
        'DUPEFILTER_CLASS': "scrapy12306.filter.URLTurnFilter",
        'JOBDIR': "s/Stationcodes",
    }

    def __init__(self, *a, **kw):
        super(StationcodesSpider, self).__init__(self.name, **kw)
        self.turn = a[0]
        self.logger.info("%s. this turn %d" % (self.name, self.turn))

    def start_requests(self):
        # 此url需要定期更新
        url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9027'
        yield Request(url, callback=self.parse, meta={"turn": self.turn})

    def parse(self, response):
        station_str = response.body.decode("utf-8")
        stations = station_str.split(u"@")
        for i in range(1, len(stations)):
            data = stations[i].split("|")
            item = StationCodeItem()
            item["name"] = data[1]
            item["code"] = data[2]
            item["turn"] = response.meta["turn"]

            yield item

        yield CommitItem()
