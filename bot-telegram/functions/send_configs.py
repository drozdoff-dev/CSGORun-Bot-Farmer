

import sys
from telebot import types

def send_config_accounts(app_path):
    sys.path.insert(1, app_path + '/storage/temp/global/')
    import init_classes

    sys.path.insert(1, app_path + '/storage/temp/bet_bot/')
    import configs

    text = f'Конфигурация аккаунтов\n\nАктивный аккаунт: *{configs.storage["main"]["active_account"]}*\nСписок доступных аккаунтов:\n```html\n'
    for (i,account) in zip(range(len(configs.storage['accounts'])),configs.storage['accounts']):
        text += f'{account}\n'
    text += f'```\nВыберите, что хотите сделать:\n1. Сменить активный аккаунт\n2. Добавить аккаунт\n3. Удалить аккаунт.'
    init_classes.bot_tg.send_message(text,parse_mode="Markdown")

def send_config_action_bot(app_path):
    sys.path.insert(1, app_path + '/storage/temp/global/')
    import init_classes

    sys.path.insert(1, app_path + '/storage/temp/bet_bot/')
    import configs
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for btn_num in range(19):
        btn = types.KeyboardButton(f"{btn_num+1}")
        markup.add(btn)

    convert = {"True": 'Да', "False": 'Нет'}
    text = (f"Конфигурация поведения бота\n"
            +f"\n*Поведение бота при запуске:*\n"
            +f"```html\n1. Ожидание краша: {convert[configs.storage['bot-start']['wait_crash']]} | Да/Нет\n"
            +f"2. Мин. Ожидание после краша: {configs.storage['bot-start']['skip_min']} игр(ы). | 1-∞\n"
            +f"3. Макс. Ожидание после краша: {configs.storage['bot-start']['skip_max']} игр(ы). | Мин.-∞```\n"
            +f"\n*Поведение бота при разбавочных играх:*\n"
            +f"_Краш/проигрыш_\n"
            +f"```html\n4. Ожидание при краше: {convert[configs.storage['bot-dilute']['pause_by_crash']]} | Да/Нет\n"
            +f"5. Ожидание при проигрыше: {convert[configs.storage['bot-dilute']['pause_by_lose']]} | Да/Нет\n"
            +f"6. Мин. ожидание при краше/проигрыше: {configs.storage['bot-dilute']['pause_min']} игр(ы). | 1-∞\n"
            +f"7. Макс. ожидание при краше/проигрыше: {configs.storage['bot-dilute']['pause_max']} игр(ы). | Мин.-∞```\n"
            +f"\n_Ставки_\n"
            +f"```html\n8. Мин. ставок перед ожиданием комбинаций: {configs.storage['bot-dilute']['rounds_min']} | 1-∞\n"
            +f"9. Макс. ставок перед ожиданием комбинаций: {configs.storage['bot-dilute']['rounds_max']} игр(ы). | Мин.-∞\n"
            +f"10. Пропуск раундов после линии ставок: {convert[configs.storage['bot-dilute']['skip_rounds_row']]} игр(ы). | Да/Нет\n"
            +f"11. Мин. ставок подряд: {configs.storage['bot-dilute']['row_min']} игр(ы). | 1-∞\n"
            +f"12. Макс. ставок подряд: {configs.storage['bot-dilute']['row_max']} игр(ы). | Мин.-∞\n"
            +f"13. Мин. пропуск раундов: {configs.storage['bot-dilute']['skip_row_min']} игр(ы). | 1-∞\n"
            +f"14. Макс. пропуск раундов: {configs.storage['bot-dilute']['skip_row_max']} игр(ы). | Мин.-∞\n"
            +f"15. Ожидание краша после пропущенных игр: {convert[configs.storage['bot-dilute']['wait_crash_row']]} | Да/Нет```\n"
            +f"\n*Поведение бота при поиске комбинаций*\n"
            +f"```html\n16. Поиск комбинаций во время разбавочных игр: {convert[configs.storage['bot-patterns']['search_by_dilute']]} | Да/Нет\n"
            +f"17. Не пропускать ожидание после сыгранной комбинации: {convert[configs.storage['bot-patterns']['wait_after_pattern']]} | Да/Нет\n"
            +f"18. Мин. поиск комбинаций после разбавки: {configs.storage['bot-patterns']['wait_seconds_min']} сек. | 1-∞\n"
            +f"19. Макс. поиск комбинаций после разбавки: {configs.storage['bot-patterns']['wait_seconds_max']} сек. | Мин.-∞```")
    text += f'\n\nВыберите номер пункта, который хотите изменить.'
    init_classes.bot_tg.send_message(text,parse_mode="Markdown",reply_markup=markup)

def send_config_bet_bot(app_path):
        sys.path.insert(1, app_path + '/storage/temp/global/')
        import init_classes

        sys.path.insert(1, app_path + '/storage/temp/bet_bot/')
        import configs

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
        btn1 = types.KeyboardButton("1. Изменить ставки по времени.")
        btn2 = types.KeyboardButton("2. Изменить ставки по комбинациям.")
        btn3 = types.KeyboardButton("3. Изменить ставки по разбавочным играм.")
        markup.add(btn1, btn2, btn3)

        text = f"Конфигурация ставок бота\n"
        text += f"\n*Ставки по времени*\n"
        if(len(configs.storage['auto_bet']['Time_Bet']) > 0):
            for (i,time_bet) in zip(range(len(configs.storage['auto_bet']['Time_Bet'])),configs.storage['auto_bet']['Time_Bet']):
                text += f"```html {i+1}. В {time_bet} МСК - ставка: {configs.storage['auto_bet']['Time_Bet'][time_bet]['cost']['min']}-{configs.storage['auto_bet']['Time_Bet'][time_bet]['cost']['max']}$ на {configs.storage['auto_bet']['Time_Bet'][time_bet]['coef']['min']}-{configs.storage['auto_bet']['Time_Bet'][time_bet]['coef']['max']}x.```\n"
        else:
            text += f"```html Ставки отсутстуют ```\n"
        text += f"\n*Ставки по комбинациям*\n"
        for (i,pattern_bet) in zip(range(len(configs.storage['auto_bet']['Pattern_Bet']['patterns'])),configs.storage['auto_bet']['Pattern_Bet']['patterns']):
            text += f"```html {i+1}. {pattern_bet} - ставка: {configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_bet]['cost']['min']}-{configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_bet]['cost']['max']}$ на {configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_bet]['coef']['min']}-{configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_bet]['coef']['max']}x.```\n"
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
        text += (f"\n*Ставки по разбавочным играм*\n"
                +f"```html Диапозон ставки: {configs.storage['auto_bet']['Dilute_Bet']['cost']['min']}-{configs.storage['auto_bet']['Dilute_Bet']['cost']['max']}$ на {configs.storage['auto_bet']['Dilute_Bet']['coef']['min']}-{configs.storage['auto_bet']['Dilute_Bet']['coef']['max']}x```\n")
        text += (f"\n_Информация"
                +f"\nРазбавочные игры нужны для разброса в статистике, чтобы не было ставок по одним и тем же комбинациями.\nТакую же роль выполняют конфигурации связанные с диапозоном, данная возможность позволяет сделать статистику более правдоподобной на настоящего человека.\nИнтересный факт: пропуски игр и пазуы выполняют такую же роль )_")
        text += f'\n\nВыберите, что хотите сделать:\n1. Изменить ставки по времени.\n2. Изменить ставки по комбинациям.\n3. Изменить ставки по разбавочным играм.'
        init_classes.bot_tg.send_message(text,parse_mode="Markdown",reply_markup=markup)

def send_config_notifications(app_path):
    sys.path.insert(1, app_path + '/storage/temp/global/')
    import init_classes

    sys.path.insert(1, app_path + '/storage/temp/bet_bot/')
    import configs

    sys.path.insert(1, app_path + '/storage/temp/telegram_bot/')
    import info_bot_tg

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for btn_num in range(31):
        btn = types.KeyboardButton(f"{btn_num+1}")
        markup.add(btn)


    convert = {True: 'Да', False: 'Нет'}
    message = f"Конфигурация уведомлений\n"
    message += (f"\nГлобальное:```html\n"
            +f"1. Уведомления об ошибках - {convert[configs.storage['telegram']['notification']['Global']['error']]} | Да/Нет```\n"
            +f"\n*Разбавочные игры:*```html\n"
            +f"2. Уведомления о ставках - {convert[configs.storage['telegram']['notification']['Dilute_Game']['bet']]} | Да/Нет\n"
            +f"3. Уведомления о победах - {convert[configs.storage['telegram']['notification']['Dilute_Game']['win']]} | Да/Нет\n"
            +f"4. Уведомления о проигрышах - {convert[configs.storage['telegram']['notification']['Dilute_Game']['lose']]} | Да/Нет\n"
            +f"5. Уведомления о крашах - {convert[configs.storage['telegram']['notification']['Dilute_Game']['crash']]} | Да/Нет\n"
            +f"6. Уведомления о ставке предмета - {convert[configs.storage['telegram']['notification']['Dilute_Game']['bet_item']]} | Да/Нет\n"
            +f"7. Уведомления о покупке предмета - {convert[configs.storage['telegram']['notification']['Dilute_Game']['buy_item']]} | Да/Нет\n"
            +f"8. Уведомления об обмене предметов - {convert[configs.storage['telegram']['notification']['Dilute_Game']['change_item']]} | Да/Нет\n"
            +f"9. Уведомления о пропуске игр - {convert[configs.storage['telegram']['notification']['Dilute_Game']['skip_rounds']]} | Да/Нет\n"
            +f"10. Уведомления о количестве пропускаемых игр - {convert[configs.storage['telegram']['notification']['Dilute_Game']['skip_count']]} | Да/Нет\n"
            +f"11. Уведомления о ожидании комбинаций - {convert[configs.storage['telegram']['notification']['Dilute_Game']['wait_pattern']]} | Да/Нет```\n"
            +f"\n*Игры по комбинациям:*```html\n"
            +f"12. Уведомления о ставках - {convert[configs.storage['telegram']['notification']['Pattern_Game']['bet']]} | Да/Нет\n"
            +f"13. Уведомления о победах - {convert[configs.storage['telegram']['notification']['Pattern_Game']['win']]} | Да/Нет\n"
            +f"14. Уведомления о проигрышах - {convert[configs.storage['telegram']['notification']['Pattern_Game']['lose']]} | Да/Нет\n"
            +f"15. Уведомления о крашах - {convert[configs.storage['telegram']['notification']['Pattern_Game']['crash']]} | Да/Нет\n"
            +f"16. Уведомления о ставке предмета - {convert[configs.storage['telegram']['notification']['Pattern_Game']['bet_item']]} | Да/Нет\n"
            +f"17. Уведомления о покупке предмета - {convert[configs.storage['telegram']['notification']['Pattern_Game']['buy_item']]} | Да/Нет\n"
            +f"18. Уведомления об обмене предметов - {convert[configs.storage['telegram']['notification']['Pattern_Game']['change_item']]} | Да/Нет\n"
            +f"19. Уведомления о пропуске игр - {convert[configs.storage['telegram']['notification']['Pattern_Game']['skip_rounds']]} | Да/Нет\n"
            +f"20. Уведомления о количестве пропускаемых игр - {convert[configs.storage['telegram']['notification']['Pattern_Game']['skip_count']]} | Да/Нет\n"
            +f"21. Уведомления о найденном паттерне - {convert[configs.storage['telegram']['notification']['Pattern_Game']['found_pattern']]} | Да/Нет```\n"
            +f"\n*Игры по времени:*```html\n"
            +f"22. Уведомления о ставках - {convert[configs.storage['telegram']['notification']['Time_Game']['bet']]} | Да/Нет\n"
            +f"23. Уведомления о победах - {convert[configs.storage['telegram']['notification']['Time_Game']['win']]} | Да/Нет\n"
            +f"24. Уведомления о проигрышах - {convert[configs.storage['telegram']['notification']['Time_Game']['lose']]} | Да/Нет\n"
            +f"25. Уведомления о крашах - {convert[configs.storage['telegram']['notification']['Time_Game']['crash']]} | Да/Нет\n"
            +f"26. Уведомления о ставке предмета - {convert[configs.storage['telegram']['notification']['Time_Game']['bet_item']]} | Да/Нет\n"
            +f"27. Уведомления о покупке предмета - {convert[configs.storage['telegram']['notification']['Time_Game']['buy_item']]} | Да/Нет\n"
            +f"28. Уведомления об обмене предметов - {convert[configs.storage['telegram']['notification']['Time_Game']['change_item']]} | Да/Нет\n"
            +f"29. Уведомления о пропуске игр - {convert[configs.storage['telegram']['notification']['Time_Game']['skip_rounds']]} | Да/Нет\n"
            +f"30. Уведомления о количестве пропускаемых игр - {convert[configs.storage['telegram']['notification']['Time_Game']['skip_count']]} | Да/Нет\n"
            +f"31. Уведомления о ожидании времени ставки - {convert[configs.storage['telegram']['notification']['Time_Game']['wait_time']]} | Да/Нет```\n")
    message += f"\nВыберите номер конфигурации, который хотите изменить.\nИли напишите номера через запятую, и они автоматически изменятся."
    init_classes.bot_tg.send_message(message,parse_mode="Markdown", reply_markup=markup)