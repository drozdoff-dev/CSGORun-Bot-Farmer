
import random
import sys


def game(app_path):
    sys.path.insert(1, app_path + '/storage/temp/bot_bet/')
    import info_bets
    import configs

    import wait_games

    sys.path.insert(1, app_path + '/bot-bet/functions')
    import notifications

    import make_bet

    sys.path.insert(1, app_path + '/bot-bet/')
    import pattern_game

    sys.path.insert(1, app_path + '/storage/temp/global')
    import run_info
    
    if(info_bets.storage['played_dilute_bets']['ring_size'] == 0):
        notifications.send(app_path,"Dilute_Game",'skip_count',f"Генерирую размер круга для разбавочных игр из указанного диапозона {configs.storage['bot-dilute']['rounds_min']}-{configs.storage['bot-dilute']['rounds_max']}.")
        info_bets.storage['played_dilute_bets']['ring_size'] = random.randint(configs.storage['bot-dilute']['rounds_min'], configs.storage['bot-dilute']['rounds_max'])
        notifications.send(app_path,"Dilute_Game",'skip_count',f"Размер сгенерированного круга составляет - {info_bets.storage['played_dilute_bets']['ring_size']} раундов.")
    elif(info_bets.storage['played_dilute_bets']['ring_size'] <= info_bets.storage['played_dilute_bets']['count_played_games']):
        notifications.send(app_path,"Dilute_Game",'wait_pattern',f"Круг из {info_bets.storage['played_dilute_bets']['ring_size']} разбавочных ставок пройден.\nОбнуляю количество пройденных игр.\nПерехожу в ожидание паттерна.")
        info_bets.storage['played_dilute_bets']['ring_size'] = random.randint(configs.storage['bot-dilute']['rounds_min'], configs.storage['bot-dilute']['rounds_max'])
        info_bets.storage['played_dilute_bets']['count_played_games'] = 0
        info_bets.storage['played_dilute_bets']['count_played_games_row'] = 0
        wait_games.wait_pattern_game(app_path)

    if(info_bets.storage['played_dilute_bets']['row_size'] == 0):
        notifications.send(app_path,"Dilute_Game",'skip_count',f"Генерирую размер линии для разбавочных игр из указанного диапозона {configs.storage['bot-dilute']['row_min']}-{configs.storage['bot-dilute']['row_max']}.")
        info_bets.storage['played_dilute_bets']['row_size'] = random.randint(configs.storage['bot-dilute']['row_min'], configs.storage['bot-dilute']['row_max'])
        notifications.send(app_path,"Dilute_Game",'skip_count',f"Размер сгенерированной линии составляет - {info_bets.storage['played_dilute_bets']['row_size']} раундов.")
    elif(info_bets.storage['played_dilute_bets']['row_size'] <= info_bets.storage['played_dilute_bets']['count_played_games_row']):
        info_bets.storage['played_dilute_bets']['row_size'] = random.randint(configs.storage['bot-dilute']['row_min'], configs.storage['bot-dilute']['row_max'])
        info_bets.storage['played_dilute_bets']['count_played_games_row'] = 0

        if(configs.storage['bot-dilute']['skip_rounds_row'] == "True"):
            notifications.send(app_path,"Dilute_Game",'skip_rounds',f"Приступаю к пропуску раундов, ведь завышено сгенерированное число ставок подряд.")
            skip_rounds = random.randint(configs.storage['bot-dilute']['skip_row_min'], configs.storage['bot-dilute']['skip_row_max'])+1
            notifications.send(app_path,"Dilute_Game",'skip_count',f"Сгенерировал число для пропуска раундов из указанного диапозона {configs.storage['bot-dilute']['skip_row_min']}-{configs.storage['bot-dilute']['skip_row_max']}.\nОжидаю {skip_rounds} раундов")
            wait_games.crash(app_path,'Dilute_Bet',skip_rounds,'skip',newgen=False)

        if(configs.storage['bot-dilute']['wait_crash_row'] == "True"):
            if(configs.storage['bot-dilute']['skip_rounds_row'] == "True"):
                notifications.send(app_path,"Dilute_Game",'crash',f"Приступаю к ожидаю краша после пропущенных раундов.")
            else:
                notifications.send(app_path,"Dilute_Game",'crash',f"Приступаю к ожидаю краша после линии игр.")
            wait_games.crash(app_path,'Dilute_Bet')

    data = {
        "type": "Dilute_Bet",
        "info": {},
        "coef_bet": configs.storage['auto_bet']['Dilute_Bet']['coef'],
        "cost_bet": configs.storage['auto_bet']['Dilute_Bet']['cost']
    }
    if(info_bets.storage['played_dilute_bets']['ring_size'] >= info_bets.storage['played_dilute_bets']['count_played_games'] or info_bets.storage['played_dilute_bets']['row_size'] >= info_bets.storage['played_dilute_bets']['count_played_games_row']):
        #history_games = run_info.history_games
        #if(configs.storage['bot-patterns']['search_by_dilute'] == "True"):
        #    pattern_game.game(app_path,history_games)
        if(info_bets.storage['before_bet']['type'] != "Pattern_Bet" and info_bets.storage['active_bet']['type'] != "Pattern_Bet"):
            get_item = make_bet.get_item(app_path,data)
            if(get_item):
                info_bets.storage['before_bet']['type'] = "Dilute_Bet"
                info_bets.storage['before_bet']['item'] = get_item[0]
                info_bets.storage['before_bet']['cost'] = get_item[1]
                info_bets.storage['before_bet']['coef'] = get_item[2]
                wait_games.bet(app_path,data)