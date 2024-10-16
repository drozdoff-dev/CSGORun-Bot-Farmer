import sys
from threading import Thread
from telebot import types


def call_page(app_path,command):
    sys.path.insert(1, app_path + '/bot-auth')
    import auth_bot

    sys.path.insert(1, app_path + '/bot-telegram/functions')
    import send_configs

    sys.path.insert(1, app_path + '/storage/temp/telegram_bot')
    import info_bot_tg
    import info_user_tg

    sys.path.insert(1, app_path + '/storage/temp/global')
    import init_classes

    guard = command.upper()
    auth = auth_bot.auth_user(app_path,guard)
    #t_auth_user = Thread(target=auth_bot.auth_user,kwargs={'app_path':app_path,'guard':guard})
    #t_auth_user.daemon = True
    #t_auth_user.start()