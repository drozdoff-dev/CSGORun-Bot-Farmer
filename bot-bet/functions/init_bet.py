import configparser
from datetime import date
import json
import sys
import time


def config(app_path,id_message,text_message):
    sys.path.insert(1, app_path + '/storage/temp/bot_bet/')
    import configs
    sys.path.insert(1, app_path + '/bot-bet/functions')
    import notifications
    sys.path.insert(1, app_path + '/storage/temp/global')
    import init_classes
    sys.path.insert(1, app_path + '/storage/temp/telegram_bot/')
    import info_bot_tg
    import info_user_tg

    notifications.log_console('debug','-------Загрузка конфигурации-------')
    text_message += "\n-------Загрузка конфигурации-------"
    init_classes.bot_tg.edit_message(id_message,text_message)

    notifications.log_console('debug','Открытие auto_bet.json...')
    text_message += "\nОткрытие auto_bet.json..."
    init_classes.bot_tg.edit_message(id_message,text_message)

    with open(app_path + '/config/auto_bet.json','r+') as bet_cfg:
        configs.storage['auto_bet'] = json.load(bet_cfg)
        notifications.log_console('debug','auto_bet.json иницилизирован')
        text_message += "\nauto_bet.json иницилизирован"
        init_classes.bot_tg.edit_message(id_message,text_message)
    notifications.log_console('debug','Открытие accounts.json...')
    with open(app_path + '/config/accounts.json','r+') as acc_cfg:
        configs.storage['accounts'] = json.load(acc_cfg)
        notifications.log_console('debug','accounts.json иницилизирован')
        text_message += "\naccounts.json иницилизирован"
        init_classes.bot_tg.edit_message(id_message,text_message)

    notifications.log_console('debug','Чтение config.cfg...')
    text_message += "\nЧтение config.cfg..."
    init_classes.bot_tg.edit_message(id_message,text_message)
    config = configparser.ConfigParser()
    config.read_file(open(app_path + '/config/config.cfg'))

    notifications.log_console('debug','Чтение раздела MAIN')
    text_message += "\nЧтение раздела MAIN"
    init_classes.bot_tg.edit_message(id_message,text_message)
    configs.storage['main']['active_account'] = config.get('MAIN', 'active_account')

    with open(app_path + '/storage/temp/global/auth_info.json','r+') as auth_info:
        auth_info = json.load(auth_info)
        if(auth_info['active_account'] != config.get('MAIN', 'active_account')):
            notifications.log_console('info',f"Выбранный вами активный аккаунт отличается от прошлого, поэтому необходимо провести авторизацию.")
            info_user_tg.storage['active_page']['auth_csgorun'] = {}
            init_classes.bot_tg.send_message(f"Выбранный вами активный аккаунт отличается от прошлого, поэтому необходимо провести авторизацию.\nВведите ниже Steam Guard - {config.get('MAIN', 'active_account')}, чтобы я мог произвести авторизацию.")
        else:
            if(auth_info['token'] == "" or auth_info['cookie'] == ""):
                notifications.log_console('info',f"Токен или куки отсутстует, поэтому необходимо провести авторизацию по аккаунту заново.")
                info_user_tg.storage['active_page']['auth_csgorun'] = {}
                init_classes.bot_tg.send_message(f"Токен или куки отсутстует, поэтому необходимо провести авторизацию по аккаунту заново.\nВведите ниже Steam Guard - {config.get('MAIN', 'active_account')}, чтобы я мог произвести авторизацию.")

        while('auth_csgorun' in info_user_tg.storage['active_page']):
            time.sleep(1)

        with open(app_path + '/storage/temp/global/auth_info.json','r+') as auth_info:
            auth_info = json.load(auth_info)

        auth_info['active_account'] = config.get('MAIN', 'active_account')
        configs.storage['accounts'][configs.storage['main']['active_account']]['cookie'] = auth_info['cookie']
        configs.storage['accounts'][configs.storage['main']['active_account']]['token'] = auth_info['token']

        with open(app_path + '/storage/temp/global/auth_info.json', 'w', encoding='utf-8') as auth_info_write:
            json.dump(auth_info, auth_info_write, ensure_ascii=False, indent=4)

    notifications.log_console('debug','Чтение раздела BOT-Start')
    text_message += "\nЧтение раздела BOT-Start"
    init_classes.bot_tg.edit_message(id_message,text_message)
    configs.storage['bot-start']['wait_crash'] = config.get('BOT-Start', 'wait_crash_by_start')
    configs.storage['bot-start']['skip_min'] = int(config.get('BOT-Start', 'count_skips_rounds_after_crash_by_start_min'))
    configs.storage['bot-start']['skip_max'] = int(config.get('BOT-Start', 'count_skips_rounds_after_crash_by_start_max'))

    notifications.log_console('debug','Чтение раздела BOT-Dilute')
    text_message += "\nЧтение раздела BOT-Dilute"
    init_classes.bot_tg.edit_message(id_message,text_message)
    configs.storage['bot-dilute']['pause_by_crash'] = config.get('BOT-Dilute', 'pause_by_crash') #пауза при краше
    configs.storage['bot-dilute']['pause_by_lose'] = config.get('BOT-Dilute', 'pause_by_lose') #пауза при проигрыше
    configs.storage['bot-dilute']['wait_crash_row'] = config.get('BOT-Dilute', 'wait_crash_after_row') #ожидание краша после длинной линии
    configs.storage['bot-dilute']['skip_rounds_row'] = config.get('BOT-Dilute', 'skip_rounds_after_row') #пропуск раундов после длинной линии
    configs.storage['bot-dilute']['pause_min'] = int(config.get('BOT-Dilute', 'count_pause_rounds_crash_min')) #пропуск раундов после краша 
    configs.storage['bot-dilute']['pause_max'] = int(config.get('BOT-Dilute', 'count_pause_rounds_crash_max')) #
    configs.storage['bot-dilute']['rounds_min'] = int(config.get('BOT-Dilute', 'count_min_dilute_rounds')) #количество раундов в кругу до ожидания паттерна
    configs.storage['bot-dilute']['rounds_max'] = int(config.get('BOT-Dilute', 'count_max_dilute_rounds')) #
    configs.storage['bot-dilute']['row_min'] = int(config.get('BOT-Dilute', 'count_min_dilute_row_rounds')) #количество ставок подряд
    configs.storage['bot-dilute']['row_max'] = int(config.get('BOT-Dilute', 'count_max_dilute_row_rounds')) #
    configs.storage['bot-dilute']['skip_row_min'] = int(config.get('BOT-Dilute', 'count_min_dilute_skip_by_row_rounds')) #пропуск раундов после лимита линии ставок
    configs.storage['bot-dilute']['skip_row_max'] = int(config.get('BOT-Dilute', 'count_max_dilute_skip_by_row_rounds')) #

    notifications.log_console('debug','Чтение раздела BOT-Patterns')
    text_message += "\nЧтение раздела BOT-Patterns"
    init_classes.bot_tg.edit_message(id_message,text_message)
    configs.storage['bot-patterns']['search_by_dilute'] = config.get('BOT-Patterns', 'search_pattern_by_dilute')
    configs.storage['bot-patterns']['wait_after_pattern'] = config.get('BOT-Patterns', 'wait_after_pattern') #продолжать ожидание после найденного паттерна
    configs.storage['bot-patterns']['wait_seconds_min'] = int(config.get('BOT-Patterns', 'wait_pattern_in_seconds_min'))
    configs.storage['bot-patterns']['wait_seconds_max'] = int(config.get('BOT-Patterns', 'wait_pattern_in_seconds_max'))

    #notifications.log_console('debug','Чтение раздела BOT-Time')
    #configs.storage['bot-time'][''] = config.get('BOT-Time', '')

    notifications.log_console('debug',f'Запись сегодняшней даты - {date.today()}')
    text_message += f'\nЗапись сегодняшней даты - {date.today()}'
    init_classes.bot_tg.edit_message(id_message,text_message)
    configs.storage['today'] = date.today()
    notifications.log_console('debug','-------Конфигурация загружена!-------\n')
    text_message += f'\n-------Конфигурация загружена!-------'
    init_classes.bot_tg.edit_message(id_message,text_message)