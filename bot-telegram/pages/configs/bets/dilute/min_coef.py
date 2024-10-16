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

    change_min_coef = command
    try:
        change_min_coef = float(change_min_coef)
    except ValueError:
        return init_classes.bot_tg.send_message(f'Вы ввели неверный тип данных. - {change_min_coef}')
    if(change_min_coef >= 1.01):
        if(change_min_coef <= configs.storage['auto_bet']['Dilute_Bet']['coef']['max']):
            info_user_tg.storage['active_page']['configs']['bets']['dilute'] = {}
            init_classes.bot_tg.send_message(f"Значение минимального коэффициента у разбавочных игр изменено с {configs.storage['auto_bet']['Dilute_Bet']['coef']['min']} на {change_min_coef}")
            configs.storage['auto_bet']['Dilute_Bet']['coef']['min'] = change_min_coef
            text = ''
            text += (f"\n*Текущая информация по разбавочным играм*\n"
                    +f"```html Диапозон ставки: {configs.storage['auto_bet']['Dilute_Bet']['cost']['min']}-{configs.storage['auto_bet']['Dilute_Bet']['cost']['max']}$ на {configs.storage['auto_bet']['Dilute_Bet']['coef']['min']}-{configs.storage['auto_bet']['Dilute_Bet']['coef']['max']}x```\n")
            text += f"\nВыберите, что хотите изменить:\n1. Мин. Ставку.\n2. Макс. Ставку.\n3. Мин. Коэф.\n4. Макс. Коэф."
            return init_classes.bot_tg.send_message(text,parse_mode="Markdown")
        else:
            text = f"Минимальное значение коэффициента должно быть меньше или равно максимальному - {configs.storage['auto_bet']['Dilute_Bet']['coef']['max']}"
            return init_classes.bot_tg.send_message(text,parse_mode="Markdown")
    else:
        text = f"Значение коэффициента должно быть больше или равно 1.01x"
        return init_classes.bot_tg.send_message(text,parse_mode="Markdown")