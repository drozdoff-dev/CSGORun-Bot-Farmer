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

    number_pattern_bet = info_user_tg.storage['args']['pattern_bet']['select']
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

    for pattern_bet in configs.storage['auto_bet']['Pattern_Bet']['patterns']:
        if(pattern_bet == command):
            return init_classes.bot_tg.send_message(f'Вы не можете установить время {command}, ведь уже существует ставка с таким временем.')
    for (i,pattern_bet) in zip(range(len(configs.storage['auto_bet']['Pattern_Bet']['patterns'])),configs.storage['auto_bet']['Pattern_Bet']['patterns']):
        if(i == number_pattern_bet-1):
            configs.storage['auto_bet']['Pattern_Bet']['patterns'][command] = configs.storage['auto_bet']['Pattern_Bet']['patterns'].pop(pattern_bet)
            info_user_tg.storage['args']['pattern_bet']['last_command'] = ''
            info_user_tg.storage['active_page']['configs']['bets']['patterns']['edit']['change'] = {}
            init_classes.bot_tg.send_message(f'Значение комбинации {pattern_bet} у ставки №{number_pattern_bet} изменено на {command}')
            text = f''
            text += f"Текущая информация о ставке\n```html {i+1}. {command} - ставка: {configs.storage['auto_bet']['Pattern_Bet']['patterns'][command]['cost']['min']}-{configs.storage['auto_bet']['Pattern_Bet']['patterns'][command]['cost']['max']}$ на {configs.storage['auto_bet']['Pattern_Bet']['patterns'][command]['coef']['min']}-{configs.storage['auto_bet']['Pattern_Bet']['patterns'][command]['coef']['max']}x.```\n"
            text += f"\nВыберите, что хотите изменить:\n1. Комбинацию ставки.\n2. Мин. Ставку.\n3. Макс. Ставку.\n4. Мин. Коэф.\n5. Макс. Коэф."
            return init_classes.bot_tg.send_message(text,parse_mode="Markdown")