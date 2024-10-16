import sys
import colorama
from colorama import Fore, Back, Style
colorama.init()

def log_console(type,text):
    if(type == "log"):
        print(Fore.BLUE + f'[LOG] ' + Fore.WHITE + text)
    elif(type == "debug"):
        print(Fore.MAGENTA + f'[DEBUG] ' + Fore.WHITE + text)
    elif(type == "error"):
        print(Fore.RED + f'[ERROR] ' + Fore.WHITE + text)
    elif(type == "win"):
        print(Fore.LIGHTGREEN_EX + f'[WIN] ' + Fore.WHITE + text)
    elif(type == "lose"):
        print(Fore.LIGHTBLUE_EX + f'[LOSE] ' + Fore.WHITE + text)
    elif(type == "info"):
        print(Fore.CYAN + f'[INFO] ' + Fore.WHITE + text)

def send(app_path,type_game,type_notify,text):
    sys.path.insert(1, app_path + '/storage/temp/bot_bet/')
    import configs

    sys.path.insert(1, app_path + '/storage/temp/global')
    import init_classes

    names_notify = {
        "titles": {
            "Dilute_Game": 'Разбавочные',
            "Pattern_Game": 'Комбинации',
            "Time_Game": 'По времени'
        },
        "desc": {
            "bet": 'Ставка',
            "win": 'Победа',
            "lose": 'Проигрыш',
            "crash": 'Краш',
            "bet_item": 'Поставил',
            "buy_item": 'Купил',
            "change_item": 'Обмен',
            "skip_rounds": 'Пропуск',
            "skip_count": 'Количество пропусков',
            "wait_pattern": 'Ожидание комбинации',
            "found_pattern": 'Комбинация найдена',
            "wait_time": 'Оставшееся время'
        }
    }
    colors_notify = {
        "titles": {
            "Dilute_Game": Fore.CYAN,
            "Pattern_Game": Fore.GREEN,
            "Time_Game": Fore.BLUE
        },
        "desc": {
            "bet": Fore.LIGHTMAGENTA_EX,
            "win": Fore.LIGHTGREEN_EX,
            "lose": Fore.RED,
            "crash": Fore.LIGHTRED_EX,
            "bet_item": Fore.LIGHTGREEN_EX,
            "buy_item": Fore.MAGENTA,
            "change_item": Fore.YELLOW,
            "skip_rounds": Fore.LIGHTRED_EX,
            "skip_count": Fore.LIGHTRED_EX,
            "wait_pattern": Fore.GREEN,
            "found_pattern": Fore.LIGHTGREEN_EX,
            "wait_time": Fore.LIGHTWHITE_EX
        }
    }

    message_id = 0

    if(type_game == 'Dilute_Bet'):
        type_game = 'Dilute_Game'
    elif(type_game == 'Pattern_Bet'):
        type_game = 'Pattern_Game'
    elif(type_game == 'Time_Bet'):
        type_game = 'Time_Game'

    notify = configs.storage['telegram']['notification'][type_game]
    for notify in configs.storage['telegram']['notification'][type_game]:
        text_console = text.replace('\n','\n' + colors_notify["titles"][type_game] + f'[{names_notify["titles"][type_game]}]' + colors_notify["desc"][type_notify] + f'[{names_notify["desc"][notify]}] ' + Fore.WHITE)
        console = colors_notify["titles"][type_game] + f'[{names_notify["titles"][type_game]}]' + colors_notify["desc"][type_notify] + f'[{names_notify["desc"][notify]}]' + Fore.WHITE + f' {text_console}'
        if(notify == type_notify):
            if(notify):
                text = text.replace('_','-')
                text = text.replace('*','!')
                text = text.replace('~~','"')
                text = text.replace('`','"')
                text = text.replace('||','|')
                text_message = text.replace('\n',f'_\n*[{names_notify["titles"][type_game]}][{names_notify["desc"][notify]}]* _')
                separator = 3096
                chunks = [text_message[i:i+separator] for i in range(0, len(text_message), separator)]
                for fragment in chunks:
                    message = (f'*[{names_notify["titles"][type_game]}][{names_notify["desc"][notify]}]* - _{fragment}_')
                    message_id = init_classes.bot_tg.send_message(message,parse_mode="Markdown")
            print(console)
    if(message_id != 0):
        return message_id
    