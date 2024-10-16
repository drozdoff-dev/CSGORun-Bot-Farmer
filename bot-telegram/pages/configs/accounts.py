import sys


def call_page(app_path):
    sys.path.insert(1, app_path + '/storage/temp/telegram_bot/')
    import info_bot_tg
    import info_user_tg

    info_user_tg.storage['active_page']['configs']['accounts']['create'] = {}
    print('3')