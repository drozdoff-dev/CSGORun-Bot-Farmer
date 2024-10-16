import sys
from telebot import types


def call_page(app_path,command):
    sys.path.insert(1, app_path + '/storage/temp/telegram_bot')
    import info_bot_tg
    import info_user_tg

    sys.path.insert(1, app_path + '/storage/temp/global')
    import init_classes

    sys.path.insert(1, app_path + '/storage/temp/bet_bot/')
    import configs

    if(command == "1. изменить ставки по времени."):
        info_user_tg.storage['active_page']['configs']['bets']['time'] = {}
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
        btn1 = types.KeyboardButton("1. добавить ставку.")
        btn2 = types.KeyboardButton("2. изменить ставки.")
        btn3 = types.KeyboardButton("3. удалить ставку.")
        markup.add(btn1, btn2, btn3)

        text = f"1. добавить ставку.\n2. изменить ставки.\n3. удалить ставку."
        init_classes.bot_tg.send_message(text,parse_mode="Markdown",reply_markup=markup)
    elif(command == "2. изменить ставки по комбинациям."):
        info_user_tg.storage['active_page']['configs']['bets']['patterns'] = {}
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
        btn1 = types.KeyboardButton("1. добавить ставку.")
        btn2 = types.KeyboardButton("2. изменить ставки.")
        btn3 = types.KeyboardButton("3. удалить ставку.")
        markup.add(btn1, btn2, btn3)

        text = f"1. добавить ставку.\n2. изменить ставки.\n3. удалить ставку."
        init_classes.bot_tg.send_message(text,parse_mode="Markdown",reply_markup=markup)
    elif(command == "3. изменить ставки по разбавочным играм."):
        info_user_tg.storage['active_page']['configs']['bets']['dilute'] = {}
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
        btn1 = types.KeyboardButton("1. Мин. Ставку.")
        btn2 = types.KeyboardButton("2. Макс. Ставку.")
        btn3 = types.KeyboardButton("3. Мин. Коэф.")
        btn4 = types.KeyboardButton("4. Макс. Коэф.")
        markup.add(btn1, btn2, btn3, btn4)

        text = ''
        text += (f"\n*Текущая информация по разбавочным играм*\n"
                +f"```html Диапозон ставки: {configs.storage['auto_bet']['Dilute_Bet']['cost']['min']}-{configs.storage['auto_bet']['Dilute_Bet']['cost']['max']}$ на {configs.storage['auto_bet']['Dilute_Bet']['coef']['min']}-{configs.storage['auto_bet']['Dilute_Bet']['coef']['max']}x```\n")
        text += f"\nВыберите, что хотите изменить:\n1. Мин. Ставку.\n2. Макс. Ставку.\n3. Мин. Коэф.\n4. Макс. Коэф."
        init_classes.bot_tg.send_message(text,parse_mode="Markdown",reply_markup=markup)