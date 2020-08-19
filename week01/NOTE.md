学习笔记

## 关于 python 虚拟环境

放弃 Anaconda，学习使用 Python 的 venv 来进行虚拟环境的管理。

### 配置 venv 虚拟环境

#### Windows 环境

```
python -m venv project-venv
project-venv\scripts\activate

# 退出
deactivate
```

#### Mac 环境

```
python -m venv project-venv
source project-venv/bin/activate
```

venv 创建的虚拟环境的 Python 是基于你自己安装的 Python 版本，如果有其它版本的需要，可以进行多版本 Python 的安装，然后根据需要创建虚拟环境。

## 爬虫解析库

### BeautifulSoup

这里主要记录一些常用的方法注意事项，更多的可以在官方文档进行查看

[BeautifulSoup](https://beautifulsoup.readthedocs.io/zh_CN/v4.4.0/)

#### 简单示例：

```
import requests
from bs4 import BeautifulSoup as bs

myurl = 'https://movie.douban.com/top250?start=0'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
headers = {'user-agent': user_agent}
response = requests.get(myurl, headers=headers)

bs_info = bs(response.text, 'html.parser')

for tags in bs_info.find_all('div', attrs={'class': 'hd'}):
    for atag in tags.find_all('a'):
        print(atag.get('href'))
        print(atag.find('span').text)
```

#### find_all() 和 find()

```
find_all( name , attrs , recursive , string , **kwargs )

find( name , attrs , recursive , string , **kwargs )
```

find_all() 方法搜索当前 tag 的**所有** tag 子节点,并判断是否符合过滤器的条件，其中有几个可选的参数：

- name：搜索 name 参数的值可以使任一类型的 过滤器 ,字符窜,正则表达式,列表,方法或是 True
- string 参数：通过 string 参数可以搜搜文档中的字符串内容.与 name 参数的可选值一样, string 参数接受 字符串 , 正则表达式 , 列表, True
- keyword 参数：如果一个指定名字的参数不是搜索**内置的参数名**，搜索时会把该参数当作指定名字 tag 的**属性**来搜索
- limit 参数：限定搜索数量
- recursive 参数：调用 tag 的 find_all() 方法时,Beautiful Soup 会检索当前 tag 的所有子孙节点,如果只想搜索 tag 的直接子节点,可以使用参数 recursive=False

find() 方法搜索符合条件的**第一个** tag。

#### find_all() 和 find() 的区别

1. find_all() 方法的返回结果是值包含一个元素的列表,而 find() 方法直接返回结果.
2. find_all() 方法没有找到目标是返回空列表, find() 方法找不到目标时,返回 None

### Xpath

Xpath 是一个比 BeautifulSoup 更加高效的解析库，是一门在 XML 文档中查找信息的语言。

#### 简单示例：

```
import requests
import lxml.etree

detail_url = 'https://movie.douban.com/subject/1292052/'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
headers = {}
headers['user-agent'] = user_agent
response = requests.get(detail_url, headers=headers)

selector = lxml.etree.HTML(response.text)

film_name = selector.xpath('//*[@id="content"]/h1/span[1]/text()')
print(film_name)

plan_data = selector.xpath('//*[@id="info"]/span[10]/text()')
print(plan_data)

rating = selector.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')
print(rating)
```

Xpath 的使用主要路径表达式的书写，需要不断重复训练来掌握常用的表达式！

## Scrapy

如何创建 Scrapy 项目

**安装 scrapy 包**

```
pip install scrapy
```

**创建项目文件**

```
scrapy startproject spiders

cd spiders
scrapy genspider movies douban.com
```

**运行**

```
scrapy crawl douban
```

#### 学习 Scrapy 中踩过的坑：

在 pipelines.py 文件中写好数据存储的代码之后，运行却并没有效果，pipelines.py 文件没有执行

原因：忽略了配置文件 setting.py

解决：在 settings.py 里面进行正确的配置即可

```
# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'spiders.pipelines.SpidersPipeline': 300,
}
```
