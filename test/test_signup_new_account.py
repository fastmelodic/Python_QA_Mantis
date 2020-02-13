import string
import random

#Генератор случайной строки для тестовых данных
def random_string(prefix, maxlen):
    symbols = string.ascii_letters
    return prefix + "".join(random.choice(symbols) for x in range(random.randrange(maxlen)))

def test_signup_new_account(app): #перед тестом фикстурой configure_server (фикстура pytest в conftest.py) подкладываем
    #приложению по FTP свой конфиг файл для обхода капчи
    username = random_string("user_", 10)
    email = username + "@localhost"
    password = "test"
    #по средстваом протокола Telnet создаем почту на локально развернутом сервере James(если существует то не создаем)
    app.james.ensure_user_exists(username, password)
    #регистрируем нового пользователя по созданной почте, стягиваем письмо (протокол POP3), из письма стягиваем линк
    #для потверждения регистрации, переходим по нему и логинимся
    app.signup.new_user(username, email, password)
    #по протоколу SOAP тестим запросом возможность логина
    assert app.soap.can_login(username, password)
    #негативный тест на регистрацию уже зарегестрированного пользователя
    assert app.signup.check_if_already_registered(username, email)