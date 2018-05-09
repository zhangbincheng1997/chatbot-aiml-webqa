#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import urllib


# 图灵机器人
def tuling(message):
    key = '11f83b13f0784e77a897b1acaec86f33'
    url = 'http://www.tuling123.com/openapi/api?key=' + key + '&info=' + message
    page = urllib.urlopen(url)
    response = page.read()
    dic_json = json.loads(response)
    return dic_json['text']


if __name__ == '__main__':
    print tuling('时间')
