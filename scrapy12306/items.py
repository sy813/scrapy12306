# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CommitItem(scrapy.Item):
    pass


class TurnItem(scrapy.Item):
    id = scrapy.Field()
    mark = scrapy.Field()


class AgencyItem(scrapy.Item):
    province = scrapy.Field()
    city = scrapy.Field()
    county = scrapy.Field()
    address = scrapy.Field()
    name = scrapy.Field()
    windows = scrapy.Field()
    start = scrapy.Field()
    end = scrapy.Field()
    turn = scrapy.Field()


class StationItem(scrapy.Item):
    bureau = scrapy.Field()
    station = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    passenger = scrapy.Field()
    luggage = scrapy.Field()
    package = scrapy.Field()
    turn = scrapy.Field()


class BriefItem(scrapy.Item):
    code = scrapy.Field()
    train_no = scrapy.Field()
    start = scrapy.Field()
    end = scrapy.Field()
    turn = scrapy.Field()


class InfoItem(scrapy.Item):
    train_no = scrapy.Field()
    no = scrapy.Field()
    station = scrapy.Field()
    type = scrapy.Field()
    start_time = scrapy.Field()
    arrive_time = scrapy.Field()
    stopover_time = scrapy.Field()
    turn = scrapy.Field()


class BriefDeltaItem(scrapy.Item):
    code = scrapy.Field()
    seat_type = scrapy.Field()
    turn = scrapy.Field()


class StationCodeItem(scrapy.Item):
    name = scrapy.Field()
    code = scrapy.Field()
    turn = scrapy.Field()


class TicketItem(scrapy.Item):
    train_no = scrapy.Field()
    start = scrapy.Field()
    end = scrapy.Field()
    swz = scrapy.Field()
    tz = scrapy.Field()
    zy = scrapy.Field()
    ze = scrapy.Field()
    gr = scrapy.Field()
    rw = scrapy.Field()
    yw = scrapy.Field()
    rz = scrapy.Field()
    yz = scrapy.Field()
    wz = scrapy.Field()
    qt = scrapy.Field()
    turn = scrapy.Field()
