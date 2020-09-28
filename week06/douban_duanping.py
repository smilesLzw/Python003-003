import re
import time
import json
import logging

from lxml import etree

from download import download
from ezpymysql import Connection

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')


# 解析网页，获取星级和短评
def parse_page(html):
    data = []
    rate_dict = {
        '很差': 1,
        '较差': 2,
        '还行': 3,
        '推荐': 4,
        '力荐': 5,
    }
    selector = etree.HTML(html)
    comment_items = selector.xpath(
        '//div[@id="comments"]/div[@class="comment-item "]')
    for comment_item in comment_items:
        nickname = comment_item.xpath('./div[2]/h3/span[2]/a/text()')[0]
        rate = comment_item.xpath('./div[2]/h3/span[2]/span[2]/@title')[0]
        star = rate_dict.get(rate, 0)
        comment = comment_item.xpath(
            './div[@class="comment"]/p/span[@class="short"]/text()')[0]
        comment_time = comment_item.xpath(
            './div[2]/h3/span[2]/span[@class="comment-time "]/@title')[0]
        comment_time = re.search(
            '(\d{4}-\d{2}-\d{2})',
            comment_time).group(1) if comment_time and re.search(
                '\d{4}-\d{2}-\d{2}', comment_time) else None
        item = {
            'nickname': nickname,
            'star': star,
            'comment': comment,
            'comment_time': comment_time
        }
        logging.info('Get data %s', item)
        data.append(item)

    return data


# 加载配置文件
def load_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config


# 存储数据到 Mysql
def save_data(data, config):
    db = Connection(config['db_host'], config['db_table'], config['db_user'],
                    config['db_password'])
    for item in data:
        last_id = db.table_insert('index_commentinfo', item)
        if last_id:
            logging.info('data saved successful!')
        else:
            logging.error('error occurred while save data %s',
                          item,
                          exc_info=True)
    logging.info('All data saved!')


if __name__ == '__main__':
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'Cookie':
        '__gads=ID=3916380c0cada069:T=1563846034:S=ALNI_MYYbmjciV-lv7A1sieZjr76-2O-tQ; _vwo_uuid_v2=D28D1A7949B635BF1C473BC94B29D3110|497943000feac3205a3c7c9a145f8af4; douban-fav-remind=1; gr_user_id=5d89f0c9-8ff4-43a6-8783-9fd5ebba92a6; viewed="3354490_26880667_30813632"; __utmv=30149280.17864; bid=C_6w0NzMlsc; __yadk_uid=lGW70NrTSlOXQXhLDrnZ9wQNxH2N7hYS; ll="118349"; _ga=GA1.2.1804573732.1563846027; push_noty_num=0; push_doumail_num=0; ct=y; __utmc=30149280; __utmc=223695111; ap_v=0,6.0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1601281174%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=30149280.1804573732.1563846027.1601276614.1601281175.41; __utmb=30149280.0.10.1601281175; __utmz=30149280.1601281175.41.12.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=223695111.2029627377.1597377049.1601276614.1601281175.25; __utmb=223695111.0.10.1601281175; __utmz=223695111.1601281175.25.11.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_id.100001.4cf6=4ca5c703e57e611e.1597377049.24.1601281181.1601276614.'
    }
    urls = [
        f'https://movie.douban.com/subject/30128916/comments?start={page * 20}&limit=20&status=P&sort=new_score'
        for page in range(5)
    ]

    comment_data = []
    for url in urls:
        _, html, _ = download(url, headers=headers)
        time.sleep(3)
        data = parse_page(html)
        comment_data += data

    config = load_config()
    save_data(comment_data, config)