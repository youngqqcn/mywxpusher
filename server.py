# conding:utf8
# author: yqq
# date: 2022-02-27 15:54
# description: 通过微信推送机子离线的消息，这是个本地服务

from flask import Flask, jsonify, request
from wxpusher import WxPusher

from monitor import get_offline_workers



app = Flask(__name__)

# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"


@app.route("/offline")
def offline_workers():
    eth_workers, btc_workers, ltc_workers = get_offline_workers()
    result = eth_workers + btc_workers + ltc_workers
    return  jsonify({"err_code":0,"err_msg":"", "data": result })

# @app.route("/sendmsg", methods=["POST"])
# def send_msg():
#     if 'msg_text' not in request.json:
#         return jsonify({"err_code":401,"err_msg":"invalid request parameters"})
#     msg_text = request.json['msg_text']
#     if len(msg_text) == 0: 
#         return jsonify({"err_code":402,"err_msg":"msg_text is empty"})
    
#     # 推送消息
#     response = WxPusher.send_message(msg_text,
#                       uids=["UID_GMc98LNntwlnCiqLc9Z4WTfFoa7O","UID_37ulq6Lw7Or3sLWDzTzgYBJ1xuNA"],
#                       topic_ids=[4845],
#                       token='AT_aVB4y3AQOtIn023wluulDzuWI8m0nXuS')

#     if 1000 == response['code'] or response["success"] == True:
#         return jsonify({"err_code":0,"err_msg":None})
#     return jsonify({"err_code": response["code"], "err_msg": response["msg"] })


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9444, debug=True)