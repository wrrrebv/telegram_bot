import telebot
import datetime
import config

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def handle_message(message):
    bot.send_message(message.chat.id,"привет!" )

@bot.message_handler(commands=['current_time', 'time', 'now'])
def current_time(message):
    now = datetime.datetime.now()
    output_message = f'{now.year} год, сентябрь, {now.day} число'
    bot.send_message(message.chat.id, output_message)

bot.infinity_polling()