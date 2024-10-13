import datetime

from telebot import types

import config
import user_contact

contacts = []
name = None
phone_number = None

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    add_contact_btn = types.KeyboardButton('добавить контакт')
    show_contact_btn = types.KeyboardButton('показать все контакты')

    bot.send_message(message.chat.id, 'привет! я - бот для контактов.',
                                      reply_markup=create_main_keyboard())
    bot.register_next_step_handler(message, handle_main_commands)

def handle_main_commands(message):
    #user_message  = bot.reply_to(message, 'как зовут нового контакта?')
    #bot.register_next_step_handler(user_message, process_name_step)

        if message.text == 'добавить контакт':
            #print('пользователь захотел добавить контакт')
            delete_keyboard = types.ReplyKeyboardRemove()
            bot.send_messsage(message.chat.id, 'как зовут контакта?', reply_markup=delete_keyboard)
        elif message.text == 'показать все контакты':
            bot.send_messsage(message.chat.id, 'список всех контактов')
            bot.register_next_step_handler(message, handle_main_commands)
        else:
            bot.send_messsage(message.chat.id, 'чо')
            bot.register_next_step_handler(message, handle_main_commands)
            
def process_name_step(message):
    name = message.text

    if not name:
        bot.send_message(message.chat.id, 'имя не может быть пустым!')
        bot.register_next_step_handler(message, process_name_step)
        return

    #contact_builder.add_name(name)

    bot.send_message(message.chat.id, 'номер телефона:')
    bot.register_next_step_handler(message, process_phone_number_step)

def process_phone_number_step(message):
    phone_number = message.text

    if not phone_number:
        bot.send_message(message.chat.id, 'номер телефона не может быть пустым!')
        bot.register_next_step_handler(message, process_phone_number_step)
        return

    #contact_builder.add_phone_number(name)

    keyboard = types.InlineKeyboardMarkup()

    skip_btn = types.InlineKeyboardButton(text='пропустить', callback_data='')


    bot.send_message(message.chat.id, 'описание:')
    bot.register_next_step_handler(message, process_description_step)

def process_description_step(message):
    phone_number = message.text

    if not description:
        bot.send_message(message.chat.id,
                         'контакт создан!',
                         reply_markup=create_main_keyboard())
        bot.register_next_step_handler(message, process_description_step)


bot.infinity_polling()
