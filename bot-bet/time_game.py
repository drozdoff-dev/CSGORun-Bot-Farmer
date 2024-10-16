

import datetime
import sys


def game(app_path):
    import wait_games

    sys.path.insert(1, app_path + '/storage/temp/bot_bet/')
    import info_bets
    import configs
    
    if(len(configs.storage['auto_bet']['Time_Bet']) > 0):
        for time_bet in configs.storage['auto_bet']['Time_Bet']:
            real_time = datetime.datetime.now().strftime("%H:%M")

            start = datetime.datetime.strptime(time_bet, "%H:%M")
            end = datetime.datetime.strptime(real_time, "%H:%M")

            difference = start - end
            difference = int(difference.total_seconds() / 60)
            if(difference <= 2 and difference >= 0):
                if(not time_bet in info_bets.storage['played_time_bets']):
                    data = {
                        "type": "Time_Bet",
                        "info": {
                            "time_bet": time_bet
                        },
                        "coef_bet": configs.storage['auto_bet']['Time_Bet'][time_bet]['coef'],
                        "cost_bet": configs.storage['auto_bet']['Time_Bet'][time_bet]['cost']
                    }
                    wait_games.bet(app_path,data)
                    break