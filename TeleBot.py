import telebot
from telebot import types
import datetime
from Results import Score
from Token import TOKEN


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['Hello', 'start'])
def message(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text='Да', callback_data="Yes")
    button2 = types.InlineKeyboardButton(text='Нет', callback_data="No")
    markup.add(button1, button2)
    bot.send_message(message.chat.id, "Добрый день!\nПоказать результаты?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call:True)
def main(call):
    if call.data == "Yes":
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text='Футбол', callback_data="football")
        button2 = types.InlineKeyboardButton(text='Хоккей', callback_data="hockey")
        button3 = types.InlineKeyboardButton(text='Баскетбол', callback_data="basketball")
        button4 = types.InlineKeyboardButton(text='Гандбол', callback_data="handball")
        markup.add(button1, button2)
        markup.add(button3, button4)
        bot.send_message(call.message.chat.id, "Какой вид спорта Вас интересует?", reply_markup=markup)

    elif call.data == "No":
        bot.send_message(call.message.chat.id, "Goodbye")

    elif call.data == "football" or call.data == "hockey" or call.data == "basketball" or call.data == "handball":
        global sport
        sport = call.data
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text='Сегодня', callback_data="Today")
        markup.add(button1)
        bot.send_message(call.message.chat.id, "Введите дату в формате:\nДД-ММ-ГГГГ", reply_markup=markup)

    elif call.data == "Today":
        global score
        global score_live
        date = "-".join(reversed(str(datetime.datetime.now().date()).split("-")))
        score, score_live = Score(sport=sport, date=date)
        results = "Какая лига Вас интересует?"+ "\n" + "\n" + '\n'.join(score.keys())
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text='Показать Live матчи', callback_data="Live")
        markup.add(button1)
        bot.send_message(call.message.chat.id, results, reply_markup=markup)

    elif call.data == "Live":
        res_live = ''
        for key in score_live.keys():
            res_live += key + '\n' + '\n' + score_live[key] + '\n'
        bot.send_message(call.message.chat.id, res_live)


@bot.message_handler(content_types="text")
def results(message):

    if message.text == "Начать" or message.text == "Добрый день" or message.text == "Привет" or message.text == "Старт":
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text='Да', callback_data="Yes")
        button2 = types.InlineKeyboardButton(text='Нет', callback_data="No")
        markup.add(button1, button2)
        bot.send_message(message.chat.id, "Добрый день!\nПоказать результаты?", reply_markup=markup)

    elif len(message.text.split('-')) == 3 or len(message.text.split('.')) == 3:
        global score
        global score_live
        date = message.text if len(message.text.split('-')) == 3 else "-".join(message.text.split('.'))
        score, score_live = Score(sport, date)
        results = "Какая лига Вас интересует?"+ "\n" + "\n" + '\n'.join(score.keys())
        bot.send_message(message.chat.id, results)

    elif message.text in score:
        bot.send_message(message.chat.id, score[message.text])

    else:
        bot.send_message(message.chat.id, "Такой лиги нет\nПопробуйте еще раз:")


bot.polling(none_stop=True)