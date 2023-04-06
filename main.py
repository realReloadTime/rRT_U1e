from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'M3d1ZWlod0ZFV0pXRkplZnZkbnhzbmN4enVocXd5dWVyMnkzMjh0SUVXSEZFM1VJZWcxMg=='
logging.basicConfig(level=logging.INFO)
sessionStorage = {}


@app.route('/')
@app.route('/index')
def index():
    return "Привет, Яндекс!"


if __name__ == '__main__':
    app.run()
