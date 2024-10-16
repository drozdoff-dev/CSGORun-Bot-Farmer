from datetime import date
import random
import sys
import time



def run_check(app_path):
    sys.path.insert(1, app_path + '/storage/temp/global')
    import init_classes
    import run_info

    sys.path.insert(1, app_path + '/storage/temp/bot_bet/')
    import configs
    import info_bets

    while True:
        if(configs.storage['today'] != date.today()):
            info_bets.storage['played_time_bets'] = {}
            configs.storage['today'] = date.today()

        run_info.history_games = init_classes.run_api.get_history_games()
        run_info.account_info = init_classes.run_api.get_info_account(configs.storage['accounts'][configs.storage['main']['active_account']]['cookie'], configs.storage['accounts'][configs.storage['main']['active_account']]['token'])
        time.sleep(random.uniform(0.5,1.5))
