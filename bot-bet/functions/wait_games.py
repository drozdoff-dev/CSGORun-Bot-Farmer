import datetime
import random
import sys
from colorama import Fore
import time
import locale

locale.setlocale(locale.LC_ALL, ('ru_RU', 'UTF-8'))


def bet(app_path,data):
    sys.path.insert(1, app_path + '/storage/temp/bot_bet/')
    import info_bets
    import configs
    import pattern_game

    import make_bet

    sys.path.insert(1, app_path + '/bot-bet/functions')
    import notifications

    sys.path.insert(1, app_path + '/storage/temp/global')
    import run_info
    
    skip = False
    if(data['type'] == "Time_Bet"):
        notifications.send(app_path,'Time_Bet','wait_time',f"Ожидаю времени {data['info']['time_bet']} для ставки.")
        while True:
            real_time = datetime.datetime.now().strftime("%H:%M")
            if(real_time >= data['info']['time_bet']):
                notifications.send(app_path,'Time_Bet','wait_time',f"Время {data['info']['time_bet']} настало.")
                break
    elif(data['type'] == "Pattern_Bet"):
        skip = True
    elif(data['type'] == "Dilute_Bet"):
        if(info_bets.storage['played_dilute_bets']['count_played_games'] > 0):
            skip = True
        else:
            pass
    else:
        return False
    
    #-------------------------#
    # if(info_bets.storage['before_bet']['type'] == "Pattern_Bet"):
    #     if(info_bets.storage['before_bet']['item'] == None and info_bets.storage['found_pattern']):
    #         notifications.send(app_path,"Pattern_Game",'found_pattern',f"Паттерн был обнаружен, но не было выбрано предмета для ставки, поэтому закупаю предмет по разбавочной стоимости для ставки.")
    #         info_bets.storage['before_bet']['type'] = None
    #         info_bets.storage['before_bet']['item'] = None
    #         info_bets.storage['before_bet']['cost'] = 0
    #         info_bets.storage['before_bet']['coef'] = 0

    #         data = {
    #             "type": "Dilute_Bet",
    #             "info": {},
    #             "coef_bet": configs.storage['auto_bet']['Dilute_Bet']['coef'],
    #             "cost_bet": configs.storage['auto_bet']['Dilute_Bet']['cost']
    #         }
            
    #         get_item = make_bet.get_item(app_path,data)
    #         if(get_item):
    #             info_bets.storage['before_bet']['type'] = "Dilute_Bet"
    #             info_bets.storage['before_bet']['item'] = get_item[0]
    #             info_bets.storage['before_bet']['cost'] = get_item[1]
    #             info_bets.storage['before_bet']['coef'] = get_item[2]

    #     elif(not info_bets.storage['found_pattern']):
    #         notifications.send(app_path,"Pattern_Game",'found_pattern',f"По итогу, комбинация не была обнаружена, поэтому закупаю предмет по разбавочной стоимости.")
    #         info_bets.storage['before_bet']['type'] = None
    #         info_bets.storage['before_bet']['item'] = None
    #         info_bets.storage['before_bet']['cost'] = 0
    #         info_bets.storage['before_bet']['coef'] = 0
            
    #         data = {
    #             "type": "Dilute_Bet",
    #             "info": {},
    #             "coef_bet": configs.storage['auto_bet']['Dilute_Bet']['coef'],
    #             "cost_bet": configs.storage['auto_bet']['Dilute_Bet']['cost']
    #         }
            
    #         get_item = make_bet.get_item(app_path,data)
    #         if(get_item):
    #             info_bets.storage['before_bet']['type'] = "Dilute_Bet"
    #             info_bets.storage['before_bet']['item'] = get_item[0]
    #             info_bets.storage['before_bet']['cost'] = get_item[1]
    #             info_bets.storage['before_bet']['coef'] = get_item[2]
    #-------------------------#

    if(not skip):
        notifications.send(app_path,data['type'],'bet',f"Ожидание конца нынешнего раунда для ставки.")
    while True:
        history_games = run_info.history_games
        last_game = history_games[0]
        if(last_game['id'] != info_bets.storage['last_save_game']['id'] or skip == True):
            info_bets.storage['last_save_game']['id'] = last_game['id']

            #print(info_bets.storage['before_bet']['type'])
            #if(configs.storage['bot-patterns']['search_by_dilute'] == "True" and info_bets.storage['before_bet']['type'] != "Pattern_Bet" and info_bets.storage['before_bet']['type'] != "Pattern_Bet_Near"):
            #    pattern_game.game(app_path,history_games)

            notifications.send(app_path, data['type'],'bet',f"Начинаю ставить ставку...")

            # if(info_bets.storage['before_bet']['type'] == "Pattern_Bet"):
            #     if(info_bets.storage['before_bet']['item'] == None):
            #         notifications.send(app_path,"Pattern_Game",'found_pattern',f"Паттерн был обнаружен, но не было выбрано предмета для ставки, поэтому пропускаю ставку.")
            #         info_bets.storage['before_bet']['type'] = None
            #         info_bets.storage['before_bet']['item'] = None
            #         info_bets.storage['before_bet']['cost'] = 0
            #         info_bets.storage['before_bet']['coef'] = 0
            #         break
            #     if(not info_bets.storage['found_pattern']):
            #         notifications.send(app_path,"Pattern_Game",'found_pattern',f"По итогу, комбинация не была обнаружена, поэтому пропускаю ставку.")
            #         info_bets.storage['before_bet']['type'] = None
            #         info_bets.storage['before_bet']['item'] = None
            #         info_bets.storage['before_bet']['cost'] = 0
            #         info_bets.storage['before_bet']['coef'] = 0
            #         break

            make_bet.make_bet(app_path,data)
            break
        # else:
        #      if(info_bets.storage['before_bet']['item'] == None):
        #         patterns = pattern_game.check_pattern(app_path,history_games)
        #         if(patterns[3] == True):
        #             game_count = patterns[2]
        #             pattern = patterns[1]
        #             pattern_reverse = patterns[1][::-1]
        #             notifications.send(app_path,"Pattern_Game",'found_pattern',f"Комбинация почти обнаружена - '{pattern_reverse}'/'{patterns[4]}', количество игр подряд по комбинации - {game_count}.\nНачинаю подготавливать ставку.")
        #             pattern_search = ('$'*game_count) + patterns[4]
        #             data = {
        #                     "type": "Pattern_Bet",
        #                     "info": {
        #                         "pattern": patterns[4],
        #                         "game_count": game_count
        #                     },
        #                     "coef_bet": configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_search]['coef'],
        #                     "cost_bet": configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_search]['cost']
        #                 }
        #             get_item = make_bet.get_item(app_path,data)
        #             if(get_item):
        #                 info_bets.storage['before_bet']['type'] = "Pattern_Bet"
        #                 info_bets.storage['before_bet']['item'] = get_item[0]
        #                 info_bets.storage['before_bet']['cost'] = get_item[1]
        #                 info_bets.storage['before_bet']['coef'] = get_item[2]
        #         else:
        #             data = {
        #                 "type": "Dilute_Bet",
        #                 "info": {},
        #                 "coef_bet": configs.storage['auto_bet']['Dilute_Bet']['coef'],
        #                 "cost_bet": configs.storage['auto_bet']['Dilute_Bet']['cost']
        #             }
                    
        #             get_item = make_bet.get_item(app_path,data)
        #             if(get_item):
        #                 info_bets.storage['before_bet']['type'] = "Dilute_Bet"
        #                 info_bets.storage['before_bet']['item'] = get_item[0]
        #                 info_bets.storage['before_bet']['cost'] = get_item[1]
        #                 info_bets.storage['before_bet']['coef'] = get_item[2]

def crash(app_path,type,wait_rounds=None,reason=None,newgen=True):
    sys.path.insert(1, app_path + '/storage/temp/bot_bet/')
    import info_bets
    import configs
    import info_game

    sys.path.insert(1, app_path + '/storage/temp/global')
    import run_info

    sys.path.insert(1, app_path + '/bot_bet/')
    import pattern_game

    sys.path.insert(1, app_path + '/bot-bet/functions')
    import notifications

    import make_bet

    if(type == 'Dilute_Bet'):
        if(wait_rounds == None):
            notifications.send(app_path,type,'crash',f"Ожидание краша...")
        while True:
            history_games = run_info.history_games
            last_game = history_games[0]
            if(last_game['id'] != info_bets.storage['last_save_game']['id']):
                info_bets.storage['last_save_game']['id'] = last_game['id']

                if(configs.storage['bot-patterns']['search_by_dilute'] == "True"):
                    pattern_game.game(app_path,history_games)
                    info_bets.storage['search_pattern'] = False
                if(last_game['crash'] <= info_game.storage['levels_coef']['crash'] and reason == None):
                    if(wait_rounds != None and newgen == True):
                        notifications.send(app_path,type,'crash',f"Во время пропуска раундов, случился новый краш.\nГенерирую новое число раундов для пропуска в указанном диапозоне {configs.storage['bot-start']['skip_min']}-{configs.storage['bot-start']['skip_max']}.")
                    else:
                        notifications.send(app_path,type,'crash',f"Произошёл краш.\nГенерирую число раундов для пропуска в указанном диапозоне {configs.storage['bot-start']['skip_min']}-{configs.storage['bot-start']['skip_max']}.")
                    if(newgen):
                        wait_rounds = random.randint(configs.storage['bot-start']['skip_min'], configs.storage['bot-start']['skip_max'])+1
                        notifications.send(app_path,type,'crash',f"Сгенерированное число раундов для пропуска равно - {wait_rounds-1}.")
                    info_bets.storage['played_dilute_bets']['count_played_games_row'] = 0
                if(wait_rounds != None):
                    wait_rounds -= 1
                    if(wait_rounds < 1):
                        break
                    # elif(wait_rounds == 1):
                    #     if(info_bets.storage['before_bet']['item'] == None):
                    #         patterns = pattern_game.check_pattern(app_path,history_games)
                    #         if(patterns[3] == True and configs.storage['bot-patterns']['search_by_dilute'] == "True"):
                    #             game_count = patterns[2]
                    #             pattern = patterns[1]
                    #             pattern_reverse = patterns[1][::-1]
                    #             notifications.send(app_path,"Pattern_Game",'found_pattern',f"Комбинация почти обнаружена - '{pattern_reverse}'/'{patterns[4]}', количество игр подряд по комбинации - {game_count}.\nНачинаю подготавливать ставку.")
                    #             pattern_search = ('$'*game_count) + patterns[4]
                    #             data = {
                    #                     "type": "Pattern_Bet",
                    #                     "info": {
                    #                         "pattern": patterns[4],
                    #                         "game_count": game_count
                    #                     },
                    #                     "coef_bet": configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_search]['coef'],
                    #                     "cost_bet": configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_search]['cost']
                    #                 }
                    #             get_item = make_bet.get_item(app_path,data)
                    #             if(get_item):
                    #                 info_bets.storage['before_bet']['type'] = "Pattern_Bet"
                    #                 info_bets.storage['before_bet']['item'] = get_item[0]
                    #                 info_bets.storage['before_bet']['cost'] = get_item[1]
                    #                 info_bets.storage['before_bet']['coef'] = get_item[2]
                    #         else:
                    #             data = {
                    #                 "type": "Dilute_Bet",
                    #                 "info": {},
                    #                 "coef_bet": configs.storage['auto_bet']['Dilute_Bet']['coef'],
                    #                 "cost_bet": configs.storage['auto_bet']['Dilute_Bet']['cost']
                    #             }
                    #             get_item = make_bet.get_item(app_path,data)
                    #             if(get_item):
                    #                 info_bets.storage['before_bet']['type'] = "Dilute_Bet"
                    #                 info_bets.storage['before_bet']['item'] = get_item[0]
                    #                 info_bets.storage['before_bet']['cost'] = get_item[1]
                    #                 info_bets.storage['before_bet']['coef'] = get_item[2]
                    #     notifications.send(app_path,type,'crash',f"Осталось пропустить раундов - {wait_rounds}.")
                    else:
                        notifications.send(app_path,type,'crash',f"Осталось пропустить раундов - {wait_rounds}.")

def wait_pattern_game(app_path):
    sys.path.insert(1, app_path + '/storage/temp/bot_bet/')
    import info_bets
    import configs

    sys.path.insert(1, app_path + '/storage/temp/global')
    import run_info

    sys.path.insert(1, app_path + '/bot_bet/')
    import pattern_game

    sys.path.insert(1, app_path + '/bot-bet/functions')
    import notifications

    import make_bet

    sys.path.insert(1, app_path + '/storage/temp/global')
    import init_classes

    rnd_seconds = round(random.randint(configs.storage['bot-patterns']['wait_seconds_min'], configs.storage['bot-patterns']['wait_seconds_max']))
    #print(rnd_seconds)
    if(rnd_seconds > 0):
        #print('ХУЙ')
        notifications.send(app_path,"Pattern_Game",'wait_pattern',f"Сгенерировал время для ожидания из диапозона {configs.storage['bot-patterns']['wait_seconds_min']}-{configs.storage['bot-patterns']['wait_seconds_max']}сек равное {rnd_seconds}сек.")
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=rnd_seconds)

    temp_seconds = 0
    temp_seconds_tg = 0
    #print(temp_seconds)
    id_message = init_classes.bot_tg.send_message(f"Буду ожидать комбинации ещё... [Идёт генерация времени ожидания]")
    while True:
        if(rnd_seconds > 0):
            real_time = datetime.datetime.now()

            difference = end_time - real_time
            seconds = int(difference.total_seconds())
            #minutes = seconds / 60
            #hours = minutes / 60
            #days = hours / 24

            #print(f'temp - {temp_seconds}')
            #print(f'notemp - {seconds}')
            if(temp_seconds != seconds):
                sys.stdout.write("\r")
                sys.stdout.write(Fore.CYAN + f"Буду ожидать комбинации ещё {time.strftime('%H часов, %M минут, %S секунд.', time.gmtime(seconds))}") 
                sys.stdout.flush()

                if(temp_seconds_tg >= seconds or temp_seconds_tg == 0):
                    init_classes.bot_tg.edit_message(id_message,f"Буду ожидать комбинации ещё {time.strftime('%H часов, %M минут, %S секунд.', time.gmtime(seconds))}")
                    temp_seconds_tg = seconds-5

                temp_seconds = seconds

            if(real_time >= end_time):
                sys.stdout.write("\r")
                init_classes.bot_tg.edit_message(id_message,f"Буду ожидать комбинации ещё {time.strftime('%H часов, %M минут, %S секунд.', time.gmtime(seconds))}")
                notifications.send(app_path,'Pattern_Game','wait_pattern',f"Закончил ожидание комбинаций, перехожу обратно к разбавочным играм.")
                break
        
        history_games = run_info.history_games
        last_game = history_games[0]
        
        if(last_game['id'] != info_bets.storage['last_save_game']['id']):
            sys.stdout.write("\r")
            info_bets.storage['last_save_game']['id'] = last_game['id']
            sys.path.insert(1, app_path + '/bot-bet/functions')

            # if(info_bets.storage['before_bet']['type'] == "Pattern_Bet"):
            #     if(info_bets.storage['before_bet']['item'] == None and info_bets.storage['found_pattern']):
            #         notifications.send(app_path,"Pattern_Game",'found_pattern',f"Паттерн был обнаружен, но не было выбрано предмета для ставки, комбинация пропущена.")
            #         info_bets.storage['before_bet']['type'] = None
            #         info_bets.storage['before_bet']['item'] = None
            #         info_bets.storage['before_bet']['cost'] = 0
            #         info_bets.storage['before_bet']['coef'] = 0
            #     if(not info_bets.storage['found_pattern']):
            #         notifications.send(app_path,"Pattern_Game",'found_pattern',f"По итогу, комбинация не была обнаружена, поэтому обнуляю ставочные значения.")
            #         info_bets.storage['before_bet']['type'] = None
            #         info_bets.storage['before_bet']['item'] = None
            #         info_bets.storage['before_bet']['cost'] = 0
            #         info_bets.storage['before_bet']['coef'] = 0

            #patterns = pattern_game.check_pattern(app_path,history_games)
            #pattern_game.game(app_path,history_games)
            #if(patterns[0] == True):
            #    pattern_game.game(app_path,history_games)

            pattern_game.game(app_path,history_games)
            if(info_bets.storage['search_pattern']):
                info_bets.storage['search_pattern'] = False
                if(configs.storage['bot-patterns']['wait_after_pattern'] == "False"):
                    notifications.send(app_path,'Pattern_Game','wait_pattern',f"Закончил ожидание комбинаций после найденной, перехожу обратно к разбавочным играм.")
                    break

            # patterns = pattern_game.check_pattern(app_path,history_games)
            # if(patterns[0] == True):
            #     pattern_game.game(app_path,history_games)
            #     if(configs.storage['bot-patterns']['wait_after_pattern'] == "False"):
            #         break
            # elif(patterns[3] == True):
            #     game_count = patterns[2]
            #     pattern = patterns[1]
            #     pattern_reverse = patterns[1][::-1]
            #     notifications.send(app_path,"Pattern_Game",'found_pattern',f"Комбинация почти обнаружена - '{pattern_reverse}'/'{patterns[4]}', количество игр подряд по комбинации - {game_count}.\nНачинаю подготавливать ставку.")
            #     pattern_search = ('$'*game_count) + patterns[4]
            #     data = {
            #             "type": "Pattern_Bet",
            #             "info": {
            #                 "pattern": patterns[4],
            #                 "game_count": game_count
            #             },
            #             "coef_bet": configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_search]['coef'],
            #             "cost_bet": configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_search]['cost']
            #         }
            #     get_item = make_bet.get_item(app_path,data)
            #     if(get_item):
            #         info_bets.storage['before_bet']['type'] = "Pattern_Bet"
            #         info_bets.storage['before_bet']['item'] = get_item[0]
            #         info_bets.storage['before_bet']['cost'] = get_item[1]
            #         info_bets.storage['before_bet']['coef'] = get_item[2]
            # else:
            #     info_bets.storage['before_bet']['type'] = None
            #     info_bets.storage['before_bet']['item'] = None
            #     info_bets.storage['before_bet']['cost'] = 0
            #     info_bets.storage['before_bet']['coef'] = 0