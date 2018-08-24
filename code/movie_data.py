#!/usr/bin/env.python
# -*- coding: utf-8 -*-
import re
import requests
import pandas as pd
import time
import random
from requests import RequestException

"""爬取的是豆瓣影片排行前400条信息，包括电影名称，链接地址，评分，电影类型，上映日期以及国家和地区"""
def get_url(url):
    """得到异步加载的链接地址列表"""
    u = []
    for i in range(0, 40, 2):
        new_url = url + str(i*10)
        u.append(new_url)
    return u

def get_url_text(input_list, headers):
    """将每个URI链接的源代码组合成为一个大的文本"""
    str = ''
    for s in input_list:
        try:
            r = requests.get(s, headers=headers)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            str = str + r.text
        except RequestException:
            print(RequestException)
        time.sleep(1)
    return str

def get_content(text):
    """通过正则对一整个大文本进行查找操作，所查找的结果返回并保存到一个列表中"""
    address_res = []
    title = re.findall(r'"title":"(.*?)"', text)
    add = re.findall(r'"url":"(.*?)"', text)
    rate = re.findall(r'"rate":"(.*?)"', text)
    for add in add:
        address_res.append('https:'+re.sub(re.compile('\\\\'), '/', add)[8:])
    return title, address_res, rate

def get_detail(address, headers):
    """对爬取到的电影链接进行进一步的爬取，得到每部电影的详细信息。
    由于有400条URL，所以如果保存为一整个大文本可能会导致溢出，所以用另外一种方法保存得到的信息，
    另外，由于在每部电影的源代码中存在很多属性相同的节点，所以采用正则表达式会更加简便。得到的结果不算特别理想。"""
    movie_type = []
    release_date = []
    producer_country = []
    s = 1                 # 初始化计数
    for i in address:
        try:
            r = requests.get(i, headers=headers)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            movie_type.append(re.findall('<span property="v:genre">(.*?)</span>', r.text))
            release_date.append(re.findall('<span class="year">(\(.*?\))</span>', r.text))
            producer_country.append(re.findall('制片国家/地区:</span> (.*?)<br/>', r.text))
            print("正在爬取第%d个网页" % s)    # 显示每次循环爬取的第多少个链接
            s += 1
        except RequestException:
            print(RequestException)
    return movie_type, release_date, producer_country

def save_result(result, detail):
    """通过pandas对爬取到的结果进行处理，最后保存到csv文件"""
    d = {'电影名称': result[0], '电影地址': result[1], '电影评分': result[2],
         '电影类型': detail[0], '上映日期': detail[1], '国家地区': detail[2]}
    end_data = pd.DataFrame(d)
    end_data.to_csv(r'result_encoding_gb18030.csv', encoding='gb18030', index=False)
    return end_data

def main():
    """主函数"""
    my_headers = [
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0"
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"
    ]           # 构造隐藏标识
    user_agent = random.choice(my_headers)
    headers = {
        'User_Agent': user_agent,
        'Cookie': 'll="108231"; bid=lp6WDrc5nKc; _vwo_uuid_v2=D2003811F9920EDDB4CE4497C487751D9|a954d86b21a4eb3b3ccea6b2fe090eac; ap_6_0_1=1; ps=y; ue="1960595754@qq.com"; dbcl2="67484523:RIwf3EXGFW0"; ck=ZG3E; push_noty_num=0; push_doumail_num=0; __utma=30149280.804054632.1534244658.1534855799.1534871147.6; __utmc=30149280; __utmz=30149280.1534871147.6.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; __utmv=30149280.6748; __utmb=30149280.4.10.1534871147; __utma=223695111.1126706729.1534244658.1534855799.1534871152.6; __utmb=223695111.0.10.1534871152; __utmc=223695111; __utmz=223695111.1534871152.6.3.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1534871152%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; _pk_id.100001.4cf6=b7df88e2b11c58f8.1534244658.6.1534871221.1534856407.'
    }              # 对user-agent和cookie进行设置，在my_headers中随机选择浏览器标识，达到反爬的目的
    base_url = 'https://movie.douban.com/j/search_subjects?'
    params = 'type=movie&tag=豆瓣高分&sort=rank&page_limit=20&page_start='
    url = base_url + params
    input_list = get_url(url)
    text = get_url_text(input_list, headers)
    result = get_content(text)
    address = result[1]
    detail = get_detail(address, headers)
    save_result(result, detail)


main()       # 调用主函数
