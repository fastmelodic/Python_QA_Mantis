from fixture.application import Application
from fixture.db import Dbfixture
import pytest
import json
import os.path
import jsonpickle

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

@pytest.fixture
def db(request):
    db_config = load_config(request.config.getoption("--target"))["db"]
    dbfixture = Dbfixture(host = db_config["host"], name = db_config["name"], user = db_config["user"], password = db_config["password"])
    def fin():
        dbfixture.destroy()
    request.addfinalizer(fin)
    return dbfixture


def pytest_addoption(parser):
    parser.addoption("--browser", action = "store", default = "firefox")
    parser.addoption("--target", action = "store", default = "target.json")

def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("json_"):
            testdata = load_from_json(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids = [str(x) for x in testdata])


def load_from_json(file):
    with open (os.path.join(os.path.dirname(os.path.abspath(__file__)), f"data/{file}.json")) as f:
        return jsonpickle.decode(f.read())
