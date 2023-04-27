import telebot
from telebot import types
import sqlite3


bot = telebot.TeleBot("5948560486:AAF5dpggxpk-jp6kTtyA4jkFSsfensro4J4")
main_data = []


@bot.message_handler(commands=["start"])
def start_message(message):

    database(message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    connect = sqlite3.connect('db/data.sqlite')
    cursor = connect.cursor()
    admin = cursor.execute("SELECT status FROM uid WHERE chat_id = ?", (message.chat.id, )).fetchone()
    connect.close()
    if admin[0] == 1:
        b1 = types.KeyboardButton("Посмотреть заявки")
        markup.add(b1)
        bot.send_message(message.chat.id, "Привет, Юрист", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Здравствуйте! Пожалуйста, введите свои ФИО и email.")
        bot.register_next_step_handler(message, handle_message)


def handle_message(message):
    user_data = message.text.split()
    email = ''
    for i in range(len(user_data)):
        if '@' in user_data[i]:
            email = user_data[i]
            user_data.remove(user_data[i])
            break
        else:
            user_data[i].capitalize()
    user_data = ' '.join(user_data)
    connect = sqlite3.connect('db/data.sqlite')
    cursor = connect.cursor()
    application = cursor.execute('''SELECT title FROM statuses WHERE id = (SELECT status FROM submits 
                                    WHERE name LIKE ? AND email LIKE ?)''', (user_data, email)).fetchone()
    connect.close()
    if application is None:
        bot.send_message(message.chat.id, "Вы не оставили заявку на нашем сайте.")
    else:
        bot.send_message(message.chat.id, f"Статус вашей заявки: {application[-1]}")


@bot.message_handler(regexp='Посмотреть заявки')
def see_request(message, page_id=1, previous_message=None):

    connect = sqlite3.connect("db/data.sqlite")
    cursor = connect.cursor()
    pages_count_query = cursor.execute("SELECT COUNT(*) FROM submits")
    pages_count = int(pages_count_query.fetchone()[0])

    apn_type = cursor.execute(
        """SELECT title FROM services
        WHERE id = (SELECT type FROM submits WHERE id = ?)""", (page_id, )).fetchone()[0]
    text = cursor.execute("""SELECT text FROM submits WHERE id = ?""", (page_id, )).fetchone()[0]
    connect.close()

    buttons = types.InlineKeyboardMarkup()

    left = page_id - 1 if page_id != 1 else pages_count
    right = page_id + 1 if page_id != pages_count else 1

    left_button = types.InlineKeyboardButton("←", callback_data=f'to {left}')
    page_button = types.InlineKeyboardButton(f"{str(page_id)} / {str(pages_count)}", callback_data='_')
    description = types.InlineKeyboardButton("Подробнее", callback_data=f'desc {page_id}')
    right_button = types.InlineKeyboardButton("→", callback_data=f'to {right}')
    buttons.add(left_button, page_button, right_button, description)

    # noinspection PyBroadException
    try:
        msg = f"Название: *{apn_type}* Описание: "
        msg += f"*{text}*\n" if text is not None else '_нет_\n'

        bot.send_message(message.chat.id, msg, reply_markup=buttons)

    except Exception:
        msg = f"Название: *{apn_type}*\nОписание: "
        msg += f"*{text}*\n" if text is not None else '_нет_\n'

        bot.send_message(message.chat.id, msg, reply_markup=buttons)

    # noinspection PyBroadException
    try:
        bot.delete_message(message.chat.id, previous_message.id)

    except Exception:
        pass


@bot.callback_query_handler(func=lambda c: True)
def callback(c):
    if 'to' in c.data:
        see_request(c.message, page_id=int(c.data.split(' ')[1]), previous_message=c.message)
    if 'desc' in c.data:
        page = int(c.data.split(' ')[1])
        connect = sqlite3.connect("db/data.sqlite")
        cursor = connect.cursor()
        product_query = cursor.execute(
            """SELECT text, name, time, email, phone, status FROM submits 
            WHERE id = ?""", (page, )).fetchone()
        apn_type = cursor.execute(
            """SELECT title FROM services
            WHERE id = (SELECT type FROM submits WHERE id = ?)""", (page,)).fetchone()[0]
        connect.close()
        text, name, time, email, phone, status = product_query
        buttons = types.InlineKeyboardMarkup()
        turn_back = types.InlineKeyboardButton("Свернуть", callback_data=f'back {page}')
        status_button = types.InlineKeyboardButton("Сменить статус", callback_data=f'status {page}')
        buttons.add(turn_back, status_button)
        dictionary(name, email, page)
        bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id,
                              text=f'''Тип заявки: {apn_type}\nТекст: {text}\nСтатус заявки: {status}
ФИО клиента: {name}\nE-mail: {email}\nТелефон: {phone}\nВремя: {time}''', reply_markup=buttons)
    if 'back' in c.data:
        dictionary(method=False)
        see_request(c.message, page_id=int(c.data.split(' ')[1]), previous_message=c.message)
    if 'status' in c.data:
        buttons_markup = types.InlineKeyboardMarkup()
        buttons_markup.row(types.InlineKeyboardButton('Заявка отправлена исполнителю', callback_data='stts1'))
        buttons_markup.row(types.InlineKeyboardButton('Заявка прочитана, готовится ответ', callback_data='stts2'))
        buttons_markup.row(types.InlineKeyboardButton('Отправлен ответ на заявку', callback_data='stts3'))
        buttons_markup.row(types.InlineKeyboardButton('Заявка дополнена', callback_data='stts4'))
        buttons_markup.row(types.InlineKeyboardButton('Заявка закрыта', callback_data='stts5'))
        buttons_markup.row(types.InlineKeyboardButton('Заявка отменена', callback_data='stts6'))
        bot.edit_message_reply_markup(chat_id=c.message.chat.id, message_id=c.message.message_id,
                                      reply_markup=buttons_markup)
    if 'stts' in c.data:
        name, email, page = main_data[0][0], main_data[0][1], main_data[0][2]
        connect = sqlite3.connect("db/data.sqlite")
        cursor = connect.cursor()
        cursor.execute("""UPDATE submits SET status = ? WHERE (name LIKE ? AND email LIKE ?)""",
                       (c.data[4], name, email))
        connect.commit()
        connect.close()
        dictionary(method=False)
        see_request(c.message, page_id=page, previous_message=c.message)


def dictionary(name='', email='', page=1, method=True):
    if method:
        main_data.append((name, email, page))
    else:
        main_data.clear()


def database(message):
    connect = sqlite3.connect('db/data.sqlite')
    cursor = connect.cursor()
    connect.commit()
    user_id = message.chat.id

    cursor.execute("SELECT * FROM uid WHERE chat_id = ?", (user_id, ))
    data = cursor.fetchone()
    # Если база пуста
    if data is None:
        user_id = message.chat.id
        cursor.execute("INSERT INTO uid VALUES(?, ?)", (user_id, 0))

        connect.commit()
    else:
        pass


bot.polling(none_stop=True)
