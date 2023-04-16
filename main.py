from flask import Flask, request, jsonify, render_template
import logging

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'M3d1ZWlod0ZFV0pXRkplZnZkbnhzbmN4enVocXd5dWVyMnkzMjh0SUVXSEZFM1VJZWcxMg=='
# logging.basicConfig(level=logging.INFO)
# sessionStorage = {}


@app.route('/')
@app.route('/main_page')
def main_page():
    return render_template('main_page.html', title='Главная страница')


@app.route('/about')
def about_page():
    return render_template('about.html', title='О нас')


@app.route('/services')
def services_page():
    return render_template('services.html', title='Услуги')


@app.route('/submit', methods=['GET', 'POST'])
def submit_page():
    if request.method == 'GET':
        return render_template('submit.html', title='Оставить заявку')
    elif request.method == 'POST':
        print(request.form)
        print('posted')
        return 'Заявка отправлена, спасибо! Ожидайте ответа.'


if __name__ == '__main__':
    app.run()
