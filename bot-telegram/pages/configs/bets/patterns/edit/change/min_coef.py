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

    number_pattern_bet = info_user_tg.storage['args']['pattern_bet']['select']
    change_min_coef = command
    try:
        change_min_coef = float(change_min_coef)
    except ValueError:
        return init_classes.bot_tg.send_message(f'Вы ввели неверный тип данных. - {change_min_coef}')
    if(change_min_coef >= 1.01):
        for (i,pattern_bet) in zip(range(len(configs.storage['auto_bet']['Pattern_Bet']['patterns'])),configs.storage['auto_bet']['Pattern_Bet']['patterns']):
            if(i == number_pattern_bet-1):
                if(change_min_coef <= configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_bet]['coef']['max']):
                    info_user_tg.storage['args']['pattern_bet']['last_command'] = ''
                    info_user_tg.storage['active_page']['configs']['bets']['patterns']['edit']['change'] = {}
                    init_classes.bot_tg.send_message(f"Значение минимального коэффициента у ставки №{number_pattern_bet} изменено с {configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_bet]['coef']['min']} на {change_min_coef}")
                    configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_bet]['coef']['min'] = change_min_coef
                    text = f''
                    text += f"Текущая информация о ставке\n```html {i+1}. {pattern_bet} - ставка: {configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_bet]['cost']['min']}-{configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_bet]['cost']['max']}$ на {configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_bet]['coef']['min']}-{configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_bet]['coef']['max']}x.```\n"
                    text += f"\nВыберите, что хотите изменить:\n1. Комбинацию ставки.\n2. Мин. Ставку.\n3. Макс. Ставку.\n4. Мин. Коэф.\n5. Макс. Коэф."
                    return init_classes.bot_tg.send_message(text,parse_mode="Markdown")
                else:
                    text = f"Минимальное значение коэффициента должно быть меньше или равно максимальному - {configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_bet]['coef']['max']}"
                    return init_classes.bot_tg.send_message(text,parse_mode="Markdown")
    else:
        text = f"Значение коэффициента должно быть больше или равно 1.01$"
        return init_classes.bot_tg.send_message(text,parse_mode="Markdown")