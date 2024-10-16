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

    info_user_tg.storage['args']['time_bet']['cost_min'] = 0.0
    create_time = command
    try:
        create_time = time.strptime(create_time, '%H:%M')
    except ValueError:
        return init_classes.bot_tg.send_message(f'Вы ввели неверный тип данных. - {create_time}')
    for time_bet in configs.storage['auto_bet']['Time_Bet']:
        if(command == time_bet):
            return init_classes.bot_tg.send_message(f'Ставка по данному времени уже существует. - {command}')
    info_user_tg.storage['args']['time_bet']['time'] = command
    info_user_tg.storage['active_page']['configs']['bets']['time']['add']['min_cost'] = {}
    init_classes.bot_tg.send_message(f'Введите минимальный размер ставки')