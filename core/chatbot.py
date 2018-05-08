#!/usr/bin/python
# -*- coding: UTF-8 -*-

import aiml
import jieba

import learn
from crawler import crawl
from tool import filter


class ChatBot:
    """
        基于 AIML 和 WebQA的智能对话模型
        1. AIML 人工智能标记语言
        2. WebQA 开放域问答

        usage:
        bot = ChatBot()
        print bot.response('你好')
    """

    def __init__(self, filter_file=u'resources/敏感词.txt', load_file='resources/load.xml', cmd='load aiml b'):
        # 初始化分词器
        jieba.initialize()

        # 初始化过滤器
        self.gfw = filter.DFAFilter()
        self.gfw.parse(filter_file)

        # 初始化知识库
        self.mybot = aiml.Kernel()
        self.mybot.bootstrap(learnFiles=load_file, commands=cmd)

    def response(self, input_message):
        input_message = input_message.strip()

        # 限制字数
        if len(input_message) > 60:
            return self.mybot.respond("句子长度过长")
        elif len(input_message) == 0:
            return self.mybot.respond("无")

        # 过滤敏感词
        input_message = self.gfw.filter(input_message, "*")
        if input_message.find("*") != -1:
            return self.mybot.respond("过滤")

        # 结巴分词
        message = ' '.join(jieba.cut(input_message))

        # 结束聊天
        if message == 'exit' or message == 'quit':
            return self.mybot.respond('再见')
        # 开始聊天
        else:
            result = self.mybot.respond(message)

            # 匹配模式
            if result[0] != '#':
                return result
            # 搜索模式
            elif result.find('#NONE#') != -1:
                ans = crawl.search(input_message)
                if ans != '':
                    return ans.encode('utf-8')
                else:
                    ''' TODO '''
                    ##########
                    # 深度学习 #
                    ##########
                    return self.mybot.respond('找不到答案')
            # 学习模式
            elif result.find('#LEARN#') != -1:
                question = result[8:]
                answer = input_message
                learn.save(question, answer)
                return self.mybot.respond('学习完毕')
            # MAY BE BUG
            else:
                exit()


if __name__ == '__main__':
    bot = ChatBot()
    print 'AI > ' + bot.response('天气')
    while True:
        input_message = raw_input('ME > ')
        print 'AI > ' + bot.response(input_message)
