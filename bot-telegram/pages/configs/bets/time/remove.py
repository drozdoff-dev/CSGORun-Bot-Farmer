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

    number_time_bet = command
    try:
        number_time_bet = int(number_time_bet)
    except ValueError:
        return init_classes.bot_tg.send_message(f'Вы ввели неверный тип данных. - {number_time_bet}')
    if(number_time_bet > 0):
        if(len(configs.storage['auto_bet']['Time_Bet']) >= number_time_bet):
            for (i,time_bet) in zip(range(len(configs.storage['auto_bet']['Time_Bet'])),configs.storage['auto_bet']['Time_Bet']):
                if(i+1 == number_time_bet):
                    info_user_tg.storage['active_page']['configs']['bets']['time'] = {}
                    info_user_tg.storage['args']['time_bet']['last_command'] = ''
                    text = f"```html {number_time_bet}. В {time_bet} МСК - ставка: {configs.storage['auto_bet']['Time_Bet'][time_bet]['cost']['min']}-{configs.storage['auto_bet']['Time_Bet'][time_bet]['cost']['max']}$ на {configs.storage['auto_bet']['Time_Bet'][time_bet]['coef']['min']}-{configs.storage['auto_bet']['Time_Bet'][time_bet]['coef']['max']}x.``` - была удалена.\n"
                    init_classes.bot_tg.send_message(text,parse_mode="Markdown",reply_markup=markup)
                    
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
                    btn1 = types.KeyboardButton("1. добавить ставку.")
                    btn2 = types.KeyboardButton("2. изменить ставки.")
                    btn3 = types.KeyboardButton("3. удалить ставку.")
                    markup.add(btn1, btn2, btn3)

                    text = f"1. добавить ставку.\n2. изменить ставки.\n3. удалить ставку."
                    init_classes.bot_tg.send_message(text,parse_mode="Markdown",reply_markup=markup)
                    configs.storage['auto_bet']['Time_Bet'].pop(time_bet)
                    init_classes.bot_tg.send_message(text,parse_mode="Markdown")
                    return send_configs.send_config_bet_bot(app_path)
        else:
            text = f"такой игры не существует"
            return init_classes.bot_tg.send_message(text,parse_mode="Markdown")
    else:
        text = f"число должно быть положительное"
        return init_classes.bot_tg.send_message(text,parse_mode="Markdown")