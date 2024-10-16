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

    number_time_bet = info_user_tg.storage['args']['time_bet']['select']
    change_max_coef = command
    try:
        change_max_coef = float(change_max_coef)
    except ValueError:
        return init_classes.bot_tg.send_message(f'Вы ввели неверный тип данных. - {change_max_coef}')
    if(change_max_coef >= 0.01):
        for (i,time_bet) in zip(range(len(configs.storage['auto_bet']['Time_Bet'])),configs.storage['auto_bet']['Time_Bet']):
            if(i == number_time_bet-1):
                if(change_max_coef >= configs.storage['auto_bet']['Time_Bet'][time_bet]['coef']['min']):
                    info_user_tg.storage['args']['time_bet']['last_command'] = ''
                    info_user_tg.storage['active_page']['configs']['bets']['time']['edit']['change'] = {}
                    init_classes.bot_tg.send_message(f"Значение максимальной ставки у ставки №{number_time_bet} изменено с {configs.storage['auto_bet']['Time_Bet'][time_bet]['coef']['max']} на {change_max_coef}")
                    configs.storage['auto_bet']['Time_Bet'][time_bet]['coef']['max'] = change_max_coef
                    text = f''
                    text += f"Текущая информация о ставке\n```html {number_time_bet}. В {time_bet} МСК - ставка: {configs.storage['auto_bet']['Time_Bet'][time_bet]['cost']['min']}-{configs.storage['auto_bet']['Time_Bet'][time_bet]['cost']['max']}$ на {configs.storage['auto_bet']['Time_Bet'][time_bet]['coef']['min']}-{configs.storage['auto_bet']['Time_Bet'][time_bet]['coef']['max']}x.```\n"
                    text += f"\nВыберите, что хотите изменить:\n1. Время ставки.\n2. Мин. ставку.\n3. Макс. Ставку.\n4. Мин.Коэф.\n5. Макс. Коэф."
                    return init_classes.bot_tg.send_message(text,parse_mode="Markdown")
                else:
                    text = f"Максимальное значение коэффициента должно быть больше или равно минимальному - {configs.storage['auto_bet']['Time_Bet'][time_bet]['coef']['min']}"
                    return init_classes.bot_tg.send_message(text,parse_mode="Markdown")
    else:
        text = f"Значение коэффициента должно быть больше или равно 1.01$"
        return init_classes.bot_tg.send_message(text,parse_mode="Markdown")