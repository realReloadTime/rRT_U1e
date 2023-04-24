import telebot
from telebot import types
import sqlite3


bot = telebot.TeleBot("5948560486:AAF5dpggxpk-jp6kTtyA4jkFSsfensro4J4")


@bot.message_handler(commands=["start"])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1 = types.KeyboardButton("Посмотреть заявки")
    markup.add(b1)
    bot.send_message(message.chat.id, "Привет", reply_markup=markup)


@bot.message_handler(content_types=['Посмотреть заявки'])
def see_request(message, id=1, previous_message=None):

    connect = sqlite3.connect("data.sqlite")
    cursor = connect.cursor()
    pages_count_query = cursor.execute(f"SELECT COUNT(*) FROM `submits`")
    pages_count = int(pages_count_query.fetchone()[0])

    product_query = cursor.execute(
        f"SELECT 'text', 'name', 'type', 'time', 'email', 'phone', status FROM `submits` WHERE `id` = '{id}';")
    text, name, type, time, email, phone, status = product_query.fetchone()

    connect.commit()

    buttons = types.InlineKeyboardMarkup()

    left = id - 1 if id != 1 else pages_count
    right = id + 1 if id != pages_count else 1

    left_button = types.InlineKeyboardButton("←", callback_data=f'to {left}')
    page_button = types.InlineKeyboardButton(f"{str(id)} / {str(pages_count)}", callback_data='_')
    right_button = types.InlineKeyboardButton("→", callback_data=f'to {right}')
    buttons.add(left_button, page_button, right_button)
    try:
        msg = f"Название: *{name}*\nОписание: "
        msg += f"*{text}*\n" if text is not None else '_нет_\n'

        bot.send_message(message.chat.id, msg, reply_markup=buttons)

    except:
        msg = f"Название: *{name}*\nОписание: "
        msg += f"*{text}*\n" if text is not None else '_нет_\n'

        bot.send_message(message.chat.id, msg, reply_markup=buttons)

    try:
        bot.delete_message(message.chat.id, previous_message.id)

    except:
        pass


@bot.callback_query_handler(func=lambda c: True)
def callback(c):
    if 'to' in c.data:
        page = int(c.data.split(' ')[1])
        see_request(c.message, page=page, previous_message=c.message)


bot.polling(none_stop=True)
