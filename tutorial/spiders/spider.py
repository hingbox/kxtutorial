# -*- coding: utf-8 -*-
#豆瓣的爬取规则
import scrapy
import re
from tutorial.items import DouBanItem
class DouBanSpider(scrapy.Spider):
    name = "douban"
    allowed_domains = ["movie.douban.com"]
    start = 0
    url = 'https://movie.douban.com/top250?start ='
    end = '&filter='
    start_urls = [url + str(start) + end]
    def parse(self, response):
        item = DouBanItem()
        movies = response.xpath("//div[@class='info']")
        for each in movies:
            title = each.xpath('div[@class="hd"]/a/span[@class="title"]/text()').extract()
            content = each.xpath('div[@class ="bd"]/p/text()').extract()
            score = each.xpath('div[@class ="bd"]/div[@class ="star"]/span[@class ="rating_num"]/text()').extract()
            info = each.xpath('div[@class ="bd"]/p[@class ="quote"]/span/text()').extract()
            item['title'] = title[0]
            # 以;作为分隔，将content列表里所有元素合并成一个新的字符串
            item['content'] = ';'.join(content)
            item['score'] = score[0]
            item['info'] = info[0]
            # 提交item
            yield item


        if self.start <= 225:
            self.start += 25
            yield scrapy.Request(self.url + str(self.start) + self.end, callback=self.parse)

#网易新闻的爬取规则
from tutorial.items import Tech163Item
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider,Rule
class Tech163Spider(CrawlSpider):
    name = "news"#该名字必须是唯一的。不可以为不同的Spider设置相同的名字。
    allowed_domains = ["tech.163.com"]#需要对应网易新闻的类别
    start_urls = ['http://tech.163.com/']#包含了Spider在启动时进行爬取的URL列表。因此，第一个被获取的页面将是其中之一。后续的url则是从出事的url获取到的数据中提取。可以使用正则表达式定义和过滤需要进行跟进的链接。
    rules = (
        Rule(
            LinkExtractor(allow=r"/17/07\d+/\d+/*"),#这里需根据具体年份考虑 /17/是指年份 /07\d+/ 是指月份 这个可参考一个网易新闻的地址：http://tech.163.com/17/0711/07/CP20CRUC00097U7R.html
            # 代码中的正则/15/06\d+/\d+/*的含义是大概是爬去/17/07开头并且后面是数字/数字/任何格式/的新闻
            callback="parse_news",
            follow=True
            # follow=ture定义了是否再爬到的结果上继续往后爬
        ),
    )

    def parse_news(self, response):#是spider的一个方法。被调用时，每个初始url完成下载后生成的response对象将会作为唯一的参数传递给该函数。该方法负责解析返回的数据、提取数据（生成item）以及生成需要进一步处理的url的response对象。
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

        source = response.xpath("//div[@class='post_time_source']/text()").extract()
        if source:
            item['news_time'] = source[0]

    def get_news_from(self, response, item):
        news_from = response.xpath("//div[@class='ep-source cDGray']/span[@class='left']/text()").extract()
        if news_from:
            item['news_from'] = news_from[0]

    def get_from_url(self, response, item):
        from_url = response.xpath("//div[@class='ep-source cDGray']/a/@href").extract()
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

#博客园爬取规则
import sys
import string
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from tutorial.items import cnBlogsItem
sys.stdout = open('D:\\PycharmProjects\\output.txt','w') #将打印信息输出在相应的位置下
add = 0


def change_word(s):  # 把表中的字符串转化到中文显示
    print s
    sum = 0
    for i in s[0]:
        sum += 1
    ss2 = ''

    count = 0
    for i in range(0, sum):
        # 对 /u2014处理
        if (s[0][i] == u'\u2014'):
            continue
        ss2 += s[0][i]

    s = ss2
    print s
from scrapy.selector import HtmlXPathSelector
class cnBlogsSpider(CrawlSpider):
    name = "huhu"
    allowed_domain = ["cnblogs.com"]
    start_urls = [
        "http://www.cnblogs.com/huhuuu",
    ]
    rules = (
        # 提取匹配 huhuuu/default.html\?page\=([\w]+) 的链接并跟进链接(没有callback意味着follow默认为True)
        Rule(SgmlLinkExtractor(allow=('huhuuu/default.html\?page\=([\w]+)',), )),
        # 提取匹配 'huhuuu/p/' 的链接并使用spider的parse_item方法进行分析
        Rule(SgmlLinkExtractor(allow=('huhuuu/p/',)), callback='parse_item'),
        Rule(SgmlLinkExtractor(allow=('huhuuu/archive/',)), callback='parse_item'),  # 以前的一些博客是archive形式的所以
    )

    # rules = (
    #
    #     Rule(SgmlLinkExtractor(allow=('sitehome/p/[0-9]+',), )),
    #
    #     Rule(SgmlLinkExtractor(allow=('[^\s]+/p/',)), callback='parse_item'),
    #
    # )
    def parse_item(self,response):
        global add#用于统计博文的数量
        print add
        add += 1
        # sel = Selector(response)
        sel = HtmlXPathSelector(response)
        items = []
        item = cnBlogsItem()
        item['headTitle'] = sel.xpath('/html/head/title/text()').extract()#观察网页对应得html源码
        item['url'] = response
        item['datetime'] = sel.xpath("//div[@class='posthead']/span[@id='post-date']/text()").extract()
        item['content'] = sel.xpath("//div[@id='cnblogs_post_body']/p/text()").extract()
        #         for data in item['content']:
        # strTmp = ''
        #     for i in data:
        #         if (i != u'\xa0'):  # '\xa0'这个字符编译器不能识别，所以处理掉
        #             # print i
        #             strTmp += i
        #     print strTmp

        print item
        items.append(item)
        return items
