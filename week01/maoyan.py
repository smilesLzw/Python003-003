import logging
import re
from time import sleep

import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import pandas as pd

BASE_URL = 'https://maoyan.com'
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')


def scrape_page(url):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
    cookie = '__mta=45920667.1597662284150.1597836998612.1597841990228.12; uuid_n_v=v1; uuid=72E709B0E07911EAB722873DCAC2C14F687BE9A394AD42508A800383605B0DE6; _lxsdk_cuid=173fc17c8efc8-07f1cf4b6bf1b8-f7d1d38-144000-173fc17c8efc8; _lxsdk=72E709B0E07911EAB722873DCAC2C14F687BE9A394AD42508A800383605B0DE6; mojo-uuid=fd208dd91051ff956b177d764af8fa21; _csrf=e8ea6f56ad8bacd0fdb653b36f820e644501bc89d2473719d51c8df66d72e784; mojo-session-id={"id":"8347c63120ee80d07a496942f55b7c27","time":1597848442619}; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1597808329,1597808989,1597830682,1597848453; mojo-trace-id=4; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1597848491; __mta=45920667.1597662284150.1597841990228.1597848491180.13; _lxsdk_s=1740730bf88-7bb-76d-a05%7C%7C4'
    headers = {'user-agent': user_agent, 'cookie': cookie}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        logging.error('get invalid status code %s while scraping %s',
                      response.status_code, url)
    except requests.RequestException:
        logging.error('error occurred while scraping %s', url, exc_info=True)


def parse_index(html):
    bs_info = bs(html, 'html.parser')
    for tags in bs_info.find_all('div',
                                 attrs={'class': 'film-channel'},
                                 limit=10):
        href = tags.find('a').get('href')
        detail_url = urljoin(BASE_URL, href)
        logging.info('get detail url %s', detail_url)
        yield detail_url


def scrapy_detail(url):
    return scrape_page(url)


def parse_detail(html):
    bs_info = bs(html, 'html.parser')
    movie_brief = bs_info.find('div', attrs={'class': 'movie-brief-container'})
    name = movie_brief.find('h1').text
    categories = [atag.text for atag in movie_brief.find_all('a')]
    published_at = movie_brief.find_all('li')[-1].text
    return {
        'name': name,
        'categoeies': categories,
        'published_at': published_at
    }


def save_data(movie_data_list):
    movie = pd.DataFrame(data=movie_data_list)
    movie.to_csv('./movie.csv', encoding='utf8', index=False, header=False)
    logging.info('save dato to csv')


def main(url):
    movie_data_list = []
    index_html = scrape_page(url)
    detail_urls = parse_index(index_html)
    for detail_url in detail_urls:
        detail_html = scrapy_detail(detail_url)
        sleep(2)
        data = parse_detail(detail_html)
        logging.info('get detail data %s', data)
        movie_data_list.append(data)
    save_data(movie_data_list)


if __name__ == "__main__":
    url = 'https://maoyan.com/films?showType=3'
    main(url)
