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

    info_user_tg.storage['args']['pattern_bet']['coef_min'] = 0.0
    create_cost_max = command
    try:
        create_cost_max = float(create_cost_max)
    except ValueError:
        return init_classes.bot_tg.send_message(f'Вы ввели неверный тип данных. - {create_cost_max}')
    if(create_cost_max >= 0.1):
        if(create_cost_max >= info_user_tg.storage['args']['pattern_bet']['cost_min']):
            info_user_tg.storage['active_page']['configs']['bets']['patterns']['add']['min_cost']['max_cost']['min_coef'] = {}
            info_user_tg.storage['args']['pattern_bet']['cost_max'] = create_cost_max
            init_classes.bot_tg.send_message(f'Введите минимальный размер коэффицента')
        else:
            return init_classes.bot_tg.send_message(f"Максимальная ставка должна быть больше или равна минимальной. - {info_user_tg.storage['args']['pattern_bet']['cost_min']}")
    else:
        text = f"Значение ставки должно быть больше или равно 0.1$"
        return init_classes.bot_tg.send_message(text,parse_mode="Markdown")