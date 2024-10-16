import os
import sys
from threading import Thread

from colorama import Fore
import requests

class BetBot():
    def __init__(self,app_path):
        self.app_path = app_path
        sys.path.insert(1, self.app_path + '/bot-bet/functions')
        import init_bet
        sys.path.insert(1, app_path + '/storage/temp/global')
        import init_classes

        text_message = f'Начинаю запуск скрипта...'
        id_message = init_classes.bot_tg.send_message(text_message)

        init_bet.config(self.app_path,id_message,text_message)

        sys.path.insert(1, self.app_path + '/global/functions')
        import loop_read_api

        t_check_api = Thread(target=loop_read_api.run_check,kwargs={'app_path':self.app_path})
        t_check_api.daemon = True
        t_check_api.start()

        self.start_bot()

    def start_bot(self):
        sys.path.insert(1, self.app_path + '/storage/temp/global')
        import init_classes

        sys.path.insert(1, self.app_path + '/storage/temp/bot_bet/')
        import info_bot

        sys.stdout.write("\r")
        sys.stdout.write(Fore.CYAN + "Ожидаю включения...") 
        sys.stdout.flush()
        while True:
            if(not info_bot.storage['bot_started']):
                pass
            else:
                sys.stdout.write("\r")
                sys.stdout.flush()
                try:
                    self.main_cycle()
                except (requests.exceptions.ConnectionError, requests.exceptions.JSONDecodeError) as e:
                    pass
                if(info_bot.storage['has_stopped']):
                    info_bot.storage['has_stopped'] = False
                    info_bot.storage['bot_started'] = False
                    init_classes.bot_tg.send_message(f'Бот был выключен')

        

    def main_cycle(self):
        sys.path.insert(1, self.app_path + '/storage/temp/global')
        import run_info

        sys.path.insert(1, self.app_path + '/storage/temp/bot_bet/')
        import info_bets
        import configs
        import info_bot

        sys.path.insert(1, self.app_path + '/bot-bet/functions')
        import result_game

        sys.path.insert(1, self.app_path + '/bot_bet/')
        import pattern_game
        import dilute_game
        import time_game

        import wait_games
        import make_bet

        sys.path.insert(1, self.app_path + '/bot-bet/functions')
        import notifications

        history_games = run_info.history_games
        if(len(history_games) > 0):
            last_game = history_games[0]
            if(last_game['id'] != info_bets.storage['last_save_game']['id']):
                info_bets.storage['last_save_game']['id'] = last_game['id']

                result_game.last(self.app_path,last_game)
                time_game.game(self.app_path)
                if(configs.storage['bot-patterns']['search_by_dilute'] == "True"):
                    pattern_game.game(self.app_path,history_games)
                    info_bets.storage['search_pattern'] = False

                if(configs.storage['bot-start']['wait_crash'] == "True"):
                    wait_games.crash(self.app_path,'Dilute_Bet')
                    configs.storage['bot-start']['wait_crash'] = "False"

                dilute_game.game(self.app_path)
            # else:
            #     if(info_bets.storage['before_bet']['item'] == None):
            #         patterns = pattern_game.check_pattern(self.app_path,history_games)
            #         if(patterns[3] == True):
            #             game_count = patterns[2]
            #             pattern = patterns[1]
            #             pattern_reverse = patterns[1][::-1]
            #             notifications.send(self.app_path,"Pattern_Game",'found_pattern',f"Комбинация почти обнаружена - '{pattern_reverse}'/'{patterns[4]}', количество игр подряд по комбинации - {game_count}.\nНачинаю подготавливать ставку.")
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
            #             get_item = make_bet.get_item(self.app_path,data)
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
                        
            #             get_item = make_bet.get_item(self.app_path,data)
            #             if(get_item):
            #                 info_bets.storage['before_bet']['type'] = "Dilute_Bet"
            #                 info_bets.storage['before_bet']['item'] = get_item[0]
            #                 info_bets.storage['before_bet']['cost'] = get_item[1]
            #                 info_bets.storage['before_bet']['coef'] = get_item[2]