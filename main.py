from flask import Flask, request, jsonify, render_template
import logging

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'M3d1ZWlod0ZFV0pXRkplZnZkbnhzbmN4enVocXd5dWVyMnkzMjh0SUVXSEZFM1VJZWcxMg=='
# logging.basicConfig(level=logging.INFO)
# sessionStorage = {}


@app.route('/')
@app.route('/main_page')
def index():
    return render_template('header.html')


if __name__ == '__main__':
    app.run()
