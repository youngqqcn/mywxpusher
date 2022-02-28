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
    
]

def loop():
    # logging.info('开始新一轮检查')
    pool_host = 'https://api.f2pool.com'
    map = {
        'eth': ['eth', eth_addrs],
        # 'ltc': ['litecoin', ltc_addrs],
        'btc': ['bitcoin', btc_addrs],
    }
    eth_offline_workers = []
    btc_offline_workers = []
    ltc_offline_workers = []

    for k, v in map.items():
        path = pool_host + '/' + v[0]
        for addr in v[1]:
            url = path + '/' + addr
            # print(url)
            rsp = requests.get(url)
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
                    if k == 'bitcoin':
                        btc_offline_workers.append(w_name)

    if len(eth_offline_workers) == 0 and len(btc_offline_workers) == 0 and len(ltc_offline_workers) == 0:
        logging.info("没有机子掉线")
        return
    
    msg_text = '\r\n====【掉线通知】====\r\n'
    msg_text += '{}台小钢炮: [{}]\r\n\r\n'.format(len(eth_offline_workers), ','.join(eth_offline_workers))
    if len(btc_offline_workers) > 0:
        if len(msg_text) > 0: msg_text += '\r\n---------------\r\n'
        msg_text += '{}台蚂蚁:[{},{}]\r\n\r\n'.format(len(btc_offline_workers), ','.join(btc_offline_workers))
    msg_text += '\r\n=========\r\n'

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

def main():
    logging.info("启动监控程序...")
    while True:
        try:
            loop()
        except Exception as e:
            logging.error(e)
            traceback.print_exc(e)
        logging.info('开始休眠10分钟')
        time.sleep(10 * 60)
    pass

if __name__ == '__main__':
    main()
    