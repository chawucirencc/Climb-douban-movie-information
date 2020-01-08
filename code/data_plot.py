#!/usr/bin/env.python
# -*- coding: utf-8 -*-
import pandas as pd
import operator
import matplotlib.pyplot as plt
import re


''' 
    主要是针对所爬取下来的豆瓣400余条影视信息进行可视化分析：
    说明（1）：对于爬取的400余条数据信息，有48条信息不全，为类型乱码以及国家和地区为空，所以删除这些缺失的数据，
    所以所要分析的是剩下的数据，通过对电影评分的排序，可以知道剩余的数据的豆瓣评分都大于或者等于8.0.
    说明（2）：对于影片类型的分析，其中有很多电影不止分在一类，所以对这些电影做了一些处理，
    比如一部电影有三个分类，则分别对这三个类型的统计计数都分别加一次。所以得出的统计计数总数比电影数目多。
    说明（3）：对于国家和地区的分析，一部电影可能涉及多个国家和地区的制作，所以以排在第一的上映国家为准。
    简单的结果说明：
    （1）在豆瓣评分不小于8.0的这些电影中很多都在2010年以后上映，以2013年最多。
    （2）关于电影类型，可以看出绝大多数都以剧情片为主导，其中掺假爱情、犯罪、冒险等类型以及元素，从而构成电影的多元化。
    （3）对于不同国家和地区电影的产量图可以看出差距还是非常大，美国以绝对的优势领先。
'''
def get_data():
    """处理缺失数据，形成新的可用数据"""
    file = pd.read_csv('result_encoding_gb18030.csv', encoding='gb18030')
    data_frame = file[~file['国家地区'].isin(['[]'])]
    # print(sorted(data_frame['电影评分'], reverse=True))    # 查看评分排行
    return data_frame

def diff_date(data_frame):
    """处理不同年份和场次"""
    re_date = {}
    for i in data_frame['上映日期']:
        date = i.strip('[]').strip("''").strip('()')
        if date not in re_date:
            re_date[date] = 1
        else:
            re_date[date] += 1
    release_date = sorted(re_date.items(), key=operator.itemgetter(1), reverse=True)
    date = []
    times = []
    for da, time in release_date[:30]:
        date.append(da)
        times.append(time)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.bar(date, height=times, alpha=0.8, color=['r', 'g', 'b', 'y', 'm', 'c', 'g'])
    for x, y in enumerate(times):
        plt.text(x, y, '%s' % y, ha='center')
    plt.ylim(0, 30)
    plt.xlabel('电影上映年份', fontsize=12)
    plt.ylabel('电影场次', fontsize=12)
    plt.title('不同年份的电影场次数', fontsize=15)
    plt.show()

def diff_type(data_frame):
    """针对电影类型作出饼图"""
    mov_type = {}
    for i in data_frame['电影类型']:
        ty = re.sub(r"'", '', i).strip('[]').split(',')
        for t in ty:
            res = t.strip()
            if res not in mov_type:
                mov_type[res] = 1
            else:
                mov_type[res] += 1
    movies_type = sorted(mov_type.items(), key=operator.itemgetter(1), reverse=True)
    num = []
    types = []
    for x, y in movies_type:
        types.append(x)
        num.append(y)
    x = num[:15]
    x.append(sum(num[15:]))
    labels = types[:15]
    labels.append('其他')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.pie(x=x, labels=labels, autopct='%3.2f%%', startangle=0)
    plt.axis('equal')
    plt.title('电影类型占比', fontsize=15)
    plt.legend()
    plt.show()

def diff_regions(data_frame):
    """处理不同国家和地区"""
    country = data_frame['国家地区']
    regions = {}
    for c in country:
        cou = re.sub(r"'", '', c).strip('[]').split('/')[0].strip()
        if cou not in regions:
            regions[cou] = 1
        else:
            regions[cou] += 1
    countries_and_regions = sorted(regions.items(), key=operator.itemgetter(1), reverse=True)
    place, number = [], []
    for pl, num in countries_and_regions:
        place.append(pl)
        number.append(num)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.bar(place, number, alpha=0.8, color=['r', 'g', 'b', 'm', 'c', 'g'])
    for x, y in enumerate(number):
        plt.text(x, y, '%s' % y, ha='center')
    plt.xlabel('不同的国家和地区', fontsize=12)
    plt.ylabel('所属国家的电影部数', fontsize=12)
    plt.title('不同国家和地区的电影产量', fontsize=15)
    plt.show()
    
def main():
    """主函数"""
    data_frame = get_data()
    diff_date(data_frame)
    diff_type(data_frame)
    diff_regions(data_frame)


if __name__ == "__main__":
    """调用主函数"""
    main()
         
