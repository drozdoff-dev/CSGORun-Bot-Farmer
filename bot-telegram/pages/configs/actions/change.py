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

    sys.path.insert(1, app_path + '/bot-telegram/functions')
    import send_configs

    new_val = command
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
    action_cfg = info_user_tg.storage['args']['action_cfg']
    search_conf = {
        1: 'wait_crash',
        2: 'skip_min',
        3: 'skip_max',
        4: 'pause_by_crash',
        5: 'pause_by_lose',
        6: 'pause_min',
        7: 'pause_max',
        8: 'rounds_min',
        9: 'rounds_max',
        10: 'skip_rounds_row',
        11: 'row_min',
        12: 'row_max',
        13: 'skip_row_min',
        14: 'skip_row_max',
        15: 'wait_crash_row',
        16: 'search_by_dilute',
        17: 'wait_after_pattern',
        18: 'wait_seconds_min',
        19: 'wait_seconds_max',
    }
    match action_cfg:
        case 2 | 6 | 8 | 11 | 13 | 18:
            try:
                new_val = int(new_val)
            except ValueError:
                return init_classes.bot_tg.send_message(f'Вы ввели неверный тип данных. - {new_val}')
            
            if(new_val >= 1):
                if(action_cfg >= 1 and action_cfg <= 3):
                    if(new_val <= configs.storage['bot-start'][search_conf[action_cfg+1]]):
                        configs.storage['bot-start'][search_conf[action_cfg]] = new_val
                    else:
                        return init_classes.bot_tg.send_message(f"Минимальное значение не может быть больше максимального. - {configs.storage['bot-start'][search_conf[action_cfg+1]]}")
                elif(action_cfg >= 4 and action_cfg <= 15):
                    if(new_val <= configs.storage['bot-dilute'][search_conf[action_cfg+1]]):
                        configs.storage['bot-dilute'][search_conf[action_cfg]] = new_val
                    else:
                        return init_classes.bot_tg.send_message(f"Минимальное значение не может быть больше максимального. - {configs.storage['bot-dilute'][search_conf[action_cfg+1]]}")
                elif(action_cfg >= 16 and action_cfg <= 19):
                    if(new_val <= configs.storage['bot-patterns'][search_conf[action_cfg+1]]):
                        configs.storage['bot-patterns'][search_conf[action_cfg]] = new_val
                    else:
                        return init_classes.bot_tg.send_message(f"Минимальное значение не может быть больше максимального. - {configs.storage['bot-patterns'][search_conf[action_cfg+1]]}")
            else:
                return init_classes.bot_tg.send_message(f'Вы ввели недопустимое число. - {new_val}')
        case 3 | 7 | 9 | 12 | 14 | 19:
            try:
                new_val = int(new_val)
            except ValueError:
                return init_classes.bot_tg.send_message(f'Вы ввели неверный тип данных. - {new_val}')
            
            if(new_val >= 1):
                if(action_cfg >= 1 and action_cfg <= 3):
                    configs.storage['bot-start'][search_conf[action_cfg]] = new_val
                elif(action_cfg >= 4 and action_cfg <= 15):
                    configs.storage['bot-dilute'][search_conf[action_cfg]] = new_val
                elif(action_cfg >= 16 and action_cfg <= 19):
                    configs.storage['bot-patterns'][search_conf[action_cfg]] = new_val
            else:
                return init_classes.bot_tg.send_message(f'Вы ввели недопустимое число. - {new_val}')
        case _:
            return
        
    info_user_tg.storage['active_page']['configs']['actions'] = {}
    send_configs.send_config_action_bot(app_path)
    init_classes.bot_tg.send_message(f"Вы изменили - {names_change_conf[action_cfg]} = {new_val}")
    info_user_tg.storage['args']['action_cfg'] = 0