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

    sys.path.insert(1, app_path + '/bot-telegram/functions')
    import send_configs

    create_coef_max = command
    try:
        create_coef_max = float(create_coef_max)
    except ValueError:
        return init_classes.bot_tg.send_message(f'Вы ввели неверный тип данных. - {create_coef_max}')
    if(create_coef_max >= 1.01):
        if(create_coef_max >= info_user_tg.storage['args']['time_bet']['coef_min']):
            info_user_tg.storage['args']['time_bet']['coef_max'] = create_coef_max
            configs.storage['auto_bet']['Time_Bet'][info_user_tg.storage['args']['time_bet']['time']] = {
                "coef": {
                    "min": info_user_tg.storage['args']['time_bet']['coef_min'],
                    "max": info_user_tg.storage['args']['time_bet']['coef_max']
                },
                "cost": {
                    "min": info_user_tg.storage['args']['time_bet']['cost_min'],
                    "max": info_user_tg.storage['args']['time_bet']['cost_max']
                }
            }
            info_user_tg.storage['active_page']['configs']['bets']['time'] = {}
            send_configs.send_config_bet_bot(app_path)
            init_classes.bot_tg.send_message(f'Ставка была успешно создана')
        else:
            return init_classes.bot_tg.send_message(f"Максимальная ставка должна быть больше или равна минимальной. - {info_user_tg.storage['args']['time_bet']['cost_min']}")
    else:
        text = f"Значение коэффициента должно быть больше или равно 1.01x"
        return init_classes.bot_tg.send_message(text,parse_mode="Markdown")