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

    change_max_cost = command
    try:
        change_max_cost = float(change_max_cost)
    except ValueError:
        return init_classes.bot_tg.send_message(f'Вы ввели неверный тип данных. - {change_max_cost}')
    if(change_max_cost >= 0.1):
        if(change_max_cost >= configs.storage['auto_bet']['Dilute_Bet']['cost']['min']):
            info_user_tg.storage['active_page']['configs']['bets']['dilute'] = {}
            init_classes.bot_tg.send_message(f"Значение максимальной ставки у разбавочных игр изменено с {configs.storage['auto_bet']['Dilute_Bet']['cost']['max']} на {change_max_cost}")
            configs.storage['auto_bet']['Dilute_Bet']['cost']['max'] = change_max_cost
            text = ''
            text += (f"\n*Текущая информация по разбавочным играм*\n"
                    +f"```html Диапозон ставки: {configs.storage['auto_bet']['Dilute_Bet']['cost']['min']}-{configs.storage['auto_bet']['Dilute_Bet']['cost']['max']}$ на {configs.storage['auto_bet']['Dilute_Bet']['coef']['min']}-{configs.storage['auto_bet']['Dilute_Bet']['coef']['max']}x```\n")
            text += f"\nВыберите, что хотите изменить:\n1. Мин. Ставку.\n2. Макс. Ставку.\n3. Мин. Коэф.\n4. Макс. Коэф."
            return init_classes.bot_tg.send_message(text,parse_mode="Markdown")
        else:
            text = f"Максимальное значение ставки должно быть больше или равно минимальному - {configs.storage['auto_bet']['Dilute_Bet']['cost']['min']}"
            return init_classes.bot_tg.send_message(text,parse_mode="Markdown")
    else:
        text = f"Значение ставки должно быть больше или равно 0.1$"
        return init_classes.bot_tg.send_message(text,parse_mode="Markdown")