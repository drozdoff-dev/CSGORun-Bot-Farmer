import sys


def call_page(app_path,command):
    sys.path.insert(1, app_path + '/bot-telegram/functions')
    import send_configs

    sys.path.insert(1, app_path + '/storage/temp/global')
    import init_classes

    sys.path.insert(1, app_path + '/storage/temp/bet_bot/')
    import configs
    
    change_conf = command.split(',')
    for conf in change_conf:
        try:
            conf = int(conf)
        except ValueError:
            return init_classes.bot_tg.send_message(f'Вы ввели неверный тип данных. - {conf}')
        if(isinstance(conf, int)):
            if(conf == 1):
                if(configs.storage['telegram']['notification']['Global']['error']):
                    configs.storage['telegram']['notification']['Global']['error'] = False
                else:
                    configs.storage['telegram']['notification']['Global']['error'] = True
            elif(conf >= 2 and conf <= 11):
                for (i,conf_not) in zip(range(len(configs.storage['telegram']['notification']['Dilute_Game'])),configs.storage['telegram']['notification']['Dilute_Game']):
                    if(i == conf-2):
                        if(configs.storage['telegram']['notification']['Dilute_Game'][conf_not]):
                            configs.storage['telegram']['notification']['Dilute_Game'][conf_not] = False
                        else:
                            configs.storage['telegram']['notification']['Dilute_Game'][conf_not] = True

            elif(conf >= 12 and conf <= 21):
                for (i,conf_not) in zip(range(len(configs.storage['telegram']['notification']['Pattern_Game'])),configs.storage['telegram']['notification']['Pattern_Game']):
                    if(i == conf-12):
                        if(configs.storage['telegram']['notification']['Dilute_Game'][conf_not]):
                            configs.storage['telegram']['notification']['Pattern_Game'][conf_not] = False
                        else:
                            configs.storage['telegram']['notification']['Pattern_Game'][conf_not] = True

            elif(conf >= 22 and conf <= 31):
                for (i,conf_not) in zip(range(len(configs.storage['telegram']['notification']['Time_Game'])),configs.storage['telegram']['notification']['Time_Game']):
                    if(i == conf-22):
                        if(configs.storage['telegram']['notification']['Dilute_Game'][conf_not]):
                            configs.storage['telegram']['notification']['Time_Game'][conf_not] = False
                        else:
                            configs.storage['telegram']['notification']['Time_Game'][conf_not] = True
            else:
                return init_classes.bot_tg.send_message(f'Выбранный параметр несуществует. - {conf}')
        else:
            return init_classes.bot_tg.send_message(f'Вы ввели неверный параметр. - {conf}')
    send_configs.send_config_notifications(app_path)