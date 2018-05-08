#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
python server.py (nohub python server.py)

curl "0.0.0.0:5000/chat" -d "message=新闻"
curl "0.0.0.0:5000/chat" -d "message=天气"
curl "0.0.0.0:5000/chat" -d "message=时间"
"""


from flask import Flask, render_template, request
from core.chatbot import ChatBot
import logging

app = Flask(__name__, static_url_path='')
bot = ChatBot()

log_file = 'log/info.log'
fmt = '%(asctime)s : %(levelname)s : %(message)s'
logging.basicConfig(filename=log_file, format=fmt, level=logging.INFO)


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
