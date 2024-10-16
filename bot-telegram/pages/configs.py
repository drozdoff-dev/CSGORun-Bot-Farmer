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

    if(command == "1. конфигурация аккаунтов."):
        info_user_tg.storage['active_page']['configs']['accounts'] = {}
    
    elif(command == "2. конфигурация поведения бота."):
        info_user_tg.storage['active_page']['configs']['actions'] = {}
        send_configs.send_config_action_bot(app_path)
    
    elif(command == "3. конфигурация ставок бота."):
        info_user_tg.storage['active_page']['configs']['bets'] = {}
        send_configs.send_config_bet_bot(app_path)
    
    elif(command == "4. конфигурация уведомлений в телеграмм."):
        info_user_tg.storage['active_page']['configs']['notifications'] = {}
        send_configs.send_config_notifications(app_path)
    

