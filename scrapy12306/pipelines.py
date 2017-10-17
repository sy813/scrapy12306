# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql.cursors

from .items import CommitItem, BriefItem, BriefDeltaItem


class Scrapy12306Pipeline(object):
    def process_item(self, item, spider):
        return item


class AgencySQLPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306,
                                    user='12306',
                                    password='12306',
                                    db='12306',
                                    charset='utf8')
        self.cursor = self.conn.cursor()
        self.sql = "INSERT IGNORE INTO `agencies` (`province`, `city`,\
                        `county`, `address`, `name`, `windows`,\
                        `start`, `end`, `turn`) VALUES\
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

    def process_item(self, item, spider):
        if isinstance(item, CommitItem):
            try:
                self.conn.commit()
            except Exception as e:
                spider.logger.warning("commit fail:{}".format(e))
        else:
            try:
                self.cursor.execute(self.sql, (item["province"], item["city"],
                                               item["county"], item["address"],
                                               item["name"], item["windows"],
                                               item["start"] + "00",
                                               item["end"] + "00",
                                               item["turn"]))
            except Exception as e:
                spider.logger.warning("insert item fail".format(e))


class StationSQLPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306,
                                    user='12306',
                                    password='12306',
                                    db='12306',
                                    charset='utf8')
        self.cursor = self.conn.cursor()
        self.sql = "INSERT IGNORE INTO `stations` (`bureau`, `station`,\
                `name`, `address`, `passenger`, `luggage`,\
                `package`, `turn`) VALUES\
                (%s, %s, %s, %s, %s, %s, %s, %s)"

    def process_item(self, item, spider):
        if isinstance(item, CommitItem):
            try:
                self.conn.commit()
            except Exception as e:
                spider.logger.warning("commit fail:{}".format(e))
        else:
            try:
                self.cursor.execute(self.sql, (item["bureau"], item["station"],
                                               item["name"], item["address"],
                                               item["passenger"], item["luggage"],
                                               item["package"], item["turn"]))
            except Exception as e:
                spider.logger.warning("insert item fail".format(e))


class TrainSQLPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306,
                                    user='12306',
                                    password='12306',
                                    db='12306',
                                    charset='utf8')
        self.cursor = self.conn.cursor()
        self.brief_sql = "INSERT IGNORE INTO `train_briefs` VALUES\
                            (%s, %s, %s, %s, null, %s)"
        self.info_sql = "INSERT IGNORE INTO `train_infos` VALUES\
                            (%s, %s, %s, %s, %s, %s, %s, %s)"
        # self.turn_sql = "INSERT IGNORE INTO `turns` VALUES\
        #                     (%s, %s)"

    def process_item(self, item, spider):
        try:
            if isinstance(item, CommitItem):
                self.conn.commit()
            elif isinstance(item, BriefItem):
                self.cursor.execute(self.brief_sql, (item["code"],
                                                     item["train_no"],
                                                     item["start"], item["end"], item["turn"]))
            else:
                self.cursor.execute(self.info_sql, (item["train_no"],
                                                    item["no"],
                                                    item["station"], item["type"],
                                                    item["start_time"], item["arrive_time"],
                                                    item["stopover_time"], item["turn"]))
        except Exception as e:
            spider.logger.warning("excute sql fail:{}".format(e))


class StationcodeSQLPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306,
                                    user='12306',
                                    password='12306',
                                    db='12306',
                                    charset='utf8')
        self.cursor = self.conn.cursor()
        self.sql = "INSERT IGNORE INTO `stations_code` VALUES\
                    (%s, %s, %s)"

    def process_item(self, item, spider):
        if isinstance(item, CommitItem):
            try:
                self.conn.commit()
            except Exception as e:
                spider.logger.warning("commit fail:{}".format(e))
        else:
            try:
                self.cursor.execute(self.sql, (item["name"], item["code"], item["turn"]))
            except Exception as e:
                spider.logger.warning("insert item fail".format(e))


class TicketSQLPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306,
                                    user='12306',
                                    password='12306',
                                    db='12306',
                                    charset='utf8')
        self.cursor = self.conn.cursor()
        self.update_brief = "UPDATE `train_briefs` SET \
                            `seat_type` = %s WHERE `code` = %s AND `turn` = %s"
        self.tickets_sql = "INSERT IGNORE INTO `train_tickets` VALUES\
                            (%s, %s, %s, %s, %s, %s, %s, %s,\
                            %s, %s, %s, %s, %s, %s, %s)"

    def process_item(self, item, spider):
        try:
            if isinstance(item, CommitItem):
                self.conn.commit()
            elif isinstance(item, BriefDeltaItem):
                self.cursor.execute(self.update_brief, (item["seat_type"], item["code"], item["turn"]))
            else:
                self.cursor.execute(self.tickets_sql, (item["train_no"],
                                                       item["start"], item["end"], item["swz"],
                                                       item["tz"], item["zy"], item["ze"],
                                                       item["gr"], item["rw"], item["yw"],
                                                       item["rz"], item["yz"], item["wz"],
                                                       item["qt"], item["turn"]))
        except Exception as e:
            spider.logger.warning("excute sql fail:{}".format(e))
