from flask import Flask, request, render_template, flash, redirect, session, send_from_directory
from data import db_session
import logging
from data.tables import Submit
from datetime import datetime, timedelta

import os

# позже здесь напишу адрес сайта на хостинге

application = Flask(__name__)
application.config['SECRET_KEY'] = 'M3d1ZWlod0ZFV0pXRkplZnZkbnhzbmN4enVocXd5dWVyMnkzMjh0SUVXSEZFM1VJZWcxMg=='
application.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60 * 24 * 30)
logging.basicConfig(level=logging.INFO)
sessionStorage = {}


@application.route('/')
@application.route('/main_page')
def main_page():
    if 'counter' not in session:  # счетчик посещений сайта (располагается в подвале)
        session['counter'] = 1
    else:
        session['counter'] += 1
    return render_template('main_page.html', title='Главная страница', count=session['counter'])


@application.route('/about')
def about_page():
    return render_template('about.html', title='О нас', count=session['counter'])


@application.route('/services')
def services_page():
    return render_template('services.html', title='Услуги', count=session['counter'])


@application.route('/submit', methods=['GET', 'POST'])
def submit_page():
    if request.method == 'GET':
        return render_template('submit.html', title='Оставить заявку', count=session['counter'])
    elif request.method == 'POST':
        works = ['Внесение изменений', 'Реорганизация ООО', 'Ликвидация',
                 'Регистрация ИП', 'Регистрация юр. лица', 'Регистрация ООО', 'Другое']  # список предоставляемых услуг

        # добавляю новую запись в таблицу заявок
        new_sub = Submit()
        new_sub.name = request.form['fio']
        new_sub.text = request.form['comment']
        new_sub.type = works.index(request.form['type']) + 1  # + 1 синхронизирует индекс дата базы с индексом в списке
        new_sub.time = str(datetime.now().strftime('%d.%m.%Y %H:%M'))
        new_sub.email = request.form['email']
        new_sub.phone = request.form['phone']
        new_sub.status = 1  # начальный статус любой заявки ("отправлено")

        db_sess = db_session.create_session()
        db_sess.add(new_sub)
        db_sess.commit()

        flash('Заявка отправлена, спасибо! Ожидайте ответа.', category='message')  # сообщение для пользователя
        return redirect('/submit')


@application.route('/galery')
def galery_page():
    return render_template('galery.html', title='Галерея работ', count=session['counter'])


@application.route('/favicon.ico')
def favicon():  # для отдельного отображения значка сайта
    return send_from_directory(os.path.join(application.root_path, 'static'),
                               'img/favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    db_session.global_init("db/data.sqlite")
    application.run()
