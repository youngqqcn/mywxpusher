# coding:utf8
# author: yqq
# 监控

import json
import time
import traceback
import requests
from wxpusher import WxPusher
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s,%(levelname)s] %(message)s')


def get_offline_workers():

    eth_addrs = [
        '0xc8eb99d5db1ec8ed483bf36cf548d096c063b4b2',
        '0xa71f66a1faa36ae54ef8c3141bbdfc0aae3791ee',
        '0x20f72f9bad243ac4d49101a29aa1cb180b933930',
        '0xa1647b564b3c1e9617d431100fff7ea8740fb62b',
        'heizai',
        '0xa1647b564b3c1e9617d431100fff7ea8740fb62b',
        '0x6b41d273ebe0cfe3c1c54253aa251a0b5c57e06d',
        '0xcc26c8ffd21aa299929db453ab9014d560143ef6',
        'z18978645557'
    ]

    btc_addrs = [
        'shishishu'
    ]

    ltc_addrs = [
        'shishishu',
        'dai5786',
    ]

    # logging.info('开始新一轮检查')
    pool_host = 'https://api.f2pool.com'
    map = {
        'eth': ['eth', eth_addrs],
        'btc': ['bitcoin', btc_addrs],
        'ltc': ['litecoin', ltc_addrs],
    }
    eth_offline_workers = []
    btc_offline_workers = []
    ltc_offline_workers = []

    # f2pool
    try:
        for k, v in map.items():
            path = pool_host + '/' + v[0]
            print(path)
            for addr in v[1]:
                url = path + '/' + addr
                print(url)
                rsp = requests.get(url)
                if rsp is None:
                    return eth_offline_workers, btc_offline_workers, ltc_offline_workers
                if rsp.status_code != 200:
                    logging.error('获取workers失败, status code: {}'.format(rsp.status_code))
                    time.sleep(10)
                    rsp = requests.get(url)
                    if rsp.status_code != 200:
                        return eth_offline_workers, btc_offline_workers, ltc_offline_workers

                jrsp = json.loads(rsp.text)
                workers = jrsp['workers']

                for worker in workers:
                    w_name = worker[0]
                    w_time = worker[6]
                    w_time = w_time[ : w_time.find('.')]
                    ta = time.strptime(w_time, "%Y-%m-%dT%H:%M:%S")
                    timestamp = int(time.mktime(ta))  + 8*3600
                    # print(timestamp)
                    nowts = int(time.time())
                    # print(nowts)

                    # 超过15分钟
                    if nowts - timestamp > 15 * 60:
                        if k == 'eth':
                            eth_offline_workers.append(w_name)
                        if k == 'btc':
                            btc_offline_workers.append(w_name)
                        if k == 'ltc':
                            ltc_offline_workers.append(w_name)
    except Exception as e:
        # logging.error("{}", e)
        traceback.print_exc(e)
    return eth_offline_workers, btc_offline_workers, ltc_offline_workers