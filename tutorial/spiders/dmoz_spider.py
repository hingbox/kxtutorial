# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import TestItem
from scrapy.http import Request
# class TestSpider(scrapy.Spider):
#     # 定义爬虫的名字和需要爬取的网址
#     name = "test"
#     allowed_domains = ["www.abckg.com"]
#     start_urls = ['http://www.abckg.com/']
#     def parse(self,response):
#         for resp in response.css(".post"):
#             item = TestItem()
#             # 把获取到的内容保存到item内
#             item['href'] = resp.css('h2 a::attr(href)').extract()
#             item['title'] = resp.css('h2 a::text').extract()
#             item['content'] = resp.css('.intro p::text').extract()
#             item['view'] = response.css('h6::text').extract()[3] #得到h6元素下面的第三个信息
#             yield item
#
#         # 下面是多页面的爬取方法
#         urls = response.css('.pageinfo a::attr(href)').extract()
#         for url in urls:
#             yield Request(url, callback=self.parse)
#         categorys = response.css('.menu li a::attr(href)').extract()
#         for ct in categorys:
#             yield Request(ct, callback=self.parse)
#             yield item
#
