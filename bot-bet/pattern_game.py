

import datetime
import json
import random
import sys
import time


def game(app_path,history_games):
    import wait_games
    import make_bet

    sys.path.insert(1, app_path + '/storage/temp/bot_bet/')
    import configs

    sys.path.insert(1, app_path + '/bot-bet/functions')
    import notifications

    sys.path.insert(1, app_path + '/storage/temp/bot_bet/')
    import info_bets

    import result_game
    result_game.last(app_path,history_games[0])

    patterns = check_pattern(app_path,history_games)
    #print(patterns)
    pattern = patterns[1]
    game_count = patterns[5]
    pattern_search = ('$'*game_count) + pattern

    if(info_bets.storage['before_bet']['type'] == "Pattern_Bet_Near"):
        if(patterns[0] == True):
            if(info_bets.storage['before_bet']['item'] == None):
                notifications.send(app_path,"Pattern_Game",'found_pattern',f"Комбинация была обнаружена, но не было выбрано предмета для ставки, поэтому пропускаю ставку.")
                info_bets.storage['before_bet']['type'] = None
                info_bets.storage['before_bet']['item'] = None
                info_bets.storage['before_bet']['cost'] = 0
                info_bets.storage['before_bet']['coef'] = 0
            else:
                if(pattern in info_bets.storage['before_bet']['item']):
                    info_bets.storage['found_pattern'] = pattern
                    info_bets.storage['search_pattern'] = True
                    
                    notifications.send(app_path,"Pattern_Game",'found_pattern',f"Комбинация обнаружена - '{pattern}', количество игр подряд по комбинации - {game_count}.")
                    
                    while(game_count > 0):
                        game_count -= 1
                        data = {
                            "type": "Pattern_Bet",
                            "info": {
                                "pattern": pattern,
                                "game_count": game_count
                            },
                            "coef_bet": configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_search]['coef'],
                            "cost_bet": configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_search]['cost']
                        }
                        info_bets.storage['before_bet']['type'] = "Pattern_Bet"
                        wait_games.bet(app_path,data)
        else:
            #if(info_bets.storage['before_bet']['item'] != None):
            #    if(pattern in info_bets.storage['before_bet']['item']):
            notifications.send(app_path,"Pattern_Game",'found_pattern',f"По итогу, комбинации не были обнаружены.")
            info_bets.storage['before_bet']['type'] = None
            info_bets.storage['before_bet']['item'] = None
            info_bets.storage['before_bet']['cost'] = 0
            info_bets.storage['before_bet']['coef'] = 0

    if(len(patterns[3]) > 0):
        if(not isinstance(info_bets.storage['before_bet']['item'], dict) or not isinstance(info_bets.storage['before_bet']['cost'], dict) or not isinstance(info_bets.storage['before_bet']['coef'], dict)):
            info_bets.storage['before_bet']['item'] = {}
            info_bets.storage['before_bet']['cost'] = {}
            info_bets.storage['before_bet']['coef'] = {}

        for last_pattern_num in range(len(patterns[3])):
            crop_pattern = patterns[3][last_pattern_num]
            full_pattern = patterns[4][last_pattern_num]
            last_pattern_reverse = crop_pattern[::-1]
            game_count = patterns[2][last_pattern_num]
            notifications.send(app_path,"Pattern_Game",'found_pattern',f"Комбинация почти обнаружена - '{last_pattern_reverse}'/'{full_pattern}', количество игр подряд по комбинации - {game_count}.\nНачинаю подготавливать ставку.")
            pattern_search = ('$'*game_count) + full_pattern
            data = {
                    "type": "Pattern_Bet",
                    "info": {
                        "pattern": full_pattern,
                        "game_count": game_count
                    },
                    "coef_bet": configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_search]['coef'],
                    "cost_bet": configs.storage['auto_bet']['Pattern_Bet']['patterns'][pattern_search]['cost']
                }
            info_bets.storage['before_bet']['type'] = "Pattern_Bet_Near"
            get_item = make_bet.get_item(app_path,data)
            if(get_item):
                info_bets.storage['before_bet']['item'][full_pattern] = get_item[0]
                info_bets.storage['before_bet']['cost'][full_pattern] = get_item[1]
                info_bets.storage['before_bet']['coef'][full_pattern] = get_item[2]

    # if(len(patterns[3]) == 0):
    #     info_bets.storage['before_bet']['item'] = None
    #     info_bets.storage['before_bet']['cost'] = 0
    #     info_bets.storage['before_bet']['coef'] = 0

def check_pattern(app_path,history_games):
    sys.path.insert(1, app_path + '/storage/temp/bot_bet/')
    import configs
    import info_game

    sys.path.insert(1, app_path + '/storage/temp/bot_bet/')
    import info_bets

    sys.path.insert(1, app_path + '/storage/temp/global')
    import init_classes
    sys.path.insert(1, app_path + '/storage/temp/telegram_bot/')
    import info_bot_tg
    import info_user_tg

    sys.path.insert(1, app_path + '/bot-bet/functions')
    import notifications

    if(info_bets.storage['played_patterns_bets']['count_error_bet_row'] >= 3):
        info_user_tg.storage['active_page']['auth_csgorun'] = {}
        notifications.send(app_path,"Pattern_Game",'bet_item',f"Не удалось поставить по комбинации {info_bets.storage['played_patterns_bets']['count_error_bet_row']} раз(а).\nБыл получен бан комбинаций.\nДля очистки куки и токена для разблокировки необходимо произвести переавторизацию.\nВведите ниже Steam Guard - {configs.storage['main']['active_account']}, чтобы я мог произвести переавторизацию.")

        while('auth_csgorun' in info_user_tg.storage['active_page']):
            time.sleep(1)
    if(info_bets.storage['played_patterns_bets']['count_lose_bet_row'] >= 3):
        notifications.send(app_path,"Pattern_Game",'lose',f"Проиграно подряд комбинаций {info_bets.storage['played_patterns_bets']['count_error_bet_row']} раз(а).\nВозможен фикс комбинаций.\nВременная блокировка потока, до обновления с выбором вариантов действий в ТГ.")

        while True:
            time.sleep(1)

    result = False
    pattern_string = ''
    count_row_games = 0
    last_maybe_patterns = []
    send_full_patterns = []
    found_count = []
    found_pattern = ''
    count_found_game = 0
    for full_pattern in configs.storage['auto_bet']['Pattern_Bet']['patterns']:

        pattern_string = ''
        count_row_games_temp = full_pattern.count('$')

        full_pattern = full_pattern.replace('$', '')
        pattern_len = len(full_pattern)

        should_exit_before = False
        should_exit = False

        crop_pattern_history = history_games[:pattern_len-1][::-1]
        crop_full_pattern = full_pattern[::-1][:pattern_len-1]

        for (history_element, pat_game) in zip(crop_pattern_history, crop_full_pattern):
            count_row_games = count_row_games_temp

            search = search_game_pat(app_path,pat_game,history_element)
            if(not search):
                should_exit_before = True
                break
            else:
                pattern_string += pat_game

        if(not should_exit_before):
            #print(pattern_string)
            last_maybe_patterns.append(pattern_string)
            send_full_patterns.append(full_pattern)
            found_count.append(count_row_games)
        else:
            pattern_string = ''
            pattern_history = history_games[:pattern_len]
            full_pattern = full_pattern[:pattern_len]
            for (history_element, pat_game) in zip(pattern_history, full_pattern):
                if(not should_exit):
                    search = search_game_pat(app_path,pat_game,history_element)
                    if(not search):
                        should_exit = True
                        break
                    else:
                        pattern_string += pat_game

            if(not should_exit):
                found_pattern = pattern_string
                count_found_game = count_row_games
                result = True

    #print(last_maybe_patterns)
    if(found_pattern != ''):
        return [result, found_pattern, found_count, last_maybe_patterns, send_full_patterns, count_found_game]
    else:
        return [result, pattern_string, found_count, last_maybe_patterns, send_full_patterns, count_found_game]

def search_game_pat(app_path,pat_game,history_element):
    sys.path.insert(1, app_path + '/storage/temp/bot_bet/')
    import configs
    import info_game

    if(pat_game == 'r'):
        if(history_element['crash'] <= info_game.storage['levels_coef']['crash']):
            return True
        else:
            return False
    elif(pat_game == 'w'):
        if(history_element['crash'] >= info_game.storage['levels_coef']['blue']):
            return True
        else:
            return False
    elif(pat_game == 'b'):
        if(history_element['crash'] >= info_game.storage['levels_coef']['blue'] and history_element['crash'] < info_game.storage['levels_coef']['purple']):
            return True
        else:
            return False
    elif(pat_game == 'p'):
        if(history_element['crash'] >= info_game.storage['levels_coef']['purple'] and history_element['crash'] < info_game.storage['levels_coef']['green']):
            return True
        else:
            return False
    elif(pat_game == 'g'):
        if(history_element['crash'] >= info_game.storage['levels_coef']['green'] and history_element['crash'] < info_game.storage['levels_coef']['yellow']):
            return True
        else:
            return False
    elif(pat_game == 'y'):
        if(history_element['crash'] >= info_game.storage['levels_coef']['yellow'] and history_element['crash'] < info_game.storage['levels_coef']['turquoise']):
            return True
        else:
            return False
    elif(pat_game == 't'):
        if(history_element['crash'] >= info_game.storage['levels_coef']['turquoise']):
            return True
        else:
            return False
    elif(pat_game == '-'):
        if(history_element['crash']):
            return True
        else:
            return False