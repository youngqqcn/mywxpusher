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

    if len(eth_offline_workers) == 0 and len(btc_offline_workers) == 0 and len(ltc_offline_workers) > 0:
        logging.info("没有机子掉线")
    else:
        rtx3060ti_worker = []
        rx588_worker = []
        rtx2060_worker = []
        rx6600_worker = []
        rtx1660_worker = []
        rtx3080_worker = []
        a11_worker = []
        for w in eth_offline_workers:
            if '588' in w:
                rx588_worker.append(w)
            elif '3060' in w:
                rtx3060ti_worker.append(w)
            elif '1660' in w:
                rtx1660_worker.append(w)
            elif '3080' in w:
                rtx3080_worker.append(w)
            elif '6600' in w:
                rx6600_worker.append(w)
            elif '2060' in w:
                rtx2060_worker.append(w)
            elif w.count('x') < 2:
                a11_worker.append(w)
            else:
                rx588_worker.append(w)
            pass
    
        msg_text = '\r\n=====【掉线通知】=====\r\n'
        if len(rx588_worker)> 0:
            msg_text += '{}台小钢炮:[{},{}]\r\n\r\n'.format(len(rx588_worker), ','.join(rx588_worker[:5]), '' if len(rx588_worker) <= 5 else '...')
        if len(rtx3060ti_worker) > 0:
            msg_text += '{}台3060:[{},{}]\r\n\r\n'.format(len(rtx3060ti_worker), ','.join(rtx3060ti_worker[:5]), '' if len(rtx3060ti_worker) <= 5 else '...')
        if len(a11_worker) > 0:
            msg_text += '{}台心动:[{},{}]\r\n\r\n'.format(len(a11_worker), ','.join(a11_worker[:5]), '' if len(a11_worker) <= 5 else '...')
        if len(rx6600_worker) > 0:
            msg_text += '{}台6600:[{},{}]\r\n\r\n'.format(len(rx6600_worker), ','.join(rx6600_worker[:5]), '' if len(rx6600_worker) <= 5 else '...')
        if len(rtx1660_worker) > 0:
            msg_text += '{}台1660:[{},{}]\r\n\r\n'.format(len(rtx1660_worker), ','.join(rtx1660_worker[:5]), '' if len(rtx1660_worker) <= 5 else '...')
        if len(rtx2060_worker) > 0:
            msg_text += '{}台2060:[{},{}]\r\n\r\n'.format(len(rtx2060_worker), ','.join(rtx2060_worker[:5]), '' if len(rtx2060_worker) <= 5 else '...')
        if len(rtx3080_worker) > 0:
            msg_text += '{}台3080:[{},{}]\r\n\r\n'.format(len(rtx3080_worker), ','.join(rtx3080_worker[:5]), '' if len(rtx3080_worker) <= 5 else '...')
        if len(btc_offline_workers) > 0:
            msg_text += '{}台S19:[{},{}]\r\n\r\n'.format(len(btc_offline_workers), ','.join(btc_offline_workers[:5]), '' if len(btc_offline_workers) <= 5 else '...')
        msg_text += '======================\r\n'

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
    