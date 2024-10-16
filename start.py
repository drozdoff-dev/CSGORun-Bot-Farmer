import os
import sys

if getattr(sys, 'frozen', False):
    name_script = os.path.basename(__file__)
    app_path = os.path.dirname(sys.executable).replace(name_script, '')
elif __file__:
    name_script = os.path.basename(__file__)
    app_path = os.path.dirname(__file__).replace(name_script, '')
sys.path.insert(1, app_path)

sys.path.insert(1, app_path + '/global/functions')
from csgorun_api import CsgoRunApi
sys.path.insert(1, app_path + '/bot-bet')
from bot_bet import BetBot
sys.path.insert(1, app_path + '/bot-telegram')
from bot_tg import TelegaBot

sys.path.insert(1, app_path + '/storage/temp/global')
import init_classes

if __name__ == "__main__":
    init_classes.bot_tg = TelegaBot(app_path)
    init_classes.run_api = CsgoRunApi()
    init_classes.bot_bet = BetBot(app_path)