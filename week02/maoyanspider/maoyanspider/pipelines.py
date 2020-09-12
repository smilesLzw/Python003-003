# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
import pymysql


class MaoyanspiderPipeline:
    def process_item(self, item, spider):
        return item


class MaoyanspiderMysqlPipeline(object):
    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(host=crawler.settings.get('HOST'),
                   user=crawler.settings.get('USER'),
                   password=crawler.settings.get('PASSWORD'),
                   db=crawler.settings.get('DB'))

    def open_spider(self, spider):
        self.conn = pymysql.connect(self.host, self.user, self.password,
                                    self.db)

    def process_item(self, item, spider):
        name = item['name']
        categories = item['categories']
        published_at = item['published_at']

        sql = "INSERT INTO doubanmovie (name, categories, published_at) VALUES (%s, %s, %s)"
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, (name, categories, published_at))
        except:
            self.conn.rollback()
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()
