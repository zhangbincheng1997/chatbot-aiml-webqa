#!/usr/bin/python
# -*- coding: UTF-8 -*-

import glob
import yaml

import jieba

# https://github.com/gunthercox/chatterbot-corpus/tree/master/chatterbot_corpus/data/chinese
files = glob.glob('chinese/*.yml')
output_path = 'best.aiml'

doc_start = '<aiml version="1.0" encoding="UTF-8">\n'
doc_end = '</aiml>\n'
template_single = '<category><pattern>%s</pattern><template>%s</template></category>\n'
template_multiple = '<category><pattern>%s</pattern><template><random>%s</random></template></category>\n'
punc_cn = '＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､　、〃〈〉《》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏﹑﹔·！？｡。'.decode("utf-8")
punc_en = '!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~'.decode("utf-8")

questions = {}


def cut_word(text):
    text = text.strip(punc_en)
    text = text.strip(punc_cn)
    seg_list = jieba.cut(text)
    result = ' '.join(seg_list)
    return result


for file in files:
    with open(file, 'r') as f:
        data = yaml.load(f)
        for pair in data['conversations']:
            q = pair[0]
            a = pair[1]
            if not q in questions.keys(): questions[q] = []
            questions[q].append(a)

with open(output_path, 'w') as out:
    out.write(doc_start)
    for q, a in questions.items():
        q = cut_word(q)
        if len(a) == 1:
            temp = template_single % (q, a[0])
        else:
            str = ''.join(['<li>%s</li>' % aa for aa in a])
            temp = template_multiple % (q, str)
        out.write(temp.encode('utf-8'))
    out.write(doc_end)
