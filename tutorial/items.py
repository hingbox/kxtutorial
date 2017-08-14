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
    news_thread = scrapy.Field()#定义获取新闻的进程
    news_title = scrapy.Field()#获取新闻标题
    news_url = scrapy.Field()#获取新闻地址
    news_time = scrapy.Field()#获取新闻发布时间
    news_from = scrapy.Field()#获取发布者
    from_url = scrapy.Field()#获取。。。
    news_body = scrapy.Field()#获取新闻正文

#豆瓣的爬取内容
class DouBanItem(Item):
    title = Field()#电影标题
    score = Field()#电影评分
    content = Field()#电影信息
    info = Field()#简介
    evaluate = Field()#评价数


#博客园内容
class cnBlogsItem(Item):
    headTitle = Field()
    content = Field()
    datetime = Field()
    url = Field()

#中药知识平台内容
# class ChineseMedicineItem(Item):
#     medicineName = Field()#药名
#     overView = Field()#概述
#     basicInfo = Field()#基本信息

