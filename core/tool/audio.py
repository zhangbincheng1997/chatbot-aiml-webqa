#!/usr/bin/python
# -*- coding: UTF-8 -*-


# pip install baidu-aip
from aip import AipSpeech


# 糗事百科
def chat(message):
    """ 你的 APPID AK SK """
    APP_ID = '11199364'
    API_KEY = 'Em0YWy6shT5CiPXQGFHFCDd4'
    SECRET_KEY = '5ruCGEB2CZtKi6wfVNYVoniBsQCXftDN'

    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    # spd	String	语速，取值0-9，默认为5中语速	否
    # pit	String	音调，取值0-9，默认为5中语调	否
    # vol	String	音量，取值0-15，默认为5中音量
    # per	String	发音人选择, 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女
    result = client.synthesis(message, 'zh', 1, {'spd': 5, 'pit': 5, 'vol': 5, 'per': 0})

    # 识别正确返回语音二进制 错误则返回dict
    if not isinstance(result, dict):
        with open('auido0.mp3', 'wb') as f:
            f.write(result)


if __name__ == '__main__':
    chat('我是baby，请问我有什么可以帮你的吗？')
