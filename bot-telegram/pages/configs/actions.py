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

    names_change_conf = {
        1: "[Поведение бота при запуске][Ожидание краша]",
        2: "[Поведение бота при запуске][Мин. Ожидание после краша]",
        3: "[Поведение бота при запуске][Макс. Ожидание после краша]",
        4: "[Краш/Проигрыш][Ожидание при краше]",
        5: "[Краш/Проигрыш][Ожидание при проигрыше]",
        6: "[Краш/Проигрыш][Мин. ожидание при краше/проигрыше]",
        7: "[Краш/Проигрыш][Макс. ожидание при краше/проигрыше]",
        8: "[Ставки][Мин. ставок перед ожиданием комбинаций]",
        9: "[Ставки][Макс. ставок перед ожиданием комбинаций]",
        10: "[Ставки][Пропуск раундов после линии ставок]",
        11: "[Ставки][Мин. ставок подряд]",
        12: "[Ставки][Макс. ставок подряд]",
        13: "[Ставки][Мин. пропуск раундов]",
        14: "[Ставки][Макс. пропуск раундов]",
        15: "[Ставки][Ожидание краша после пропущенных игр]",
        16: "[Поиск комбинаций][Поиск комбинаций во время разбавочных игр]",
        17: "[Поиск комбинаций][Не пропускать ожидание после сыгранной комбинации]",
        18: "[Поиск комбинаций][Мин. поиск комбинаций после разбавки]",
        19: "[Поиск комбинаций][Макс. поиск комбинаций после разбавки]"
    }
    change_conf = command
    try:
        change_conf = int(change_conf)
    except ValueError:
        return init_classes.bot_tg.send_message(f'Вы ввели неверный тип данных. - {command}')
    
    match change_conf:
        case 1:
            if(configs.storage['bot-start']['wait_crash'] == "True"):
                configs.storage['bot-start']['wait_crash'] = "False"
            else:
                configs.storage['bot-start']['wait_crash'] = "True"
        case 4:
            if(configs.storage['bot-dilute']['pause_by_crash'] == "True"):
                configs.storage['bot-dilute']['pause_by_crash'] = "False"
            else:
                configs.storage['bot-dilute']['pause_by_crash'] = "True"
        case 5:
            if(configs.storage['bot-dilute']['pause_by_lose'] == "True"):
                configs.storage['bot-dilute']['pause_by_lose'] = "False"
            else:
                configs.storage['bot-dilute']['pause_by_lose'] = "True"
        case 10:
            if(configs.storage['bot-dilute']['skip_rounds_row'] == "True"):
                configs.storage['bot-dilute']['skip_rounds_row'] = "False"
            else:
                configs.storage['bot-dilute']['skip_rounds_row'] = "True"
        case 15:
            if(configs.storage['bot-dilute']['wait_crash_row'] == "True"):
                configs.storage['bot-dilute']['wait_crash_row'] = "False"
            else:
                configs.storage['bot-dilute']['wait_crash_row'] = "True"
        case 16:
            if(configs.storage['bot-patterns']['search_by_dilute'] == "True"):
                configs.storage['bot-patterns']['search_by_dilute'] = "False"
            else:
                configs.storage['bot-patterns']['search_by_dilute'] = "True"
        case 17:
            if(configs.storage['bot-patterns']['wait_after_pattern'] == "True"):
                configs.storage['bot-patterns']['wait_after_pattern'] = "False"
            else:
                configs.storage['bot-patterns']['wait_after_pattern'] = "True"
        case 2 | 3 | 6 | 7 | 8 | 9 | 11 | 12 | 13 | 14 | 18 | 19:
            info_user_tg.storage['active_page']['configs']['actions']['change'] = {}
            info_user_tg.storage['args']['action_cfg'] = change_conf
            return init_classes.bot_tg.send_message(f'Укажите новое значение для {names_change_conf[change_conf]}')
        case _:
            return init_classes.bot_tg.send_message(f'Пункта не существует - {change_conf}')

    send_configs.send_config_action_bot(app_path)