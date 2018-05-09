#!/usr/bin/python
# -*- coding: UTF-8 -*-

from search import *


#####################
#       WebQA       #
#####################
def search(message):
    result = ''

    '''新浪新闻'''
    if message.find('新闻') != -1:
        result += u'我给你讲个新闻吧~~~\n'
        result += news()
        return result

    '''每日一文'''
    if message.find('文章') != -1:
        result += u'我给你讲个文章吧~~~\n'
        result += read()
        return result

    '''糗事百科'''
    if message.find('笑话') != -1:
        result += u'我给你讲个笑话吧~~~\n'
        result += joke()
        return result

    ''' 搜狗时间'''
    if message.find('时间') != -1:
        soup_sougou = get_sougo(message)
        url = soup_sougou.select_one('a[href*="http://time.tianqi.com/"]')
        if url is not None:
            print '搜狗时间找到答案'
            soup_time = get_html(url['href'])
            result = soup_time.find(id='clock').get_text().strip()
            return result

    '''搜狗天气'''
    if message.find('天气') != -1:
        soup_sougou = get_sougo(message)
        res1 = soup_sougou.find(class_='more-day')
        if res1 is not None:
            print '搜狗天气找到答案'  # 单个城市天气
            for a in res1.find_all('a'):
                for p in a.stripped_strings:
                    result += p + ' '
                result += '\n'
            return result[:-1]
        res2 = soup_sougou.find(class_='modules-statistics')
        if res2 is not None:
            print '搜狗天气找到答案'  # 多个城市天气
            for tr in res2.find_all('tr'):
                for td in tr.stripped_strings:
                    result += td + ' '
                result += '\n'
            return result[:-1]

    '''搜狗空气'''
    if message.find('空气') != -1:
        soup_sougou = get_sougo(message)
        res = soup_sougou.find(class_='show-box')
        if res is not None:
            print '搜狗空气找到答案'
            num = soup_sougou.find(class_='num').get_text().strip()
            state = soup_sougou.find(class_='state').get_text().strip()
            txt = soup_sougou.find(class_='txt').get_text().strip()
            result += num + ' ' + state + ' ' + txt + '\n'
            return result

    # 抓取百度前10条的摘要
    soup_baidu = get_baidu(message)
    for i in range(1, 10):
        results = soup_baidu.find(id=i)
        if results is not None:
            '''百度汉语'''
            if results.attrs.has_key('mu') and results.attrs['mu'].__contains__('http://hanyu.baidu.com'):
                prop = results.find(class_='op_exactqa_detail_s_prop')
                author = results.find(class_='op_exactqa_detail_s_author')
                answer = results.find(class_='op_exactqa_detail_s_answer')
                if prop is not None and author is not None and answer is not None:
                    print '百度汉语找到答案'
                    result += prop.get_text().strip() + '\n'
                    result += author.get_text().strip() + '\n'
                    result += answer.get_text().strip()
                    return result
                table = results.find_all(class_='op_dict3_chinese_result_table')
                if table is not None:
                    print '百度汉语找到答案'
                    result = '\n'.join([tb.get_text().strip() for tb in table])
                    return result

            '''百度翻译'''
            if results.attrs.has_key('mu') and results.attrs['mu'].__contains__('http://fanyi.baidu.com'):
                one = results.find(class_='op_sp_fanyi_line_one')
                two = results.find(class_='op_sp_fanyi_line_two')
                if one is not None and two is not None:
                    print '百度翻译找到答案'
                    result += one.get_text().strip() + '\n'
                    result += two.get_text().strip()
                    return result
                text1 = results.find_all(class_='op_dict_text1')
                text2 = results.find_all(class_='op_dict_text2')
                if text1 is not None and text2 is not None:
                    print '百度翻译找到答案'
                    result = '\n'.join([t1.get_text().strip() + t2.get_text().strip() for t1, t2 in zip(text1, text2)])
                    return result

            '''百度汇率'''
            if results.attrs.has_key('tpl') and results.attrs['tpl'] == 'exrate':
                res = results.find(class_='op_exrate_result')
                tip = results.find(class_='op_exrate_tip')
                if res is not None and tip is not None:
                    print '百度汇率找到答案'
                    result += res.get_text().strip() + '\n'
                    result += tip.get_text().strip()
                    return result

            '''百度图谱'''
            if results.attrs.has_key('tpl') and results.attrs['tpl'] == 'exactqa':
                answer = results.find(class_='op_exactqa_s_answer')
                if answer is not None:
                    print '百度图谱找到答案'
                    result = answer.get_text().strip()
                    return result
                body = results.find(class_='op_exactqa_body')
                if body is not None:
                    print '百度图谱找到答案'
                    result = ' '.join([a.find('a')['title'] for a in body.select('.op_exactqa_item')])
                    return result

            '''百度计算'''
            if results.attrs.has_key('tpl') and results.attrs['tpl'] == 'calculator_html':
                pro = results.find(class_='op_new_val_screen_process')
                res = results.find(class_='op_new_val_screen_result')
                if pro is not None and res is not None:
                    print '百度计算找到答案'
                    result += pro.get_text().strip() + '\n'
                    result += res.get_text().strip()
                    return result

            '''百度股票'''
            if results.attrs.has_key('tpl') and results.attrs['tpl'] == 'stockdynamic_moretab':
                pan = results.find(class_='op-stockdynamic-moretab-pan')
                info = results.find(class_='op-stockdynamic-moretab-info')
                if pan is not None and info is not None:
                    print '百度股票找到答案'
                    result += pan.get_text().strip() + '\n'
                    result += info.get_text().strip()
                    return result

            '''百度歌词'''
            if results.attrs.has_key('tpl') and results.attrs['tpl'] == 'music_lrc':
                lines = results.find_all(class_='wa-musicsong-lyric-line')
                if lines is not None:
                    print '百度歌词找到答案'
                    result = '\n'.join([line.get_text().strip() for line in lines])
                    return result

            '''百度推荐'''
            if results.attrs.has_key('tpl') and results.attrs.has_key('tpl') and results.attrs['tpl'] == 'best_answer':
                url = results.find(class_='op_best_answer_question_link')
                if url is not None:
                    print '百度推荐找到答案'
                    soup_html = get_html(url['href'])
                    text = soup_html.find(class_='best-text')
                    if text is not None:
                        result = text.get_text().strip()
                        return result

            '''百度最新'''
            if results.find('h3') is not None and results.attrs.has_key('tpl') and results.attrs[
                'tpl'] == 'sp_realtime_bigpic5':
                url = results.find('h3').find('a')['href']
                if url is not None:
                    print '百度最新找到答案'
                    soup_html = get_html(url)
                    best = soup_html.find(class_='t')
                    if best is not None:
                        result = best.get_text().strip()
                        return result

            '''百度百科'''
            if results.find('h3') is not None and results.find('h3').find('a').get_text().__contains__(u"百度百科"):
                url = results.find('h3').find('a')['href']
                if url is not None:
                    print '百度百科找到答案'
                    soup_baike = get_html(url)
                    [s.extract() for s in soup_baike(class_=['sup--normal', 'sup-anchor'])]  # 过滤标签
                    result = soup_baike.find(class_='lemma-summary').get_text().replace('\n', '').strip()
                    if result != '': return result

            '''百度知道'''
            if results.find('h3') is not None and results.find('h3').find('a').get_text().__contains__(u"百度知道") \
                    and i > 3:
                url = results.find('h3').find('a')['href']
                if url is not None:
                    print '百度知道找到答案'
                    soup_zhidao = get_html(url)
                    best = soup_zhidao.find(class_='best-text')
                    text = soup_zhidao.find(class_='answer-text')
                    if best is not None:
                        result = best.get_text().strip()
                        return result
                    if text is not None:
                        result = text.get_text().strip()
                        return result

    return result


if __name__ == '__main__':
    message = "四大美女"
    print search(message)
