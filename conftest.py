from fixture.application import Application
import pytest
import json
import os.path

fixture = None
target = None

def load_config(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as f:
            target = json.load(f)
    return target

@pytest.fixture
def app(request):
    global fixture
    global target
    browser = request.config.getoption("--browser")
    web_config = load_config(request.config.getoption("--target"))["web"]
    web_config_admin = load_config(request.config.getoption("--target"))["web_admin"]
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser, web_config["baseUrl"])
    fixture.session.ensure_login(web_config_admin["username"], web_config_admin["password"])
    return fixture

@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture

def pytest_addoption(parser):
    parser.addoption("--browser", action = "store", default = "firefox")
    parser.addoption("--target", action = "store", default = "target.json")
