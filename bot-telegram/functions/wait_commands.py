import importlib.util
import os
import sys
from threading import Thread
from telebot import types


def wait(app_path,bot_tg):
    sys.path.insert(1, app_path + '/storage/temp/telegram_bot/')
    import info_bot_tg
    import info_user_tg

    sys.path.insert(1, app_path + '/storage/temp/global')
    import init_classes

    import send_configs
    
    @bot_tg.message_handler(content_types=['text'])
    def get_text_messages(message):
        command = (message.text).lower()
        info_bot_tg.storage['accept_command'] = True
        if(info_bot_tg.storage['accept_command']):

            if(info_user_tg.storage['active_page'] == {}):
                if(command == "/конфиг"):
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
                    btn1 = types.KeyboardButton("1. Конфигурация аккаунтов.")
                    btn2 = types.KeyboardButton("2. Конфигурация поведения бота.")
                    btn3 = types.KeyboardButton("3. Конфигурация ставок бота.")
                    btn4 = types.KeyboardButton("4. Конфигурация уведомлений в телеграмм.")
                    markup.add(btn1, btn2, btn3, btn4)

                    message = ('Выберите раздел, который желаете настроить:\n'
                            + '1. Конфигурация аккаунтов.\n'
                            + '2. Конфигурация поведения бота.\n'
                            + '3. Конфигурация ставок бота.\n'
                            + '4. Конфигурация уведомлений в телеграмм.')
                    init_classes.bot_tg.send_message(message, reply_markup=markup)

                    info_user_tg.storage['active_page']['configs'] = {}
                    info_user_tg.storage['user_check_config'] = False

                elif(command == "/старт"):
                    sys.path.insert(1, app_path + '/storage/temp/bot_bet/')
                    import info_bot

                    if(not info_bot.storage['bot_started']):
                        if(info_user_tg.storage['user_check_config']):
                            info_bot.storage['has_stopped'] = False
                            init_classes.bot_tg.send_message(f'Бот запущен!')
                            info_bot.storage['bot_started'] = True
                    else:
                        init_classes.bot_tg.send_message(f'Бот и так в запущенном состоянии!')

                    if(not info_user_tg.storage['user_check_config']):
                        send_configs.send_config_accounts(app_path)
                        send_configs.send_config_action_bot(app_path)
                        send_configs.send_config_bet_bot(app_path)
                        send_configs.send_config_notifications(app_path)

                        init_classes.bot_tg.send_message(f'Перед запуском бота, подтвердите, что текущая конфигурация верна.\nОтправьте повторно старт - если конфигурация верна, и вы хотите запустить бота.\nОтправьте "конфигурация", чтобы подкорректировать текущую конфигурацию.',parse_mode="Markdown")
                        info_user_tg.storage['user_check_config'] = True
                elif(command == "/стоп"):
                    sys.path.insert(1, app_path + '/storage/temp/bot_bet/')
                    import info_bot

                    if(info_bot.storage['bot_started']):
                        init_classes.bot_tg.send_message(f'Выключение произойдёт по окончанию итерации...')
                        info_bot.storage['bot_started'] = False
                        info_bot.storage['has_stopped'] = True
                    else:
                        init_classes.bot_tg.send_message(f'Бот и так в выключенном состоянии!')
                elif(command == "/статус"):
                    sys.path.insert(1, app_path + '/storage/temp/bot_bet/')
                    import info_bot
                    
                    message = ''
                    init_classes.bot_tg.send_message(message)
                    if(info_bot.storage['bot_started']):
                        message = 'Бот активен'
                    else:
                        message = 'Бот Выключен'
                    init_classes.bot_tg.send_message(message)
                elif(command == "/баланс"):
                    print()
            else:
                active_page = info_user_tg.storage['active_page']
                dir_page = app_path + f'\\bot-telegram\\pages\\'
                while True:
                    search_page = False
                    for page in active_page.keys():
                        if(active_page[page] == {}):
                            dir_page += f'{page}.py'
                            spec_path = importlib.util.spec_from_file_location(page,dir_page)
                            page = importlib.util.module_from_spec(spec_path)
                            spec_path.loader.exec_module(page)
                            page.call_page(app_path,command)
                            search_page = True
                            break
                        else:
                            active_page = active_page[page]
                            dir_page += f'{page}\\'
                    if(search_page):
                        break

        else:
            bot_tg.send_message('Бот ещё не готов к обработке команд.\nДождитесь полной загрузки скрипта.')