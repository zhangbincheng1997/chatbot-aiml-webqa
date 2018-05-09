#!/usr/bin/python
# -*- coding: UTF-8 -*-

import ConfigParser
import shelve

import aiml
import jieba

from crawler import crawl
from deeplearning import deep
from tool import filter


class ChatBot:
    """
        基于 AIML 和 WebQA 的智能对话模型
        1. AIML 人工智能标记语言
        2. WebQA 开放域问答
        3. Deeplearning 深度学习

        usage:
        bot = ChatBot()
        print bot.response('你好')
    """

    def __init__(self, config_file='config.cfg'):
        config = ConfigParser.ConfigParser()
        config.read(config_file)
        self.filter_file = config.get('resource', 'filter_file')
        self.load_file = config.get('resource', 'load_file')
        self.save_file = config.get('resource', 'save_file')
        self.shelve_file = config.get('resource', 'shelve_file')

        # 初始化分词器
        jieba.initialize()

        # 初始化过滤器
        self.gfw = filter.DFAFilter()
        self.gfw.parse(self.filter_file)

        # 初始化知识库
        self.mybot = aiml.Kernel()
        self.mybot.bootstrap(learnFiles=self.load_file, commands='load aiml b')

        # 初始化学习库
        self.template = '<aiml version="1.0" encoding="UTF-8">\n{rule}\n</aiml>'
        self.category_template = '<category><pattern>{pattern}</pattern><template>{answer}</template></category>'

    def response(self, message):
        # 限制字数
        if len(message) > 60:
            return self.mybot.respond('MAX')
        elif len(message) == 0:
            return self.mybot.respond('MIN')

        # 过滤敏感词
        message = self.gfw.filter(message, "*")
        if message.find("*") != -1:
            return self.mybot.respond('过滤')

        # 结束聊天
        if message == 'exit' or message == 'quit':
            return self.mybot.respond('再见')
        # 开始聊天
        else:
            ########
            # AIML #
            ########
            result = self.mybot.respond(' '.join(jieba.cut(message)))

            # 匹配模式
            if result[0] != '#':
                return result
            # 搜索模式
            elif result.find('#NONE#') != -1:
                #########
                # WebQA #
                #########
                ans = crawl.search(message)
                if ans != '':
                    return ans.encode('utf-8')
                else:
                    ###############
                    # Deeplearing #
                    ###############
                    ans = deep.tuling(message)
                    return ans.encode('utf-8')
            # 学习模式
            elif result.find('#LEARN#') != -1:
                question = result[8:]
                answer = message
                self.save(question, answer)
                return self.mybot.respond('已学习')
            # MAY BE BUG
            else:
                return self.mybot.respond('无答案')

    def save(self, question, answer):
        db = shelve.open(self.shelve_file, 'c', writeback=True)
        db[question] = answer
        db.sync()
        rules = []
        for r in db:
            rules.append(self.category_template.format(pattern=r, answer=db[r]))
        with open(self.save_file, 'w') as fp:
            fp.write(self.template.format(rule='\n'.join(rules)))


if __name__ == '__main__':
    bot = ChatBot()
    while True:
        message = raw_input('ME > ')
        print 'AI > ' + bot.response(message)
