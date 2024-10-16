import sys
import telebot
from telebot import types
from threading import Thread

class TelegaBot():
    def __init__(self,app_path):
        self.app_path = app_path

        sys.path.insert(1, self.app_path + '/bot-telegram/functions')
        import init_tg
        import wait_commands

        init_tg.config(self.app_path)

        sys.path.insert(1, app_path + '/storage/temp/bot_bet/')
        import configs

        self.bot_tg = telebot.TeleBot(configs.storage['telegram']['token'])
        wait_commands.wait(self.app_path,self.bot_tg)

        t_polling = Thread(target=self.bot_tg.polling,kwargs={'none_stop':True,'interval':0})
        t_polling.daemon = True
        t_polling.start()

        #self.send_message('Скрипт запущен и ожидает ваших дальнейших команд.\nстарт - для запуска бота\nпомощь - для получения всех команд бота')


    def send_message(self,message,parse_mode=None,reply_markup=None):
        sys.path.insert(1, self.app_path + '/storage/temp/bot_bet/')
        import configs

        ids_user_messages = []
        ids_chat_messages = []

        if(configs.storage['telegram']['messages_to_user'] == "True"):
            for user_id in configs.storage['telegram']['user_ids']:
                id = self.bot_tg.send_message(user_id, message, parse_mode, reply_markup=reply_markup)
                ids_user_messages.append(id.message_id)
        if(configs.storage['telegram']['messages_to_chats'] == "True"):
            for chat_id in configs.storage['telegram']['chat_ids']:
                id = self.bot_tg.send_message(chat_id, message, parse_mode, reply_markup=reply_markup)
                ids_chat_messages.append(id.message_id)

        return [ids_user_messages,ids_chat_messages]

    def edit_message(self,ids_messages,message,parse_mode=None):
        sys.path.insert(1, self.app_path + '/storage/temp/bot_bet/')
        import configs

        if(configs.storage['telegram']['messages_to_user'] == "True"):
            for id_message in ids_messages[0]:
                for user_id in configs.storage['telegram']['user_ids']:
                    self.bot_tg.edit_message_text(chat_id = user_id, message_id = id_message, text = message, parse_mode = parse_mode)
        if(configs.storage['telegram']['messages_to_chats'] == "True"):
            for id_message in ids_messages[1]:
                for chat_id in configs.storage['telegram']['chat_ids']:
                    self.bot_tg.edit_message_text(chat_id = chat_id, message_id = id_message, text = message, parse_mode = parse_mode)