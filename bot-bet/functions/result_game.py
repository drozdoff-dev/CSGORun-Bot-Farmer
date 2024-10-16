
import random
import sys


def last(app_path,last_game):
    sys.path.insert(1, app_path + '/storage/temp/bot_bet/')
    import info_bets
    import configs
    import info_game
    import info_user

    import wait_games

    sys.path.insert(1, app_path + '/storage/temp/global')
    import run_info
    user_full_info = run_info.account_info
    if(user_full_info != {}):
        info_user.storage['balance'] = user_full_info['balance']

    sys.path.insert(1, app_path + '/bot-bet/functions')
    import notifications
    
    type_bet = info_bets.storage['active_bet']['type']
    info_bets.storage['active_bet']['type'] = None

    if(type_bet != None):
        status_last_active_bet = None
        new_cost_user = 0
        
        if(info_bets.storage['active_bet']['coef'] <= last_game['crash']):
            status_last_active_bet = "Win"
            new_cost_user = info_bets.storage['active_bet']['cost']*info_bets.storage['active_bet']['coef']
        else:
            status_last_active_bet = "Lose"
            new_cost_user = 0

        if(type_bet == "Time_Bet"):
            info_bets.storage['played_time_bets'][info_bets.storage['active_bet']['info']['time_bet']] = {
                "coef": info_bets.storage['active_bet']['coef'],
                "cost": info_bets.storage['active_bet']['cost'],
                "status": status_last_active_bet
            }
            if(status_last_active_bet == "Win"):
                notifications.send(app_path,'Time_Bet','win',f"Выиграл ставку. Ставка: {info_bets.storage['active_bet']['cost']}, Выиграл: {new_cost_user}. Баланс: {info_user.storage['balance']}")
            elif(status_last_active_bet == "Lose"):
                notifications.send(app_path,'Time_Bet','lose',f"Проиграл ставку. Ставка: {info_bets.storage['active_bet']['cost']}. Баланс: {info_user.storage['balance']}")

        elif(type_bet == "Pattern_Bet"):
            if(status_last_active_bet == "Win"):
                notifications.send(app_path,'Pattern_Bet','win',f"Выиграл ставку. Ставка: {info_bets.storage['active_bet']['cost']}, Выиграл: {new_cost_user}. Баланс: {info_user.storage['balance']}")
                info_bets.storage['played_patterns_bets']['count_lose_bet_row'] = 0
            elif(status_last_active_bet == "Lose"):
                notifications.send(app_path,'Pattern_Bet','lose',f"Проиграл ставку. Ставка: {info_bets.storage['active_bet']['cost']}. Баланс: {info_user.storage['balance']}")
                info_bets.storage['played_patterns_bets']['count_lose_bet_row'] += 1
            # info_bets.storage['before_bet']['type'] = None
            # info_bets.storage['before_bet']['item'] = None
            # info_bets.storage['before_bet']['cost'] = 0
            # info_bets.storage['before_bet']['coef'] = 0
            # info_bets.storage['found_pattern'] = False

        elif(type_bet == "Dilute_Bet"):
            if(status_last_active_bet == "Win"):
                info_bets.storage['played_dilute_bets']['count_played_games_row'] += 1
                info_bets.storage['played_dilute_bets']['count_played_games'] += 1
                notifications.send(app_path,'Dilute_Bet','win',f"Выиграл ставку. Ставка: {info_bets.storage['active_bet']['cost']}, Выиграл: {new_cost_user}. Баланс: {info_user.storage['balance']}")
            elif(status_last_active_bet == "Lose"):
                notifications.send(app_path,'Dilute_Bet','lose',f"Проиграл ставку. Ставка: {info_bets.storage['active_bet']['cost']}. Баланс: {info_user.storage['balance']}")
                if(configs.storage['bot-dilute']['pause_by_lose'] == "True"):
                    pause_rounds = random.randint(configs.storage['bot-dilute']['pause_min'], configs.storage['bot-dilute']['pause_max'])
                    notifications.send(app_path,'Dilute_Bet','skip_rounds',f"Пропуск раундов при проигрыше.\nСгенерированное число раундов для пропуска {pause_rounds}.\nУстановленный диапозон {configs.storage['bot-dilute']['pause_min']}-{configs.storage['bot-dilute']['pause_max']}.")
                    wait_games.crash(app_path,'Dilute_Bet',pause_rounds,newgen=True)
                else:
                    info_bets.storage['played_dilute_bets']['count_played_games_row'] += 1
                    info_bets.storage['played_dilute_bets']['count_played_games'] += 1

            if(float(last_game['crash']) < float(info_game.storage['levels_coef']['blue']) and configs.storage['bot-dilute']['pause_by_crash'] == "True"):
                if(status_last_active_bet == "Lose" and configs.storage['bot-dilute']['pause_by_lose']):
                    return
                
                #info_bets.storage['played_dilute_bets']['count_played_games_row'] += 1
                pause_rounds = random.randint(configs.storage['bot-start']['skip_min'], configs.storage['bot-start']['skip_max'])
                notifications.send(app_path,'Dilute_Bet','crash',f"Пропуск раундов при краше.\nСгенерированное число раундов для пропуска {pause_rounds}.\nУстановленный диапозон {configs.storage['bot-start']['skip_min']}-{configs.storage['bot-start']['skip_max']}.")
                wait_games.crash(app_path,'Dilute_Bet',pause_rounds,reason=None,newgen=True)
            notifications.send(app_path,"Dilute_Game",'skip_count',f"Круг пройден на {info_bets.storage['played_dilute_bets']['count_played_games']} из {info_bets.storage['played_dilute_bets']['ring_size']}.\nЛиния пройдена на {info_bets.storage['played_dilute_bets']['count_played_games_row']} из {info_bets.storage['played_dilute_bets']['row_size']}.")
