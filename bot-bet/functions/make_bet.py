

import json
import random
import sys
import time

def get_item(app_path,data):
    sys.path.insert(1, app_path + '/storage/temp/global')
    import run_info
    from init_classes import run_api

    sys.path.insert(1, app_path + '/storage/temp/bot_bet/')
    import info_user
    import configs
    import info_bets

    sys.path.insert(1, app_path + '/bot-bet/functions')
    import notifications

    coef = round(random.uniform(data['coef_bet']['min'], data['coef_bet']['max']), 2)
    cost = round(random.uniform(data['cost_bet']['min'], data['cost_bet']['max']), 2)

    notifications.send(app_path,data['type'],'bet',f"Сгенерированная ставка в диапозоне от {data['cost_bet']['min']}$ до {data['cost_bet']['max']}$ = {cost}$.\nСгенерированный коэффициент в диапозоне от {data['coef_bet']['min']}$ до {data['coef_bet']['max']}$ = {coef}$.")

    bet_item = None

    user_full_info = run_info.account_info
    info_user.storage['balance'] = user_full_info['balance']
    if(len(user_full_info['items']) > 0):
        find_item = run_api.find_item(cost)
        cost_item = find_item["cost"]
        for item in user_full_info['items']:
            if(float(item['price']) == float(cost_item)):
                bet_item = item['id']
                notifications.send(app_path,data['type'],'bet',f"В профиле нашёлся подходящий предмет по стоимости ставки\n{item['name']} = {cost}$.")
                break

    if(bet_item == None):
        notifications.send(app_path,data['type'],'bet',f"В профиле не нашлось подходящих предметов по цене = {cost} для ставки.")
        if(float(info_user.storage['balance']) >= float(cost)):
            notifications.send(app_path,data['type'],'bet',f"Так как на балансе хватает денег для ставки {info_user.storage['balance']}$, то покупаю предмет за {cost}$.")
            find_item = run_api.find_item(cost)
            buy_item_id = find_item['id']
            if(buy_item_id != 0):
                tosleep = random.uniform(0.75, 1.4)
                time.sleep(tosleep)
                buy_result = run_api.buy_item(buy_item_id,configs.storage['accounts'][configs.storage['main']['active_account']]['cookie'],configs.storage['accounts'][configs.storage['main']['active_account']]['token'])
                if(buy_result):
                    bet_item = buy_result
                    notifications.send(app_path,data['type'],'buy_item',f"Предмет для ставки был куплен.")
                else:
                    notifications.send(app_path,data['type'],'bet',f"Во время покупки произошла непредвиденная проблема, сейчас проверю возможность обмена предметов.")
            else:
                notifications.send(app_path,data['type'],'bet',f"Во время покупки произошла ошибка связанная с заданной ценой - {cost}$.")
        if(bet_item == None):
            notifications.send(app_path,data['type'],'change_item',f"Приступаю к проверке возможности обмена.")
            items_costs = []
            items_costs_sort = []
            user_full_info = run_info.account_info
            for item in user_full_info['items']:
                
                if(info_bets.storage['found_pattern'] != False):
                    try:
                        json.loads(info_bets.storage['before_bet']['item'])
                        for pattern_item in info_bets.storage['before_bet']['item']:
                            print(pattern_item)
                            if(pattern_item != item['id']):
                                items_costs.append({
                                    "item_id": item['id'],
                                    "price": item['price'],
                                    "name": item['name'],
                                    "entity": item['entity']
                                })
                    except ValueError as e:
                        items_costs.append({
                            "item_id": item['id'],
                            "price": item['price'],
                            "name": item['name'],
                            "entity": item['entity']
                        })
                else:
                    items_costs.append({
                        "item_id": item['id'],
                        "price": item['price'],
                        "name": item['name'],
                        "entity": item['entity']
                    })

                items_costs_sort = sorted(items_costs,key=lambda x:x['price'])

            ready_change = False
            change_costs = 0.0
            items_change = []
            for cost_elem in items_costs_sort:
                change_costs += cost_elem['price']
                items_change.append(cost_elem['item_id'])
                if(round(change_costs, 2) >= round(cost, 2)):
                    ready_change = True
                    notifications.send(app_path,data['type'],'change_item',f"Сложив предметы по возростанию цены, можно потратить {round(change_costs, 2)}.:")
                    message_items = ''
                    for i in range(len(items_change)):
                        if(i == len(items_change)-1):
                            message_items += (f'{i} {items_costs_sort[i]["entity"]} | {items_costs_sort[i]["name"]} стоимостью {items_costs_sort[i]["price"]}$')
                        else:
                            message_items += (f'{i} {items_costs_sort[i]["entity"]} | {items_costs_sort[i]["name"]} стоимостью {items_costs_sort[i]["price"]}$\n')
                    notifications.send(app_path,data['type'],'change_item',message_items)
                    break
            if(ready_change):
                notifications.send(app_path,data['type'],'change_item',f"Начинаю обмен выбранных предметов.")
                if(len(items_change) > 0):
                    tosleep = random.uniform(0.75, 1.4)
                    time.sleep(tosleep)
                    find_item = run_api.find_item(cost)
                    sell_result = sell_items(app_path,items_change,find_item)
                    if(sell_result):
                        notifications.send(app_path,data['type'],'change_item',f"Обмен на предмет указанной стоимости прошёл успешно.")
                        bet_item = sell_result
                    else:
                        notifications.send(app_path,data['type'],'change_item',f"Не удалось обменять предметы.")
                else:
                    notifications.send(app_path,data['type'],'change_item',f"Нет предметов для обмена.")
            else:
                notifications.send(app_path,data['type'],'change_item',f"Суммы всех предметов не хватает для обмена на ставку по указанной стоимости.")
                if(cost > data['cost_bet']['min']):
                    notifications.send(app_path,data['type'],'bet',f"Так как случайное число из диапозона ставки больше минимального, то пробую поставить ставку сначала по минимальному значению из диапозона. А именно за {data['cost_bet']['min']}$")
                    data['cost_bet']['max'] = data['cost_bet']['min']
                    return get_item(app_path,data)
                notifications.send(app_path,data['type'],'bet',f"Никаким из образов не получилось поставить ставку, перехожу в режим ожидания депозита...\nПосле пополнения баланса я автоматически начну свою работу сначала.")
                wait_deposit(app_path,info_user.storage['balance'])

    if(bet_item != None):
        #print(bet_item)
        return [bet_item,cost,coef]
    else:
        notifications.send(app_path,data['type'],'bet',f"Неизвестная ошибка покупки, связанной с покупкой, обменом или продажей.")
        #info_bets.storage['before_bet']['type'] = None
        #info_bets.storage['before_bet']['item'] = None
        #info_bets.storage['before_bet']['cost'] = 0
        #info_bets.storage['before_bet']['coef'] = 0
        return False

def make_bet(app_path,data):
    sys.path.insert(1, app_path + '/storage/temp/global')
    import run_info
    from init_classes import run_api

    sys.path.insert(1, app_path + '/storage/temp/bot_bet/')
    import info_user
    import configs
    import info_bets

    sys.path.insert(1, app_path + '/bot-bet/functions')
    import notifications
    
    bet_item = info_bets.storage['before_bet']['item']
    cost = info_bets.storage['before_bet']['cost']
    coef = info_bets.storage['before_bet']['coef']

    if(info_bets.storage['found_pattern'] != False):
        bet_item = info_bets.storage['before_bet']['item'][info_bets.storage['found_pattern']]
        cost = info_bets.storage['before_bet']['cost'][info_bets.storage['found_pattern']]
        coef = info_bets.storage['before_bet']['coef'][info_bets.storage['found_pattern']]

    if(bet_item != None):
        #print(bet_item)
        while True:
            tosleep = random.uniform(1.5, 2.0)
            time.sleep(tosleep)
            last_game = run_info.history_games[0]
            if(last_game['id'] == info_bets.storage['last_save_game']['id']):
                bet_status = run_api.make_bet(bet_item,coef,configs.storage['accounts'][configs.storage['main']['active_account']]['cookie'],configs.storage['accounts'][configs.storage['main']['active_account']]['token'])
                #print(bet_status)
                if(bet_status):
                    if(data['type'] == 'Pattern_Bet'):
                        info_bets.storage['played_patterns_bets']['count_error_bet_row'] = 0

                    info_bets.storage['active_bet']['coef'] = coef
                    info_bets.storage['active_bet']['cost'] = cost
                    info_bets.storage['active_bet']['type'] = data['type']
                    info_bets.storage['active_bet']['info'] = data['info']
                    notifications.send(app_path,data['type'],'bet',f"Ставка размером {cost}$ успешно поставлена на {coef}x.")
                    info_bets.storage['before_bet']['type'] = None
                    info_bets.storage['before_bet']['item'] = None
                    info_bets.storage['before_bet']['cost'] = 0
                    info_bets.storage['before_bet']['coef'] = 0
                    info_bets.storage['found_pattern'] = False
                    break
            else:
                if(data['type'] == 'Pattern_Bet'):
                    info_bets.storage['played_patterns_bets']['count_error_bet_row'] += 1

                notifications.send(app_path,data['type'],'bet',f"Не успел поставить ставку на прошлой игре, приступаю к новой итерации...")
                #info_bets.storage['before_bet']['type'] = None
                info_bets.storage['before_bet']['item'] = None
                info_bets.storage['before_bet']['cost'] = 0
                info_bets.storage['before_bet']['coef'] = 0
                info_bets.storage['found_pattern'] = False
                break
    else:
        notifications.send(app_path,data['type'],'bet',f"Неизвестная ошибка ставки, связанной с покупкой, обменом или продажей.")
        #info_bets.storage['before_bet']['type'] = None
        info_bets.storage['before_bet']['item'] = None
        info_bets.storage['before_bet']['cost'] = 0
        info_bets.storage['before_bet']['coef'] = 0
        info_bets.storage['found_pattern'] = False

def sell_items(app_path,user_items,find_item):
    sys.path.insert(1, app_path + '/storage/temp/global')
    from init_classes import run_api

    sys.path.insert(1, app_path + '/storage/temp/bot_bet/')
    import configs

    buy_item_id = find_item['id']
    return run_api.exchange_items(user_items,buy_item_id,configs.storage['accounts'][configs.storage['main']['active_account']]['cookie'],configs.storage['accounts'][configs.storage['main']['active_account']]['token'])

def wait_deposit(app_path,balance):
    sys.path.insert(1, app_path + '/storage/temp/global')
    import run_info

    sys.path.insert(1, app_path + '/storage/temp/bot_bet/')
    import info_user

    while True:
        user_full_info = run_info.account_info
        info_user.storage['balance'] = user_full_info['balance']
        if(balance != info_user.storage['balance']):
            print('Изменение счёта зафиксировано, перехожу в режим ставок')
            break