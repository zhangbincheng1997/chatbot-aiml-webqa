#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os

import aiml
import jieba

import learn
from crawler import crawl
from tool import filter

LOAD_FILE = 'resources/load.xml'

if __name__ == '__main__':

    # 初始化jb分词器
    jieba.initialize()

    # 初始化过滤器
    gfw = filter.DFAFilter()
    gfw.parse(u"resources/恶心.txt")
    gfw.parse(u"resources/政治.txt")
    gfw.parse(u"resources/色情.txt")
    gfw.parse(u"resources/违法.txt")

    # 启动
    mybot = aiml.Kernel()
    mybot.bootstrap(learnFiles=LOAD_FILE, commands="load aiml b")
    print u'baby >> 请尽情调戏我吧!'

    while True:
        input_message = raw_input("me >> ")
        input_message = input_message.strip()

        ########## 过滤 ##########
        input_message = gfw.filter(input_message, "*")
        if input_message.find("*") != -1:
            print 'baby >> ' + mybot.respond("过滤")
            continue

        ########## 字数限制 ##########
        message = ' '.join(jieba.cut(input_message))
        if len(input_message) > 50:
            print 'baby >> ' + mybot.respond("句子长度过长")
            continue
        elif len(input_message) == 0:
            print 'baby >> ' + mybot.respond("无")
            continue

        ########## 开始回复 ##########
        print message
        if message == 'exit':
            print 'baby >> ' + mybot.respond('再见')
            break
        else:
            response = mybot.respond(message)

            # 知识库模式
            if response[0] != '#':
                print 'baby >> ' + response
            # 搜索模式
            elif response.find('#NONE#') != -1:
                ans = crawl.search(input_message)
                if ans == '':
                    print mybot.respond('找不到答案')
                    # TODO 深度学习
                else:
                    print 'baby >> ' + ans.encode("utf8")
            # 学习模式
            elif response.find('#LEARN#') != -1:
                question = response[8:]
                answer = input_message
                learn.save(question, answer)
                print 'baby >> ' + mybot.respond('学习完毕')
            else:
                # 出错
                exit()
