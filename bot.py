import datetime

import telebot
from telebot import types

import config
import user_contact
import contact_book


contact_builder = contact_book.ContactBuilder()
bot = telebot.TeleBot(config.token)

def create_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    add_contact_btn = types.KeyboardButton('добавить контакт')
    show_contact_btn = types.KeyboardButton('показать все контакты')
    keyboard.add(add_contact_btn, show_contact_btn)

    return keyboard

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'привет! я - бот для контактов.',
                                      reply_markup=create_main_keyboard())
    bot.register_next_step_handler(message, handle_main_commands)

def handle_main_commands(message):
    #user_message  = bot.reply_to(message, 'как зовут нового контакта?')
    #bot.register_next_step_handler(user_message, process_name_step)

    if message.text == 'добавить контакт':
        #print('пользователь захотел добавить контакт')
        delete_keyboard = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, 'как зовут контакта?', reply_markup=delete_keyboard)
        bot.register_next_step_handler(message, process_name_step)
    elif message.text == 'показать все контакты':
        contacts = contact_builder.get_contacts(message.chat.id)
        print(f"Кол-во контактов: {len(contacts)}")
        if len(contacts) > 0:
            bot.send_message(message.chat.id, 'список всех контактов:')
            for contact in contacts:
                bot.send_message(message.chat.id, str(contact))
        else:
            bot.send_message(message.chat.id, 'список контактов пуст')

        bot.register_next_step_handler(message, handle_main_commands)
    else:
        bot.send_message(message.chat.id, 'чо')
        bot.register_next_step_handler(message, handle_main_commands)
            
def process_name_step(message):
    name = message.text

    if not name:
        bot.send_message(message.chat.id, 'имя не может быть пустым!')
        bot.register_next_step_handler(message, process_name_step)
        return

    contact_builder.add_name(message.chat.id, name)

    bot.send_message(message.chat.id, 'номер телефона:')
    bot.register_next_step_handler(message, process_phone_number_step)

def process_phone_number_step(message):
    phone_number = message.text

    if not phone_number:
        bot.send_message(message.chat.id, 'номер телефона не может быть пустым!')
        bot.register_next_step_handler(message, process_phone_number_step)
        return

    contact_builder.add_phone_number(message.chat.id, phone_number)

    keyboard = types.InlineKeyboardMarkup()

    skip_btn = types.InlineKeyboardButton(text='пропустить', callback_data='')


    bot.send_message(message.chat.id, 'описание:')
    bot.register_next_step_handler(message, process_description_step)

def process_description_step(message):
    description = message.text

    contact_builder.add_description(message.chat.id, description)
    contact_builder.build(message.chat.id)
    
    bot.send_message(message.chat.id,
                    'контакт создан!',
                    reply_markup=create_main_keyboard())
    
    bot.register_next_step_handler(message, handle_main_commands)

    
bot.infinity_polling()
