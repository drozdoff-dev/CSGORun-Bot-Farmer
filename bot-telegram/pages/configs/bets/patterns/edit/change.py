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

    if(command == "1. комбинацию ставки."):
        info_user_tg.storage['active_page']['configs']['bets']['patterns']['edit']['change']['pattern'] = {}
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
        text += f'Впишите комбинацию на которую желаете изменить в формате указанном выше в примере.'
        init_classes.bot_tg.send_message(text,parse_mode="Markdown")
    elif(command == "2. мин. ставку."):
        info_user_tg.storage['active_page']['configs']['bets']['patterns']['edit']['change']['min_cost'] = {}
        init_classes.bot_tg.send_message(f"Впишите минимальную ставку ботом от 0.01.")
    elif(command == "3. макс. ставку."):
        info_user_tg.storage['active_page']['configs']['bets']['patterns']['edit']['change']['max_cost'] = {}
        init_classes.bot_tg.send_message(f"Впишите максимальную ставку ботом от Мин. ставки.")
    elif(command == "4. мин. коэф."):
        info_user_tg.storage['active_page']['configs']['bets']['patterns']['edit']['change']['min_coef'] = {}
        init_classes.bot_tg.send_message(f"Впишите минимальный коэффициент ставки от 1.01.")
    elif(command == "5. макс. коэф."):
        info_user_tg.storage['active_page']['configs']['bets']['patterns']['edit']['change']['max_coef'] = {}
        init_classes.bot_tg.send_message(f"Впишите максимальный коэффициент ставки от Мин. коэффициента.")
    else:
        print()