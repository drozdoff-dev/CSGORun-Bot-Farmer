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

    if(command == "1. время ставки."):
        info_user_tg.storage['active_page']['configs']['bets']['time']['edit']['change']['time'] = {}
        init_classes.bot_tg.send_message(f"Впишите время на которое желаете изменить в формате 'HH:MM'.")
    elif(command == "2. мин. ставку."):
        info_user_tg.storage['active_page']['configs']['bets']['time']['edit']['change']['min_cost'] = {}
        init_classes.bot_tg.send_message(f"Впишите минимальную ставку ботом от 0.01.")
    elif(command == "3. макс. cтавку."):
        info_user_tg.storage['active_page']['configs']['bets']['time']['edit']['change']['max_cost'] = {}
        init_classes.bot_tg.send_message(f"Впишите максимальную ставку ботом от Мин. ставки.")
    elif(command == "4. мин. коэф."):
        info_user_tg.storage['active_page']['configs']['bets']['time']['edit']['change']['min_coef'] = {}
        init_classes.bot_tg.send_message(f"Впишите минимальный коэффициент ставки от 1.01.")
    elif(command == "5. макс. коэф."):
        info_user_tg.storage['active_page']['configs']['bets']['time']['edit']['change']['max_coef'] = {}
        init_classes.bot_tg.send_message(f"Впишите максимальный коэффициент ставки от Мин. коэффициента.")
    else:
        print()