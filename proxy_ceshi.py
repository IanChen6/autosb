# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     
   Description :
   Author :       ianchen
   date：          
-------------------------------------------------
   Change Activity:
                   2017/11/22:
-------------------------------------------------
"""
import requests
import time
import random

static_proxy_url = "http://webapi.http.zhimacangku.com/getip?num=1&type=1&pro=440000&city=440100&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=2&regions="

def get_all_proxie():
    try_times = 0
    while try_times <= 3:
        try_times += 1
        try:
            proxy_list = []
            r = requests.get(static_proxy_url, timeout=10)
            if r is None or r.status_code != 200:
                continue
            line_list = r.text.split("\n")
            for line in line_list:
                line = line.strip("\r").strip("\n").strip()
                # if '7777' in line:
                #     line = line.replace('7777', '55555')
                # elif '8088' in line:
                #     line = line.replace('8088', '1088')

                if len(line) <= 0:
                    continue

                proxies = {'http': 'http://{}'.format(line), 'https': 'http://{}'.format(line)}
                proxy_list.append(proxies)
            return proxy_list
        except Exception:
            time.sleep(5)
            pass

    raise Exception('重试获取代理失败...')


if __name__ == "__main__":
    proxy_list=get_all_proxie()
    proxy=proxy_list[random.randint(0,len(proxy_list)-1)]
    print(proxy)