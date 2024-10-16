import configparser
import sys


def config(app_path):
    sys.path.insert(1, app_path + '/storage/temp/bot_bet/')
    import configs
    sys.path.insert(1, app_path + '/bot-bet/functions')
    import notifications

    config = configparser.ConfigParser()
    config.read_file(open(app_path + '/config/config.cfg'))

    notifications.log_console('debug','Чтение раздела Telegram')
    configs.storage['telegram']['messages_to_user'] = config.get('Telegram', 'messages_to_user')
    configs.storage['telegram']['messages_to_chats'] = config.get('Telegram', 'messages_to_chats')

    user_ids = config.get('Telegram', 'UserIDs').split(",")
    chat_ids = config.get('Telegram', 'ChatIDs').split(",")
    configs.storage['telegram']['token'] = config.get('Telegram', 'Token')
    configs.storage['telegram']['user_ids'] = user_ids
    configs.storage['telegram']['chat_ids'] = chat_ids