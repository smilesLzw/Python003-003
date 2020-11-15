from datetime import datetime

import scrapy
from scrapy.selector import Selector

from smzdm.items import SmzdmItem


class PhoneSpider(scrapy.Spider):
    name = 'phone'
    allowed_domains = ['smzdm.com']
    start_urls = ['https://www.smzdm.com/fenlei/zhinengshouji/h5c4s0f0t0p1/#feed-main/']

    # 抓取首页数据
    def start_requests(self):
        url = 'https://www.smzdm.com/fenlei/zhinengshouji/h5c4s0f0t0p1/#feed-main/'
        yield scrapy.Request(url=url, callback=self.scrape_index)

    # 获取首页前十产品链接
    def scrape_index(self, response):
        atags = Selector(response=response).xpath('//h5[@class="feed-block-title"]/a/@href').getall()[:10]
        for atag in atags:
            yield scrapy.Request(url=atag, callback=self.parse_detail)

    # 获取用户昵称及评论，实现自动翻页
    def parse_detail(self, response):
        item = SmzdmItem()
        li_box = Selector(response=response).xpath('//div[@id="commentTabBlockNew"]/ul/li[@class="comment_list"]')
        for li in li_box:
            nickname = li.xpath('./div[2]/div/a/span/text()').get()
            comment = li.xpath(
                './div[2]/div[@class="comment_conWrap"]/div/p/span/text()').get().strip()
            comment_time = li.xpath('./div[2]/div/div/meta/@content').get()
            comment_time = comment_time if comment_time else datetime.now().strftime('%Y-%m-%d')
            item['nickname'] = nickname
            item['comment'] = comment
            item['comment_time'] = comment_time
            yield item
        next_comment_url = Selector(response=response).xpath('//li[@class="pagedown"]/a/@href').get()
        if next_comment_url is not None:
            yield scrapy.Request(url=next_comment_url, callback=self.parse_detail)

    # def parse(self, response):
    #     pass
