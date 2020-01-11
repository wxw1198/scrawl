# !/usr/bin/env python
# coding=utf-8
# author: ty
# 此代码仅供学习与交流，请勿用于商业用途。
# 城市缩写和城市名的映射
# 想抓取其他已有城市的话，需要把相关城市信息放入下面的字典中
# 不过暂时只有下面这些城市在链家上是统一样式
import os
import sys
import threading
import time

import threadpool
from threading import Thread, Lock
import district

# from utils.log import *

# cities = {
#     'bj': '北京',
#     'cd': '成都',
#     'cq': '重庆',
#     'cs': '长沙',
#     'dg': '东莞',
#     'dl': '大连',
#     'fs': '佛山',
#     'gz': '广州',
#     'hz': '杭州',
#     'hf': '合肥',
#     'jn': '济南',
#     'nj': '南京',
#     'qd': '青岛',
#     'sh': '上海',
#     'sz': '深圳',
#     'su': '苏州',
#     'sy': '沈阳',
#     'tj': '天津',
#     'wh': '武汉',
#     'xm': '厦门',
#     'yt': '烟台',
#     'wx': '无锡',
# }

cities = {
    'bj': '北京',
    'cd': '成都',
    'cq': '重庆',
}
lianjia_cities = cities
beike_cities = cities


def create_prompt_text():
    """
    根据已有城市中英文对照表拼接选择提示信息
    :return: 拼接好的字串
    """
    city_info = list()
    count = 0
    for en_name, ch_name in cities.items():
        count += 1
        city_info.append(en_name)
        city_info.append(": ")
        city_info.append(ch_name)
        if count % 4 == 0:
            city_info.append("\n")
        else:
            city_info.append(", ")
    return 'Which city do you want to crawl?\n' + ''.join(city_info)


def get_chinese_city(en):
    """
    拼音拼音名转中文城市名
    :param en: 拼音
    :return: 中文
    """
    return cities.get(en, None)


# def get_city():
#     city = None
#     # 允许用户通过命令直接指定
#     if len(sys.argv) < 2:
#         print("Wait for your choice.")
#         # 让用户选择爬取哪个城市的二手房小区价格数据
#         prompt = create_prompt_text()
#         city = input(prompt)
#     elif len(sys.argv) == 2:
#         city = str(sys.argv[1])
#         print("City is: {0}".format(city))
#     else:
#         print("At most accept one parameter.")
#         exit(1)
#
#     chinese_city = get_chinese_city(city)
#     if chinese_city is not None:
#         message = 'OK, start to crawl ' + get_chinese_city(city)
#         print(message)
#         logger.info(message)
#     else:
#         print("No such city, please check your input.")
#         exit(1)
#     return city

lock = threading.Lock()

def get_city_ershou_info(params):
    print(params)
    # city = get_city(k, v)
    # if city is not None:
    totalHouse, average = district.update(params[0])
    write_str = params[0] + "," + params[1]+ "," + str(totalHouse) + "," + str(average) + "\n"
    lock.acquire()
    params[2].write(write_str)
    lock.release()
    print(params[1], totalHouse, average)

def paramList(cn_cities, f):
    thread_param_list = []
    for k, v in cn_cities:
        group = [k, v, f]
        thread_param_list.append(group)

    return thread_param_list

def update():
    csv_file = os.getcwd() + "/{0}.csv".format("all_cities")
    with open(csv_file, "w") as f:

        start_time = time.time()
        pool = threadpool.ThreadPool(len(cities.items()))

        requests = threadpool.makeRequests(get_city_ershou_info, paramList(cities.items(),f))
        [pool.putRequest(req) for req in requests]
        pool.wait()
        print('%d second' % (time.time() - start_time))


if __name__ == '__main__':
    print(get_chinese_city("sh"))
