# -*- coding: utf-8 -*-
#这个是抓取文件 主要用xpath指定抓取规则(网易新闻)
import scrapy
import re
from tutorial.items import Tech163Item
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider,Rule
class Tech163Spider(CrawlSpider):
    name = "news"
    allowed_domains = ["tech.163.com"]
    start_urls = ['http://tech.163.com/']
    rules = (
        Rule(
            LinkExtractor(allow=r"/15/06\d+/\d+/*"),
            # 代码中的正则/15/06\d+/\d+/*的含义是大概是爬去/15/06开头并且后面是数字/数字/任何格式/的新闻
            callback="parse_news",
            follow=True
            # follow=ture定义了是否再爬到的结果上继续往后爬
        ),
    )

    def parse_news(self, response):
        item = Tech163Item()
        item['news_thread'] = response.url.strip().split('/')[-1][:-5]
        self.get_title(response, item)
        self.get_source(response, item)
        self.get_url(response, item)
        self.get_news_from(response, item)
        self.get_from_url(response, item)
        self.get_text(response, item)
        return item

    def get_title(self, response, item):
        title = response.xpath("/html/head/title/text()").extract()
        if title:
            item['news_title'] = title[0][:-5]

    def get_source(self, response, item):
        source = response.xpath("//div[@class='ep-time-soure cDGray']/text()").extract()
        if source:
            item['news_time'] = source[0][9:-5]

    def get_news_from(self, response, item):
        news_from = response.xpath("//div[@class='ep-time-soure cDGray']/a/text()").extract()
        if news_from:
            item['news_from'] = news_from[0]

    def get_from_url(self, response, item):
        from_url = response.xpath("//div[@class='ep-time-soure cDGray']/a/@href").extract()
        if from_url:
            item['from_url'] = from_url[0]

    def get_text(self, response, item):
        news_body = response.xpath("//div[@id='endText']/p/text()").extract()
        if news_body:
            item['news_body'] = news_body

    def get_url(self, response, item):
        news_url = response.url
        if news_url:
            item['news_url'] = news_url