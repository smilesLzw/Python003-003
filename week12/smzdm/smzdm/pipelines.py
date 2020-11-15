# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging

import pymysql
from itemadapter import ItemAdapter


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')



class SmzdmPipeline:
    def process_item(self, item, spider):
        return item


class MysqlPipeline:
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
                   db=crawler.settings.get('DB'),
                   )

    def open_spider(self, spider):
        self.conn = pymysql.connect(self.host,
                                    self.user,
                                    self.password,
                                    self.db)

    def process_item(self, item, spider):
        nickname = item['nickname']
        comment = item['comment']
        comment_time = item['comment_time']

        sql = "INSERT INTO phone_comment (nickname, comment, comment_time) VALUES (%s, %s, %s)"
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, (nickname, comment, comment_time))
        except:
            self.conn.rollback()
        self.conn.commit()
        logging.info('data save successful!')


    def close_spider(self, spider):
        self.conn.close()