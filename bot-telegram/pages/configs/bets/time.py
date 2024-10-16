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

    if(command == "1. добавить ставку."):
        info_user_tg.storage['active_page']['configs']['bets']['time']['add'] = {}
        info_user_tg.storage['args']['time_bet']['time'] = ''
        text = f"Введите время для ставки в формате HH:MM"
        init_classes.bot_tg.send_message(text)
    elif(command == "2. изменить ставки."):
        if(len(configs.storage['auto_bet']['Time_Bet']) > 0):
            text = ""
            for (i,time_bet) in zip(range(len(configs.storage['auto_bet']['Time_Bet'])),configs.storage['auto_bet']['Time_Bet']):
                text += f"```html {i+1}. В {time_bet} МСК - ставка: {configs.storage['auto_bet']['Time_Bet'][time_bet]['cost']['min']}-{configs.storage['auto_bet']['Time_Bet'][time_bet]['cost']['max']}$ на {configs.storage['auto_bet']['Time_Bet'][time_bet]['coef']['min']}-{configs.storage['auto_bet']['Time_Bet'][time_bet]['coef']['max']}x.```\n"
            text += f"\nВыберите номер ставки, которую хотите изменить"
            info_user_tg.storage['args']['time_bet']['select'] = 0
            info_user_tg.storage['active_page']['configs']['bets']['time']['edit'] = {}
            return init_classes.bot_tg.send_message(text,parse_mode="Markdown")
        else:
            text += f"```html Ставки отсутстуют ```\n\nВы не можете ничего изменить."
            text += f"1. добавить ставку.\n2. изменить ставки.\n3. удалить ставку."
            info_user_tg.storage['active_page']['configs']['bets']['time'] = {}
            return init_classes.bot_tg.send_message(text,parse_mode="Markdown")
    elif(command == "3. удалить ставку."):
        if(len(configs.storage['auto_bet']['Time_Bet']) > 0):
            text = ""
            for (i,time_bet) in zip(range(len(configs.storage['auto_bet']['Time_Bet'])),configs.storage['auto_bet']['Time_Bet']):
                text += f"```html {i+1}. В {time_bet} МСК - ставка: {configs.storage['auto_bet']['Time_Bet'][time_bet]['cost']['min']}-{configs.storage['auto_bet']['Time_Bet'][time_bet]['cost']['max']}$ на {configs.storage['auto_bet']['Time_Bet'][time_bet]['coef']['min']}-{configs.storage['auto_bet']['Time_Bet'][time_bet]['coef']['max']}x.```\n"
            text += f"\nВыберите номер ставки, которую хотите удалить"
            info_user_tg.storage['args']['time_bet']['select'] = 0
            info_user_tg.storage['active_page']['configs']['bets']['time']['remove'] = {}
            return init_classes.bot_tg.send_message(text,parse_mode="Markdown")
        else:
            text += f"```html Ставки отсутстуют ```\n\nВы не можете ничего удалить."
            text += f"1. добавить ставку.\n2. изменить ставки.\n3. удалить ставку."
            info_user_tg.storage['active_page']['configs']['bets']['time'] = {}
            return init_classes.bot_tg.send_message(text,parse_mode="Markdown")