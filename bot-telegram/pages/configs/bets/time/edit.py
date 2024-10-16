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

    number_time_bet = command
    try:
        number_time_bet = int(number_time_bet)
    except ValueError:
        return init_classes.bot_tg.send_message(f'Вы ввели неверный тип данных. - {number_time_bet}')
    if(number_time_bet > 0):
        if(len(configs.storage['auto_bet']['Time_Bet']) >= number_time_bet):
            for (i,time_bet) in zip(range(len(configs.storage['auto_bet']['Time_Bet'])),configs.storage['auto_bet']['Time_Bet']):
                if(i+1 == number_time_bet):
                    info_user_tg.storage['active_page']['configs']['bets']['time']['edit']['change'] = {}
                    info_user_tg.storage['args']['time_bet']['select'] = number_time_bet
                    info_user_tg.storage['args']['time_bet']['last_command'] = ''
                    text = f"Текущая информация о ставке\n```html {number_time_bet}. В {time_bet} МСК - ставка: {configs.storage['auto_bet']['Time_Bet'][time_bet]['cost']['min']}-{configs.storage['auto_bet']['Time_Bet'][time_bet]['cost']['max']}$ на {configs.storage['auto_bet']['Time_Bet'][time_bet]['coef']['min']}-{configs.storage['auto_bet']['Time_Bet'][time_bet]['coef']['max']}x.```\n"
                    text += f"\nВыберите, что хотите изменить:\n1. Время ставки.\n2. Мин. Ставку.\n3. Макс. Ставку.\n4. Мин. Коэф.\n5. Макс. Коэф."
                    return init_classes.bot_tg.send_message(text,parse_mode="Markdown")
        else:
            text = f"такой игры не существует"
            return init_classes.bot_tg.send_message(text,parse_mode="Markdown")
    else:
        text = f"число должно быть положительное"
        return init_classes.bot_tg.send_message(text,parse_mode="Markdown")