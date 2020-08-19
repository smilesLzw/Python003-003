import scrapy
from urllib.parse import urljoin
from scrapy.selector import Selector

from spiders.items import SpidersItem


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/films?showType=3']

    # def parse(self, response):
    #     pass

    def start_requests(self):
        url = 'https://maoyan.com/films?showType=3'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        BASE_URL = 'https://maoyan.com'
        hrefs = Selector(response=response).xpath(
            '//div[@class="movie-item film-channel"]/a/@href').extract()[0:10]
        for href in hrefs:
            detail_url = urljoin(BASE_URL, href)
            yield scrapy.Request(url=detail_url, callback=self.parse2)

    def parse2(self, response):
        item = SpidersItem()
        movie_brief = Selector(
            response=response).xpath('//div[@class="movie-brief-container"]')
        name = movie_brief.xpath('./h1/text()').extract()
        categories = movie_brief.xpath('./ul/li/a/text()').extract()
        published_at = movie_brief.xpath('./ul/li[last()]/text()').extract()
        item['name'] = name
        item['categories'] = [category.strip() for category in categories]
        item['published_at'] = published_at
        yield item
