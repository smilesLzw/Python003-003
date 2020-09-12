import scrapy
from scrapy.selector import Selector

from maoyanspider.items import MaoyanspiderItem


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com/']

    def start_requests(self):
        url = 'https://maoyan.com/films?showType=3'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = MaoyanspiderItem()
        movie_infos = Selector(
            response=response).xpath('//div[@class="movie-hover-info"]')[0:10]
        for movie in movie_infos:
            name = movie.xpath('./div[1]/span/text()').extract()
            categories = movie.xpath(
                'normalize-space(./div[2]/span[./text()="类型:"]/following::text()[1])'
            ).extract()
            published_at = movie.xpath(
                'normalize-space(./div[4]/span[./text()="上映时间:"]/following::text()[1])'
            ).extract()
            item['name'] = name
            item['categories'] = categories
            item['published_at'] = published_at
            yield item