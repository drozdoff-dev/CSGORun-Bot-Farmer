def auth_user(app_path,guard):
    import configparser
    import pickle
    import sys
    import json

    import configs

    import notifications

    import init_classes

    import info_bot_tg
    import info_user_tg
    
    config = configparser.ConfigParser()
    config.read_file(open(app_path + '/config/config.cfg'))

    login = configs.storage['accounts'][config.get('MAIN', 'active_account')]['login']
    password = configs.storage['accounts'][config.get('MAIN', 'active_account')]['password']

    import steam.webauth as wa

    init_classes.bot_tg.send_message(f"Начинаю авторизацию под аккаунт {login}...")

    user = wa.WebAuth(login)

    # Or the login steps be implemented for other situation like so
    try:
        session = user.login(password=password, twofactor_code=guard)
    except (wa.CaptchaRequired, wa.LoginIncorrect) as exp:
        if isinstance(exp, wa.LoginIncorrect):
            return init_classes.bot_tg.send_message(f"Логин в конфиге указан неверно.")
        else:
            pass_user = password

        if isinstance(exp, wa.CaptchaRequired):
            init_classes.bot_tg.send_message(f"Пройдите капчу - {user.captcha_url}")
        else:
            captcha = None

        session = user.login(password=pass_user, captcha=captcha)
    except wa.EmailCodeRequired:
        session = user.login(email_code='ZXC123')
    except wa.TwoFactorCodeRequired:
        return init_classes.bot_tg.send_message(f"Steam Guard неверен, введите новый код.")

    init_classes.bot_tg.send_message(f"Авторизация прошла успешна.\nПриступаю к вытаскиванию jwt токена и cookie для игр.")

    session.get('https://steamcommunity.com/openid/login?openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.realm=https%3A%2F%2Fcsgrauth.ru&openid.return_to=https%3A%2F%2Fcsgrauth.ru%2Fauth%2Fcsgo3.run%2F')

    from seleniumwire import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    CHROME_PATH = app_path + f'/bot-auth/browsers/windows/chrome/chrome.exe'
    CHROMEDRIVER_PATH = app_path + f'/bot-auth/browsers/windows/chrome/chromedriver.exe'
    WINDOW_SIZE = "1920,1080"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
    chrome_options.add_argument("--log-level=3")
    chrome_options.binary_location = CHROME_PATH

    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
    cookie_auth = user.session.cookies.get_dict()

    driver.get('https://steamcommunity.com/openid/login?openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.realm=https%3A%2F%2Fcsgrauth.ru&openid.return_to=https%3A%2F%2Fcsgrauth.ru%2Fauth%2Fcsgo3.run%2F')

    for cookie in cookie_auth:
        driver.add_cookie({'name': cookie, 'value': cookie_auth[cookie], 'path': '/', 'domain': 'steamcommunity.com'})
    driver.get('https://steamcommunity.com/openid/login?openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.realm=https%3A%2F%2Fcsgrauth.ru&openid.return_to=https%3A%2F%2Fcsgrauth.ru%2Fauth%2Fcsgo3.run%2F')
    driver.find_element(By.CSS_SELECTOR, '.btn_green_white_innerfade').click()

    request = driver.wait_for_request('/ping',300)
    token = request.headers['authorization'][4::]
    cookie = request.headers['cookie']

    with open(app_path + '/storage/temp/global/auth_info.json','r+') as auth_info:
        auth_info = json.load(auth_info)
        auth_info['token'] = token
        auth_info['cookie'] = cookie
        with open(app_path + '/storage/temp/global/auth_info.json', 'w', encoding='utf-8') as auth_info_write:
            json.dump(auth_info, auth_info_write, ensure_ascii=False, indent=4)

    info_user_tg.storage['active_page'] = {}
    init_classes.bot_tg.send_message(f"Бот успешно достал необходимую информацию, продолжаю запуск скрипта.")
    driver.quit()
    return True
