import telebot
import sqlite3
import os
import schedule
import time
import datetime

'''Бот для напоминания, сколько дней осталось до моего др
Можно и для других напоминалок использовать
Имя: remind_me
For search: remind_24bot
'''

bot = telebot.TeleBot('1809111381:AAE5G0h0s3lGm34Yms76blMVynE_H8xjcoA')


@bot.message_handler(content_types=['text'])
def send_echo(message):
    connect = sqlite3.connect('remind_bot.db')

    cursor = connect.cursor()

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS for_reminded (
                id INTEGER,
                city TEXT,
                name TEXT,
                last_name TEXT,
                user_name TEXT
            )
        """)

    connect.commit()
    print(message)

    # add values
    user_id = message.from_user.id
    text_1 = message.text
    name_1 = message.from_user.first_name
    last_1 = message.from_user.last_name
    username_1 = message.from_user.username

    cursor.execute('INSERT INTO for_reminded VALUES(?, ?, ?, ?, ?);', (user_id, text_1, name_1, last_1, username_1))

    connect.commit()

    answer = 'Здравствуйте. Я бот напоминатель. Приступаю к работе!'
    bot.send_message(message.from_user.id, answer)

    # hack = 'Пользователь ' + message.from_user.username + ' отправил мне запрос: ' + message.text
    # bot.send_message(596834788, hack)

    # if message.text.lower() == 'фото алматы':
    #     photo = open('images/almaty.jpg', 'rb')
    #     bot.send_photo(chat_id=message.from_user.id, photo=photo)

    def job():
        current_date = datetime.datetime.now()

        target_date = datetime.datetime(2022, 6, 27, 00, 00, 00)

        difference_time = target_date - current_date
        str_time = str(difference_time)
        list_time = str_time.split()
        list_time.remove(list_time[1])
        # print(list_time)
        days_dif = list_time[0]
        # ['349', '3:59:11.195300']
        list_hours_min = list_time[1].split(':')
        hours_dif, min_dif = list_hours_min[0], list_hours_min[1]
        # ['3', '57', '15.000121']
        seconds_time = list_hours_min[2].split('.')
        sec_time = int(seconds_time[0])
        diff_text = 'До ухода в Алмату осталось ' + days_dif + 'дней, ' + hours_dif + 'часов, ' + min_dif + 'минут' + str(sec_time) + 'секунд. Хозяин, ты обязательно достигнешь своей цели стать Python разработчиком.'
        bot.send_message(message.from_user.id, diff_text)

    def schedule_for_bot():
        # schedule.every(10).seconds.do(job)
        schedule.every().day.at("02:57").do(job)
        # schedule.every().day.at("00:22").do(job)
        schedule.cancel_job(job)

    schedule_for_bot()

    while True:
        schedule.run_pending()
        time.sleep(1)


bot.polling(none_stop=True)




