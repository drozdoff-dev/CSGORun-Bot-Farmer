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
    change_max_cost = command
    try:
        change_max_cost = float(change_max_cost)
    except ValueError:
        return init_classes.bot_tg.send_message(f'Вы ввели неверный тип данных. - {change_max_cost}')
    if(change_max_cost >= 0.01):
        for (i,pattern_bet) in zip(range(len(configs.storage['auto_bet']['Pattern_Bet']['patterns'])),configs.storage['auto_bet']['Pattern_Bet']['patterns']):
            if(i == number_pattern_bet-1):
                if(change_max_cost >= configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_bet]['cost']['min']):
                    info_user_tg.storage['args']['pattern_bet']['last_command'] = ''
                    info_user_tg.storage['active_page']['configs']['bets']['patterns']['edit']['change'] = {}
                    init_classes.bot_tg.send_message(f"Значение максимальной ставки у ставки №{number_pattern_bet} изменено с {configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_bet]['cost']['max']} на {change_max_cost}")
                    configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_bet]['cost']['max'] = change_max_cost
                    text = f''
                    text += f"Текущая информация о ставке\n```html {i+1}. {pattern_bet} - ставка: {configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_bet]['cost']['min']}-{configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_bet]['cost']['max']}$ на {configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_bet]['coef']['min']}-{configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_bet]['coef']['max']}x.```\n"
                    text += f"\nВыберите, что хотите изменить:\n1. Комбинацию ставки.\n2. Мин. Ставку.\n3. Макс. Ставку.\n4. Мин. Коэф.\n5. Макс. Коэф."
                    return init_classes.bot_tg.send_message(text,parse_mode="Markdown")
                else:
                    text = f"Максимальное значение ставки должно быть больше или равно минимальному - {configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_bet]['cost']['min']}"
                    return init_classes.bot_tg.send_message(text,parse_mode="Markdown")
    else:
        text = f"Значение ставки должно быть больше или равно 0.1$"
        return init_classes.bot_tg.send_message(text,parse_mode="Markdown")