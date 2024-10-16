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

    number_time_bet = info_user_tg.storage['args']['time_bet']['select']
    change_time = command
    try:
        change_time = time.strptime(change_time, '%H:%M')
    except ValueError:
        return init_classes.bot_tg.send_message(f'Вы ввели неверный тип данных. - {command}')
    for time_bet in configs.storage['auto_bet']['Time_Bet']:
        if(time_bet == command):
            return init_classes.bot_tg.send_message(f'Вы не можете установить время {command}, ведь уже существует ставка с таким временем.')
    for (i,time_bet) in zip(range(len(configs.storage['auto_bet']['Time_Bet'])),configs.storage['auto_bet']['Time_Bet']):
        if(i == number_time_bet-1):
            configs.storage['auto_bet']['Time_Bet'][command] = configs.storage['auto_bet']['Time_Bet'].pop(time_bet)
            info_user_tg.storage['args']['time_bet']['last_command'] = ''
            info_user_tg.storage['active_page']['configs']['bets']['time']['edit']['change'] = {}
            init_classes.bot_tg.send_message(f'Значение времени {time_bet} у ставки №{number_time_bet} изменено на {command}')
            text = f''
            text += f"Текущая информация о ставке\n```html {number_time_bet}. В {command} МСК - ставка: {configs.storage['auto_bet']['Time_Bet'][command]['cost']['min']}-{configs.storage['auto_bet']['Time_Bet'][command]['cost']['max']}$ на {configs.storage['auto_bet']['Time_Bet'][command]['coef']['min']}-{configs.storage['auto_bet']['Time_Bet'][command]['coef']['max']}x.```\n"
            text += f"\nВыберите, что хотите изменить:\n1. Время ставки.\n2. Мин. ставку.\n3. Макс. Ставку.\n4. Мин.Коэф.\n5. Макс. Коэф."
            return init_classes.bot_tg.send_message(text,parse_mode="Markdown")