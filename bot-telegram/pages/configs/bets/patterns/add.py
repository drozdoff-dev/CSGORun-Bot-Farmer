import sys
import time
from telebot import types
import re


def call_page(app_path,command):
    sys.path.insert(1, app_path + '/storage/temp/telegram_bot')
    import info_bot_tg
    import info_user_tg

    sys.path.insert(1, app_path + '/storage/temp/global')
    import init_classes

    sys.path.insert(1, app_path + '/storage/temp/bet_bot/')
    import configs

    info_user_tg.storage['args']['pattern_bet']['cost_min'] = 0.0
    create_pattern = command

    game_pattern_count = create_pattern.count("$")
    if(game_pattern_count > 0):
        for (i, pat) in zip(range(len(create_pattern)), create_pattern):
            if(i+1 <= game_pattern_count):
                if(pat != '$'):
                    return init_classes.bot_tg.send_message(f'Знак "$" обозначающий ставку обязан стоять вначале.')
            else:
                if(pat != 'r' and pat != 'w' and pat != 'b' and pat != 'p' and pat != 'g' and pat != 'y' and pat != 't' and pat != '-'):
                    return init_classes.bot_tg.send_message(f'Комбинация принимает исключительно следующие символы.\n'
                                                            +f"_'$' - момент ставки ботом\n"
                                                            +f"'r' - красный цвет игры | 1.00-1.19x\n"
                                                            +f"'b' - синий цвет игры | 1.20-2.00x\n"
                                                            +f"'p' - фиолетовый цвет игры | 2.00-4.00x\n"
                                                            +f"'g' - зелёный цвет игры | 4.00-8.00x\n"
                                                            +f"'y' - жёлтый цвет игры | 8.00-15.00x\n"
                                                            +f"'t' - бирюзовый цвет игры | 15.00-∞x\n"
                                                            +f"'w' - любой цвет игры, кроме красного | 1.20-∞x\n"
                                                            +f"'-' - любой цвет игры | 1.00-∞x_\n"
                                                            +f"\nА у вас в комбинации указан - '{pat}'.",parse_mode="Markdown")
    else:
        return init_classes.bot_tg.send_message(f'У вас должно стоять обозначение ставки - "$".')

    for pattern in configs.storage['auto_bet']['Pattern_Bet']['patterns']:
        if(command == pattern):
            return init_classes.bot_tg.send_message(f'Ставка по данной комбинации уже существует.')
    info_user_tg.storage['args']['pattern_bet']['pattern'] = command
    info_user_tg.storage['active_page']['configs']['bets']['patterns']['add']['min_cost'] = {}
    init_classes.bot_tg.send_message(f'Введите минимальный размер ставки')