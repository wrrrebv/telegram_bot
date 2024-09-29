from random import choice

from telebot import TeleBot, types

from config import TOKEN

def who_won(user_input:str, bot_input: str) -> str:
    user_inpot = user_input.lower()
    bot_input = bot_input.lower()

    if user_input == bot_input:
        return 'nobody'
    elif user_input == 'камень' and bot_input == 'ножницы' \
            or user_input == 'бумага' and bot_input == 'камень' \
            or user_input == 'ножницы' and bot_input == 'бумага':
        return 'user'

    return 'bot'

def generate_bot_answer():
    choices = ['камень','ножницы','бумага']
    return choice(choices)


bot = TeleBot(token=TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    rock_btn= types.KeyboardButton('камень')
    scissors_btn= types.KeyboardButton('ножницы')
    paper_btn= types.KeyboardButton('бумага')
    markup.add(rock_btn, scissors_btn, paper_btn)

    bot.send_message(message.chat.id, 
                    'привет! предлагаю сыграть в камень-ножницы-бумага, выбирай:',
                    reply_markup=markup)

    bot.register_next_step_handler(message, game)


def game(message):
    user_input = message.text
    bot_input = generate_bot_answer()

    winner = who_won(user_input, bot_input)
    if winner == 'nobody':
        bot_response = 'ничья!'
    elif winner == 'user':
        bot_response = f'поздравляю с победой! я загадал: {bot_input}'
    else:
        bot_response = f'ты проиграл, я загадал {bot_input}'


    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    play_again = types.KeyboardButton('/start')
    markup.add(play_again)

    bot.send_message(message.chat.id, bot_response, reply_markup=markup)


bot.infinity_polling()