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
        'shishishu'
        'dai5786'
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
            for addr in v[1]:
                url = path + '/' + addr
                # print(url)
                rsp = requests.get(url)
                if rsp is None:
                    return eth_offline_workers, btc_offline_workers, ltc_offline_workers
                if rsp.status_code != 200:
                    logging.error('获取workers失败')
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


def get_ignored_workers():
    try:
        rsp = requests.get('http://wxapp.video.eqlky.com:13008/ignore')
        jrsp = json.loads(rsp.text)
        workers = jrsp['data']
        return workers
    except Exception as e:
        print(e)
    return []

def main():
    logging.info("启动监控程序...")
    while True:
        for i in range(1):
            try:
                eth_offline_workers, btc_offline_workers, ltc_offline_workers = get_offline_workers()
                # 去掉忽略的机子
                ignore_workers = get_ignored_workers()
                eth_offline_workers = list(set(eth_offline_workers) - set(ignore_workers))

                if len(eth_offline_workers) == 0 and len(btc_offline_workers) == 0 and len(ltc_offline_workers) == 0:
                    logging.info("没有机子掉线")
                    break
                
                msg_text = '{}E,{}B,{}L\r\n'.format(len(eth_offline_workers), len(btc_offline_workers), len(ltc_offline_workers) )
                if len(eth_offline_workers) > 0:
                    if len(msg_text) > 0: msg_text += '\r\n---------------\r\n'
                    msg_text += '{}只XGP:[{},{}]\r\n\r\n'.format(len(eth_offline_workers), ',\r\n'.join(eth_offline_workers))
                if len(btc_offline_workers) > 0:
                    if len(msg_text) > 0: msg_text += '\r\n---------------\r\n'
                    msg_text += '{}头S19:[{},{}]\r\n\r\n'.format(len(btc_offline_workers), ',\r\n'.join(btc_offline_workers))
                if len(ltc_offline_workers) > 0:
                    if len(msg_text) > 0: msg_text += '\r\n---------------\r\n'
                    msg_text += '{}条L7:[{},{}]\r\n\r\n'.format(len(ltc_offline_workers), ',\r\n'.join(ltc_offline_workers))

                # 推送消息
                logging.info(msg_text)
                response = WxPusher.send_message(msg_text,
                                uids=["UID_GMc98LNntwlnCiqLc9Z4WTfFoa7O",
                                        "UID_37ulq6Lw7Or3sLWDzTzgYBJ1xuNA",
                                        ],
                                topic_ids=[4845],
                                token='AT_aVB4y3AQOtIn023wluulDzuWI8m0nXuS')

                if 1000 == response['code'] or response["success"] == True:
                    logging.info('微信推送成功!')
                else:
                    logging.error('微信推送失败!')
                pass
            except Exception as e:
                # logging.error(e)
                traceback.print_exc(e)

        logging.info('开始休眠10分钟')
        time.sleep(10 * 60)
    pass

if __name__ == '__main__':
    main()
    