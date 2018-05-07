# 基于 AIML 和 WebQA的智能对话模型

## 概述
1. AIML 人工智能标记语言
2. WebQA 开放域问答
3. 效果展示
![alt text](docs/1.png "title")

## 启动服务
### 环境说明
Linux/Python2.7/PyCharm

### 安装依赖
```
$ pip install jieba
$ pip install aiml
$ pip install lxml
$ pip install beautifulsoup4
$ pip install shelve
```

### 运行流程
```
$ cd chatbot-aiml-webqa/core/
$ python2 chatbot.py
$ python2 web/server.py (nohub)

>>> * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)

CURL:
$ curl "0.0.0.0:5000/chat" -d "message=新闻"
$ curl "0.0.0.0:5000/chat" -d "message=天气"
$ curl "0.0.0.0:5000/chat" -d "message=时间"
```

## 处理流程
### 步骤一：预处理
1. 限制字数
2. 过滤敏感词（恶心、政治、色情、违法）
3. 结巴分词

### 步骤二：知识库匹配（AIML）
1. 基本功能：打招呼、闲聊......
2. 异常处理：问题太长、空白问题、找不到回复......
3. 情绪回答：表情、夸奖、嘲笑......

如果匹配不到，就进入步骤三

### 步骤三：互联网搜索（爬虫/API）
1. 新闻----新浪新闻
2. 文章----每日一文
3. 笑话----糗事百科
4. 时间----搜狗时间
5. 天气----搜狗天气
6. 空气----搜狗空气
7. 其他遍历百度搜索
> * 百度问答
> * 百度图谱
> * 百度汉语
> * 百度计算
> * 百度汇率
> * 百度股票
> * 百度翻译
> * 百度歌词
> * 百度百科
> * 百度知道
> * 百度推荐最佳回答
> * 百度最新相关信息

如果搜索不到，就进入步骤四

### 步骤四：神经网络
基于Seq2Seq模型的下一代对话引擎不仅仅是在现有的回答中训练最佳回答，而是能自我创造一个类似于人类的回答。
语料库：http://61.93.89.94/Noah_NRM_Data/
目前这部分没时间实现......

### 扩展功能
教学功能/记忆功能，利用AIML模板+shelve保存

### 后续实现
语音回复（百度语音合成API）

## 参考链接
1. https://github.com/SnakeHacker/QA-Snake
2. https://github.com/ictar/XIXI
3. https://github.com/fwwdn/sensitive-stop-words