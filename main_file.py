import telebot
import requests
import time
from bs4 import BeautifulSoup
from telebot import types

TOKEN = "1740563390:AAHFIQtOI7Zd7DBRPk4XAX5Ke3oMuXbRG3c"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    global id
    id = message.chat.id
    bot.send_message(id, text='Добрый день. Давайте узнаем погоду на сегодня')
    time.sleep(1.5)
    bot.send_message(id, text='Введите название города:')

@bot.message_handler(content_types=['text'])
def place(message):
    town = message.text.replace(" ", "-", 2)
    url = 'https://sinoptik.com.ru/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-' + town.lower()
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    titlec = soup.find('div', id = 'sinoptik-app').text
    title = titlec.find('404')
    if title != -1:
        bot.send_message(id, text='Я тебя не понимаю, введи другой город')
    else:
        global temp, pres, cloud
        temp = soup.find('div', class_='weather__article_main_temp').text
        cur = soup.find('div', class_='table__col current')
        pres = cur.find('div', class_='table__pressure').text
        cloud = soup.find('div', class_='weather__article_description-text').text

        if message.chat.type == 'private':
            markup = types.InlineKeyboardMarkup(row_width=1)
            temperatura = types.InlineKeyboardButton("Температура", callback_data='temperature')
            pressure = types.InlineKeyboardButton("Давление", callback_data='pressure')
            clouds = types.InlineKeyboardButton("Осадки", callback_data='clouds')
            city = types.InlineKeyboardButton("К выбору города", callback_data='city')
            clothes = types.InlineKeyboardButton("Что же мне надеть?", callback_data='clothes')
            markup.add(temperatura, pressure, clouds, clothes, city)
            bot.send_message(id, "Что именно вы хотите узнать?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def step_four(call):
    try:
        if call.message:
            id1 = call.message.chat.id
            if call.data == 'temperature':
                bot.send_message(id1, f'Температура в вашем городе сегодня: {temp[1:6]}🌡')
            elif call.data == 'pressure':
                bot.send_message(id1, f'Давление в заданном месте: {pres} мм.рт.ст.')
                if (int(pres) > 760):
                    bot.send_message(id1, 'Не пейте кофе и отдыхайте 😴')
                elif (int(pres) < 750):
                    bot.send_message(id1, 'Выпейте кофе или чай и отдыхайте☕')
            elif call.data == 'clothes':
                bot.send_message(id1, 'Думаем над выбором одежды... 🤔')
                if (int(temp[2:-3])) >= 40:
                    bot.send_message(id1, 'Блин... Живи))) Мы не знаем, что тебе посоветовать. Ходи по улице в купальнике и используй spf 🥵')
                    bot.send_photo(id1, 'https://drive.google.com/file/d/1s2VLqk-LvlOWtufrqPvJpsYvh4ywZEda/view?usp=sharing')
                elif (int(temp[2:-3])) < 40 and (int(temp[2:-3])) >= 20:
                    bot.send_message(id1, 'Довольно жарко, так что футболочки, маечки, шорты, юбки в твоем распоряжении 👕')
                    bot.send_photo(id1, 'https://drive.google.com/file/d/1i6nJ6F7iOkLdN4zxccBieXRG87fEXwF7/view?usp=sharing')
                elif (int(temp[2:-3])) < 20 and (int(temp[2:-3])) >= 15:
                    bot.send_message(id1, 'Чуть прохладно, можешь, конечно, рискнуть и надеть футболку, но лучше взять какуе-нибудь легкую куртень или кофту👔')
                    bot.send_photo(id1, 'https://drive.google.com/file/d/1Q-wrh7_Mh52ehYh6MdIWBdJ3JenXenik/view?usp=sharing')
                elif (int(temp[2:-3])) < 15 and (int(temp[2:-3])) >= 8:
                    bot.send_message(id1, 'Надень какой-нибудь плащ и водолазку, настроение: осень 24/7 🧤')
                    bot.send_photo(id1, 'https://drive.google.com/file/d/1YeWnqUoul--7CJlSAik5Zxq84PI2_sRS/view?usp=sharing')
                elif (int(temp[2:-3])) < 8 and (int(temp[2:-3])) >= 0:
                    bot.send_message(id1, 'Так, ну тут как бы холодно, особо в толстовке не побегаешь. Пальто б надеть, а то задубеть можно 🧣')
                    bot.send_photo(id1, 'https://drive.google.com/file/d/1Pb3kafw1-7tKhcSQtaEoMTHRuMZ93AUj/view?usp=sharing')
                elif (int(temp[2:-3])) < 0 and (int(temp[2:-3])) >= -20:
                    bot.send_message(id1, 'Так, ну все, зима здесь. Одевайся теплее, если выходишь на улицу. А вообще, не выходи из комнаты, не совершай ошибку 🧥')
                    bot.send_photo(id1, 'https://drive.google.com/file/d/1WMN9ruB3iqOEDnJnilzM4CMXn8v3sIHu/view?usp=sharing')
                elif (int(temp[2:-3])) < -20:
                    bot.send_message(id1, '... Плохие новости, на улице апокалипсис. ОЧЕНЬ холодно. Лучше сидеть дома, отпаивать себя чаем, греться в пледах и с помощью радиатора. Чтобы выйти на улицу, тебе надо будет стать капустой 🥶')
                    bot.send_photo(id1, 'https://drive.google.com/file/d/12iyBxL1BOU_TGL6-StHCW2jhKhHqIGFL/view?usp=sharing')
                if ("пасмурно" in cloud.lower()) or ("дожд" in cloud.lower()) or ("гроз" in cloud.lower()) or ("туман" in cloud.lower()):
                    bot.send_message(id1, 'Возьми зонт и надень что-нибудь непромокаемое. Чувствуется, что сегодня будет мокро на улице 🌧')
                    bot.send_photo(id1, 'https://drive.google.com/file/d/13zNR0XTP85I7nEmrFw2G7jXSfmpf2W5t/view')
                elif ("обла" in cloud.lower()):
                    bot.send_message(id1, 'Сегодня облачно. Честно, делай, как знаешь: хочешь - бери зонт, не хочешь - не бери🌥')
                elif ("ясн" in cloud.lower()) or ("солн" in cloud.lower()):
                    bot.send_message(id1, 'Позаботься о глазках и надень очки, котенок😎')
                    bot.send_photo(id1, 'https://drive.google.com/file/d/1t-dmrgW8fMt_cfEv-XzCRMjBKXrzGeJ6/view?usp=sharing')
            elif call.data == 'clouds':
                bot.send_message(id1, 'Смотрим в небо...')
                time.sleep(2)
                bot.send_message(id1, f'{cloud}')
            elif call.data == 'city':
                bot.send_message(id1, 'Хорошо, выберем другой город')
                time.sleep(1)
                bot.send_message(id1, 'Введите название города 🌆')

    except Exception as e:
        print(repr(e))

bot.polling(none_stop=True)
