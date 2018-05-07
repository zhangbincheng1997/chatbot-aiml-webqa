#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
python server.py (nohub python server.py)

curl "0.0.0.0:5000/chat" -d "message=新闻"
curl "0.0.0.0:5000/chat" -d "message=天气"
curl "0.0.0.0:5000/chat" -d "message=时间"
"""

import os

import sys

sys.path.append(os.path.abspath(os.path.join('..')))


from flask import Flask, render_template, request
from core.chatbot import ChatBot

app = Flask(__name__, static_url_path='')
bot = ChatBot()


@app.route('/', methods=['GET', 'POST'])
def view():
    return render_template('index.html')


@app.route('/chat', methods=['GET'])
def response():
    data = request.args.to_dict()
    message = data['message']
    if message != '':
        return bot.response(message)


if __name__ == '__main__':
    print bot.response('天气')
    app.run('0.0.0.0', debug=False)
