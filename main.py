from flask import Flask, request, jsonify, render_template, flash, redirect
import sqlite3
import logging
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'M3d1ZWlod0ZFV0pXRkplZnZkbnhzbmN4enVocXd5dWVyMnkzMjh0SUVXSEZFM1VJZWcxMg=='
logging.basicConfig(level=logging.INFO)
sessionStorage = {}


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
        con = sqlite3.connect('db/data.sqlite')
        cur = con.cursor()
        today = str(datetime.now().strftime('%d.%m.%Y %H:%M'))
        works = ['Внесение изменений', 'Реорганизация ООО', 'Ликвидация',
                 'Регистрация ИП', 'Регистрация юр. лица', 'Регистрация ООО', 'Другое']
        name, text, tipe = request.form['fio'], request.form['comment'], works.index(request.form['type']) + 1
        email, phone = request.form['email'], request.form['phone']
        cur.execute("""INSERT INTO submits (name, text, type, time, email, phone, status) VALUES (?, ?, ?, ?, ?, ?, 
        1)""", (name, text, tipe, today, email, phone))
        con.commit()
        con.close()
        flash('Заявка отправлена, спасибо! Ожидайте ответа.', category='message')
        return redirect('/submit')


if __name__ == '__main__':
    app.run()
