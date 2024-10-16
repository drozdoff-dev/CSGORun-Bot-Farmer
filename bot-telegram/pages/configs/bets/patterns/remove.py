import sys
from telebot import types

def call_page(app_path,command):
    sys.path.insert(1, app_path + '/bot-telegram/functions')
    import send_configs

    sys.path.insert(1, app_path + '/storage/temp/telegram_bot')
    import info_bot_tg
    import info_user_tg

    sys.path.insert(1, app_path + '/storage/temp/global')
    import init_classes

    sys.path.insert(1, app_path + '/storage/temp/bet_bot/')
    import configs

    number_pattern_bet = command
    try:
        number_pattern_bet = int(number_pattern_bet)
    except ValueError:
        return init_classes.bot_tg.send_message(f'Вы ввели неверный тип данных. - {number_pattern_bet}')
    if(number_pattern_bet > 0):
        if(len(configs.storage['auto_bet']['Pattern_Bet']['patterns']) >= number_pattern_bet):
            for (i,pattern_bet) in zip(range(len(configs.storage['auto_bet']['Pattern_Bet']['patterns'])),configs.storage['auto_bet']['Pattern_Bet']['patterns']):
                if(i+1 == number_pattern_bet):
                    info_user_tg.storage['active_page']['configs']['bets']['patterns'] = {}
                    info_user_tg.storage['args']['pattern_bet']['last_command'] = ''
                    text += f"```html {i+1}. {pattern_bet} - ставка: {configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_bet]['cost']['min']}-{configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_bet]['cost']['max']}$ на {configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_bet]['coef']['min']}-{configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_bet]['coef']['max']}x.``` - была удалена\n"
                    init_classes.bot_tg.send_message(text,parse_mode="Markdown",reply_markup=markup)
                    
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
                    btn1 = types.KeyboardButton("1. добавить ставку.")
                    btn2 = types.KeyboardButton("2. изменить ставки.")
                    btn3 = types.KeyboardButton("3. удалить ставку.")
                    markup.add(btn1, btn2, btn3)

                    text = f"1. добавить ставку.\n2. изменить ставки.\n3. удалить ставку."
                    init_classes.bot_tg.send_message(text,parse_mode="Markdown",reply_markup=markup)
                    configs.storage['auto_bet']['Pattern_Bet']['patterns'].pop(pattern_bet)
                    init_classes.bot_tg.send_message(text,parse_mode="Markdown")
                    return send_configs.send_config_bet_bot(app_path)
        else:
            text = f"такой игры не существует"
            return init_classes.bot_tg.send_message(text,parse_mode="Markdown")
    else:
        text = f"число должно быть положительное"
        return init_classes.bot_tg.send_message(text,parse_mode="Markdown")