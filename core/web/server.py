#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
python server.py (nohub python server.py)

curl "0.0.0.0:5000/chat" -d "message=新闻"
curl "0.0.0.0:5000/chat" -d "message=天气"
curl "0.0.0.0:5000/chat" -d "message=时间"
"""
import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, render_template, request

from core.chatbot import ChatBot

app = Flask(__name__, static_url_path='')
bot = ChatBot()

# 按天对日志进行分割
# interval: 滚动周期
# backupCount: 备份个数
handler = TimedRotatingFileHandler('log/info.log', when="D", interval=1, backupCount=3)
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)


@app.route('/', methods=['GET', 'POST'])
def view():
    return render_template('index.html')


@app.route('/chat', methods=['GET'])
def response():
    data = request.args.to_dict()
    message = data['message']
    if message != '':
        answer = bot.response(message)
        return answer


if __name__ == '__main__':
    print bot.response('天气')
    app.run('0.0.0.0', debug=True)
