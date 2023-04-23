from flask import Flask, request, render_template, flash, redirect, session, send_from_directory
import os
from data import db_session
import logging
from data.submits import Submit
from datetime import datetime, timedelta


app = Flask(__name__)
app.config['SECRET_KEY'] = 'M3d1ZWlod0ZFV0pXRkplZnZkbnhzbmN4enVocXd5dWVyMnkzMjh0SUVXSEZFM1VJZWcxMg=='
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60 * 24 * 30)
logging.basicConfig(level=logging.INFO)
sessionStorage = {}


@app.route('/')
@app.route('/main_page')
def main_page():
    if 'counter' not in session:
        session['counter'] = 1
    else:
        session['counter'] += 1
    return render_template('main_page.html', title='Главная страница', count=session['counter'])


@app.route('/about')
def about_page():
    return render_template('about.html', title='О нас', count=session['counter'])


@app.route('/services')
def services_page():
    return render_template('services.html', title='Услуги', count=session['counter'])


@app.route('/submit', methods=['GET', 'POST'])
def submit_page():
    if request.method == 'GET':
        return render_template('submit.html', title='Оставить заявку', count=session['counter'])
    elif request.method == 'POST':
        works = ['Внесение изменений', 'Реорганизация ООО', 'Ликвидация',
                 'Регистрация ИП', 'Регистрация юр. лица', 'Регистрация ООО', 'Другое']

        new_sub = Submit()
        new_sub.name = request.form['fio']
        new_sub.text = request.form['comment']
        new_sub.type = works.index(request.form['type']) + 1
        new_sub.time = str(datetime.now().strftime('%d.%m.%Y %H:%M'))
        new_sub.email = request.form['email']
        new_sub.phone = request.form['phone']
        new_sub.status = 1

        db_sess = db_session.create_session()
        db_sess.add(new_sub)
        db_sess.commit()

        flash('Заявка отправлена, спасибо! Ожидайте ответа.', category='message')
        return redirect('/submit')


@app.route('/galery')
def galery_page():
    return render_template('galery.html', title='Галерея работ', count=session['counter'])


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'img/favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    db_session.global_init("db/data.sqlite")
    app.run()
