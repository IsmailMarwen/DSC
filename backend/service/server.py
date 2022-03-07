from flask import Flask, Response, jsonify;
from flask import current_app, flash, jsonify, make_response, redirect, request, url_for
from flask_socketio import SocketIO, send
import redis
import json
from flask import jsonify
from flask_cors import CORS, cross_origin
import time
app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret'
app.debug = True
CORS(app)
redis_cache = redis.Redis(host='18.185.56.180', port=6379,charset='utf-8',decode_responses=True, password="JrHQRbplMc6zPBNIaVuEPHzHQnKTxEkZf5d6cJBqk3SauBkluEAr4CSkjBmP5RiP3nYgBooiUcmmY5h2")
@app.route('/set', methods = ['POST'])
@cross_origin(supports_credentials=True)
def set():
    print(request.json)
    redis_cache.hmset(request.json['idPartner'],request.json['detail'])
    return "OK"

@app.route('/delete/<string:key>')
def delete(key):
    redis_cache.delete(key)
    return "OK"
@app.route('/get/<string:key>')
def get(key):
    d=json.dumps(redis_cache.hgetall(key))
    return make_response(d, 200)
if __name__ == '__main__':
    app.run(host="192.168.1.32", port=5000)