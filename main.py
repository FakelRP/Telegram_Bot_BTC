import requests
from datetime import datetime
import telebot
from telebot import types
from auth_data import token


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    def crypto_price(message, crypto):
        try:
            req = requests.get(f"https://yobit.net/api/3/ticker/{crypto}_usd")
            response = req.json()
            sell_price = response[f"{crypto}_usd"]["sell"]
            bot.send_message(
                message.chat.id,
                f"{datetime.now().strftime('%Y-%m-%d %H:%M')}\nЦена продажи {crypto.upper()}: {sell_price} $"
                             )
        except Exception as ex:
            print(ex)
            bot.send_message(
                message.chat.id,
                "Произошла ошибка"
            )

    @bot.message_handler(commands=['start'])
    def button_message(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Выбрать крипту")
        btn2 = types.KeyboardButton("Привет")
        btn3 = types.KeyboardButton("Задать вопрос")
        markup.add(btn1, btn2, btn3)
        bot.send_message(message.chat.id,
                         "Привет, {0.first_name}! Нажми на интересующую тебя кнопку. Для того, чтобы узнать цену крипты нажми на кнопку 'Выбрать крипту'".format(message.from_user),
                         reply_markup=markup)

    @bot.message_handler(content_types=["text"])
    def send_text(message):
        if message.text == "Выбрать крипту":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btc_btn = types.KeyboardButton("BTC")
            eth_btn = types.KeyboardButton("ETH")
            doge_btn = types.KeyboardButton("DOGE")
            ltc_btn = types.KeyboardButton("LTC")
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(btc_btn, eth_btn, doge_btn, ltc_btn, back)
            bot.send_message(message.chat.id, text="Выбери криптовалюту, цену которой хочешь узнать!", reply_markup=markup)

        elif message.text == "BTC":
            crypto_price(message, 'btc')

        elif message.text == "ETH":
            crypto_price(message, 'eth')

        elif message.text == "DOGE":
            crypto_price(message, 'doge')

        elif message.text == "LTC":
            crypto_price(message, 'ltc')

        elif message.text == "Привет":
            bot.send_message(message.chat.id, text="Привет! Я помогу тебе узнать цену криптовалют.")

        elif message.text == "Задать вопрос":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Как меня зовут?")
            btn2 = types.KeyboardButton("Что я могу?")
            back = types.KeyboardButton("Вернуться в главное меню")
            markup.add(btn1, btn2, back)
            bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)

        elif message.text == "Как меня зовут?":
            bot.send_message(message.chat.id, "У меня нет имени..")

        elif message.text == "Что я могу?":
            bot.send_message(message.chat.id, text="Могу показать цену криптовалют")

        elif message.text == "Вернуться в главное меню":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton("Выбрать крипту")
            button2 = types.KeyboardButton("Привет")
            button3 = types.KeyboardButton("Задать вопрос")
            markup.add(button1, button2, button3)
            bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)

        else:
            bot.send_message(message.chat.id, "Проверь команду")

    bot.polling(none_stop=True)


if __name__ == '__main__':
    telegram_bot(token)
