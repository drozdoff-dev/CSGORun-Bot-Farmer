import sys
import time
from telebot import types


def call_page(app_path,command):
    sys.path.insert(1, app_path + '/storage/temp/telegram_bot')
    import info_bot_tg
    import info_user_tg

    sys.path.insert(1, app_path + '/storage/temp/global')
    import init_classes

    sys.path.insert(1, app_path + '/storage/temp/bet_bot/')
    import configs

    info_user_tg.storage['args']['pattern_bet']['coef_max'] = 0.0
    create_coef_min = command
    try:
        create_coef_min = float(create_coef_min)
    except ValueError:
        return init_classes.bot_tg.send_message(f'Вы ввели неверный тип данных. - {create_coef_min}')
    if(create_coef_min >= 1.01):
        info_user_tg.storage['active_page']['configs']['bets']['patterns']['add']['min_cost']['max_cost']['min_coef']['max_coef'] = {}
        info_user_tg.storage['args']['pattern_bet']['coef_min'] = create_coef_min
        init_classes.bot_tg.send_message(f'Введите максимальный размер коэффицента')
    else:
        text = f"Значение коэффициента должно быть больше или равно 1.01x"
        return init_classes.bot_tg.send_message(text,parse_mode="Markdown")