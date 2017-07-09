# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item,Field
class TutorialItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class TestItem(Item):
    id = Field()
    title = Field()
    href = Field()
    content = Field()
    view = Field()

class Tech163Item(Item):
    news_thread = scrapy.Field()
    news_title = scrapy.Field()
    news_url = scrapy.Field()
    news_time = scrapy.Field()
    news_from = scrapy.Field()
    from_url = scrapy.Field()
    news_body = scrapy.Field()

#豆瓣的爬取内容
class DouBanItem(Item):
    # 电影标题
    title = Field()
    # 电影评分
    score = Field()
    # 电影信息
    content = Field()
    # 简介
    info = Field()
    #评价数
    evaluate = Field()

