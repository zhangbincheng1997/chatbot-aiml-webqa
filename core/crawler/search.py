#!/usr/bin/python
# -*- coding: UTF-8 -*-

from urllib import quote

import requests
from bs4 import BeautifulSoup
from random import choice


# 百度搜索
def get_baidu(message):
    url = 'https://www.baidu.com/s?wd=' + quote(message)
    headers = {'User-Agent':
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
    soup_baidu = BeautifulSoup(requests.get(url=url, headers=headers).content, "lxml")
    return soup_baidu


# 搜狗搜索
def get_sougo(message):
    url = 'https://www.sogou.com/web?query=' + quote(message)
    headers = {'User-Agent':
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
    soup_sougou = BeautifulSoup(requests.get(url=url, headers=headers).content, "lxml")
    return soup_sougou


# 链接搜索
def get_html(url):
    headers = {'User-Agent':
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}
    soup_html = BeautifulSoup(requests.get(url=url, headers=headers).content, "lxml")
    return soup_html


# 新浪新闻
def news():
    url = 'http://news.sina.com.cn/china/'
    headers = {'User-Agent':
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}

    soup_html = BeautifulSoup(requests.get(url=url, headers=headers).content, "lxml")

    news = soup_html.select('.news-item')
    content = ''
    # 遍历每一个class=news-item的节点
    num = 0
    for new in news:
        h2 = new.select('h2')
        # 只选择长度大于0的结果
        if num == 5:
            break
        if len(h2) > 0:
            num += 1
            # 新闻时间
            time = new.select('.time')[0].get_text()
            # 新闻标题
            title = h2[0].get_text()
            # 新闻链接
            href = h2[0].select('a')[0]['href']
            content += time + ' ' + title + ' ' + href + '\n'
    return content


# 糗事百科
def joke():
    url = 'https://www.qiushibaike.com/text/'
    headers = {'User-Agent':
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}

    soup_html = BeautifulSoup(requests.get(url=url, headers=headers).content, "lxml")
    contents = soup_html.select('.content')
    content = choice(contents)

    if content is not None:
        content = content.get_text().strip()
    return content


# 每日一文
def read():
    url = 'https://meiriyiwen.com/random'
    headers = {'User-Agent':
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'}

    soup_html = BeautifulSoup(requests.get(url=url, headers=headers).content, "lxml")
    title = soup_html.find('h1')
    author = soup_html.find(class_='article_author')
    content = soup_html.find(class_='article_text')
    if title is not None and author is not None and content is not None:
        title = title.get_text().strip()
        author = author.get_text().strip()
        content = content.get_text().strip()
        return title + '\n' + author + '\n' + content
    return ''
