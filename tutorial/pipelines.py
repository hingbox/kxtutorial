# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
class TutorialPipeline(object):
    def __init__(self):
        self.file = codecs.open('D:\\PycharmProjects\\data1.json', mode='wb', encoding='utf-8')  # 数据存储到data.json

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line.decode("unicode_escape"))
        return item

#网易新闻 mongodb中
from spiders.store import NewsDB
class Tech163Pipeline(object):
    def process_item(self, item, spider):
        if spider.name != "news":
            return item
        if item.get("news_thread", None) is None:
            return item
        spec = {"news_thread": item["news_thread"]}
        NewsDB.new.update(spec, {"$set": dict(item)}, upsert=True)
        return None

#网易新闻保存xml中(暂时有问题)
from scrapy import signals
from scrapy.exporters import XmlItemExporter
# 数据以xml保存
class Tech163XmlPipeline(object):
    def __init__(self):
        pass

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        self.file = open('D:\\PycharmProjects\\new_test.xml', 'wb')
        self.expoter = XmlItemExporter(self.file)
        self.expoter.start_exporting()

    def spider_closed(self, spider):
        self.expoter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.expoter.export_item(item)
        return item


#豆瓣top250
from scrapy.conf import settings
import pymongo
class DouBanPipeline(object):
    def __init__(self):
        # 获取setting主机名、端口号和数据库名
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']

        # pymongo.MongoClient(host, port) 创建MongoDB链接
        client = pymongo.MongoClient(host=host, port=port)
        # 指向指定的数据库
        mdb = client[dbname]
        # 获取数据库里存放数据的表名
        self.post = mdb[settings['MONGODB_DOCNAME']]
    def process_item(self, item, spider):
        data = dict(item)
        # 向指定的表里添加数据
        self.post.insert(data)
        return item

