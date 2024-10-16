from typing import Dict
from unittest import result
from urllib import response
import requests
import json

class CsgoRunApi:
    def __init__(self) -> None:
        self.history_url = 'https://api.csgo3.run/current-state?montaznayaPena=null'
        self.items_url = 'https://cloud.this.team/csgo/items.json'
        self.exchange_items_url = 'https://api.csgo3.run/marketplace/exchange-items'
        self.make_bet_url = 'https://api.csgo3.run/make-bet'
    
    def get_history_games(self) -> dict:
        response = requests.get(self.history_url)
        history = response.json()['data']['game']['history']
        return history
    
    def get_info_account(self,cookie,token) -> dict:
        response = requests.get(self.history_url, headers={
			'cookie': cookie,
			'authorization': f"JWT {token}"
        })
        return response.json()['data']['user']

    def get_current_items(self,cookie,token) -> dict:
        response = requests.get(self.history_url, headers={
			'cookie': cookie,
			'authorization': f"JWT {token}"
        })
        items = response.json()['data']['user']['items']
        items_list = []
        for item in items:
            items_list.append(item['id'])
        return items_list

    def find_item(self, cost: float):
        response = requests.get(self.items_url).json()
        skin_max = None
        max_price = 0
        for skin_info in response['data']:
            if max_price - 0.01 == cost:
                break
            item_price = skin_info[6]
            if item_price <= cost and item_price > max_price:
                skin_max = skin_info
                max_price = item_price
        return {"id": skin_max[0], "cost": max_price}
    
    def buy_item(self, id: int, cookie, token) -> int:
        response = requests.post(self.exchange_items_url, headers={
            'cookie': cookie,
            'authorization': f"JWT {token}"
        }, json={"userItemIds":[], "wishItemIds":[id]}).json()
		
        if('success' in response.keys()):
            if(response['success'] == True):
                return response['data']['userItems']['newItems'][0]['id']
            else:
                return False
        else:
            return False
        
    def make_bet(self, itemid: int, coef: float, cookie, token) -> bool:
        response = requests.post(self.make_bet_url, headers={
			'cookie': cookie,
			'authorization': f"JWT {token}"
        }, json={"userItemIds":[itemid], "auto":str(coef)}).json()
        if('success' in response.keys()):
            if(response['success'] == True):
                return True
            else:
                return False
        else:
            return False
        
    def exchange_items(self, myitems: dict, buy_item_id: int, cookie, token):
        response = requests.post(self.exchange_items_url, headers={
			'cookie': cookie,
			'authorization': f"JWT {token}"
		}, json={"userItemIds":myitems, "wishItemIds":[buy_item_id]}).json()

        if('success' in response.keys()):
            if(response['success'] == True):
                return response['data']['userItems']['newItems'][0]['id']
            else:
                return False
        else:
            return False