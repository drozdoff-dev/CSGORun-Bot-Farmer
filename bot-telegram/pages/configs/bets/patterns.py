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
        info_user_tg.storage['active_page']['configs']['bets']['patterns']['add'] = {}
        info_user_tg.storage['args']['pattern_bet']['pattern'] = ''
        text = f""
        text += (f"\n_Объяснение выставлений комбинаций\n"
            +f"'$' - момент ставки ботом\n"
            +f"'r' - красный цвет игры | 1.00-1.19x\n"
            +f"'b' - синий цвет игры | 1.20-2.00x\n"
            +f"'p' - фиолетовый цвет игры | 2.00-4.00x\n"
            +f"'g' - зелёный цвет игры | 4.00-8.00x\n"
            +f"'y' - жёлтый цвет игры | 8.00-15.00x\n"
            +f"'t' - бирюзовый цвет игры | 15.00-∞x\n"
            +f"'w' - любой цвет игры, кроме красного | 1.20-∞x\n"
            +f"'-' - любой цвет игры | 1.00-∞x\n"
            +f"\nПример: '$$$-pr'\n"
            +f"В данном примере бот сделает три ставки подряд, когда 2 игры назад был красный цвет, 1 игру назад фиолетовый, и последняя любая._\n")
        text += f"\nВведите комбинацию в формате примера.\n"
        init_classes.bot_tg.send_message(text,parse_mode="Markdown")
    elif(command == "2. изменить ставки."):
        if(len(configs.storage['auto_bet']['Pattern_Bet']['patterns']) > 0):
            text = ''
            for (i,pattern_bet) in zip(range(len(configs.storage['auto_bet']['Pattern_Bet']['patterns'])),configs.storage['auto_bet']['Pattern_Bet']['patterns']):
                text += f"```html {i+1}. {pattern_bet} - ставка: {configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_bet]['cost']['min']}-{configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_bet]['cost']['max']}$ на {configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_bet]['coef']['min']}-{configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_bet]['coef']['max']}x.```\n"
            text += f"\nВыберите номер ставки, которую хотите изменить"
            info_user_tg.storage['args']['pattern_bet']['select'] = 0
            info_user_tg.storage['active_page']['configs']['bets']['patterns']['edit'] = {}
            init_classes.bot_tg.send_message(text,parse_mode="Markdown")
        else:
            text += f"```html Ставки отсутстуют ```\n\nВы не можете ничего изменить."
            text += f"1. добавить ставку.\n2. изменить ставки.\n3. удалить ставку."
            info_user_tg.storage['active_page']['configs']['bets']['patterns'] = {}
            return init_classes.bot_tg.send_message(text,parse_mode="Markdown")
    elif(command == "3. удалить ставку."):
        if(len(configs.storage['auto_bet']['Pattern_Bet']['patterns']) > 0):
            text = ''
            for (i,pattern_bet) in zip(range(len(configs.storage['auto_bet']['Pattern_Bet']['patterns'])),configs.storage['auto_bet']['Pattern_Bet']['patterns']):
                text += f"```html {i+1}. {pattern_bet} - ставка: {configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_bet]['cost']['min']}-{configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_bet]['cost']['max']}$ на {configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_bet]['coef']['min']}-{configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_bet]['coef']['max']}x.```\n"
            text += f"\nВыберите номер ставки, которую хотите удалить"
            info_user_tg.storage['active_page']['configs']['bets']['patterns']['remove'] = {}
            info_user_tg.storage['args']['pattern_bet']['select'] = 0
            init_classes.bot_tg.send_message(text,parse_mode="Markdown")
        else:
            text += f"```html Ставки отсутстуют ```\n\nВы не можете ничего удалить."
            text += f"1. добавить ставку.\n2. изменить ставки.\n3. удалить ставку."
            info_user_tg.storage['active_page']['configs']['bets']['patterns'] = {}
            return init_classes.bot_tg.send_message(text,parse_mode="Markdown")