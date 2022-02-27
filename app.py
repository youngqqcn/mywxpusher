from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/sendmsg", methods=["POST"])
def send_msg():
    print(request.json)
    return jsonify({"err_code":0,"err_msg":None})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)