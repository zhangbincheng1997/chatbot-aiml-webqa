#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
TODO
1. 模板更新
2. 模板记忆
3. 优化爬虫
"""

import os

import aiml
import jieba

from crawler import crawl

if __name__ == '__main__':

    # 初始化jb分词器
    jieba.initialize()

    mybot = aiml.Kernel()
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/bye.aiml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/bad.aiml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/funny.aiml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/personname.aiml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/OrdinaryQuestion.aiml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/Common conversation.aiml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/tuling.aiml")
    mybot.learn(os.path.split(os.path.realpath(__file__))[0] + "/resources/tools.aiml")

    print 'baby >> 请调教我吧~~~'

    while True:
        input_message = raw_input("me >> ")
        input_message = input_message.strip()

        if len(input_message) > 50:
            print 'baby >> ' + mybot.respond("句子长度过长")
            continue
        elif len(input_message) == 0:
            print 'baby >> ' + mybot.respond("无")
            continue

        message = ' '.join(jieba.cut(input_message))

        if message == 'exit':
            print 'baby >> ' + mybot.respond('再见')
            exit()
        else:
            response = mybot.respond(message)

            if response == '':
                print mybot.respond('找不到答案')
            elif response[0] != '#':  # 存在模板
                print 'baby >> ' + response
            elif response[0] == '#':  # 不存在模板
                ans = crawl.search(input_message)
                if ans == '':
                    print mybot.respond('找不到答案')
                else:
                    print 'baby >> ' + ans.encode("utf8")
