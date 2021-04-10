import pytest
from selenium import webdriver
import os
from config.config import Config
from datetime import datetime
import logging


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """ Create a log file if log_file is not mentioned in *.ini file"""
    timestamp = datetime.strftime(datetime.now(), '%Y-%m-%d_%H-%M-%S')

    if not config.option.log_file:
        log_file_name = "log_" + timestamp + ".log"       
        config.option.log_file = os.path.join(Config.LOGS_PATH, log_file_name)
    
    if not config.option.htmlpath:
        report_file_name = "report_" + timestamp + ".html" 
        config.option.htmlpath = os.path.join(Config.REPORTS_PATH, report_file_name)


def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome"
    )

    parser.addoption(
        "--headless_browser", action="store_true"
        )


def pytest_generate_tests(metafunc):
    browser_arg=metafunc.config.getoption("browser_name")
   
    if 'browser_name' in metafunc.fixturenames and browser_arg is not None:
        if browser_arg == "all":
            metafunc.parametrize("browser_name", ["firefox", "chrome"], scope="session")
        else:
            metafunc.parametrize("browser_name", [browser_arg], scope="session")


@pytest.fixture(scope="session")
def driver_get(request, browser_name):
    global driver

    if browser_name == "chrome":
        print("Launching Chrome Browser...")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-notifications")
        
        if request.config.getoption("headless_browser"):
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu') 
       
        driver = webdriver.Chrome(executable_path=os.path.join(os.environ.get('BROWSER_DRIVERS'),"chromedriver"), 
                                  options=chrome_options)
    elif browser_name == "firefox":
        print("Launching Firefox Browser...")
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference("dom.webnotifications.enabled", False)
        firefox_profile.set_preference("dom.push.enabled", False)
        firefox_options = webdriver.FirefoxOptions()
       
        if request.config.getoption("headless_browser"):
            firefox_options.add_argument('--headless')
        
        driver = webdriver.Firefox(executable_path=os.path.join(os.environ.get('BROWSER_DRIVERS'),"geckodriver"),
                                   options=firefox_options,
                                   firefox_profile=firefox_profile)
    
    yield driver
    print("Closing Browser")
    driver.quit()

@pytest.fixture(scope="session")
def get_logger_instance(request):
    logger = logging.getLogger(__name__)
    yield logger

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
        Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
        :param item:
        """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            timestamp = datetime.strftime(datetime.now(), '%Y-%m-%d_%H-%M-%S')
            file_name_1 = report.nodeid.replace("::", "_") + timestamp + ".png"
            file_name = os.path.basename(file_name_1)
            file_name = os.path.join(Config.SCREENSHOT_PATH, file_name)
            _capture_screenshot(file_name)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


def _capture_screenshot(name):
        driver.get_screenshot_as_file(name)

"""
Alternate fixtures for setup :-

Class Scope : Set the class property with the driver

@pytest.fixture(scope="class")
def browser_setup(request, browser_name):
    #browser_name=request.config.getoption("browser_name")
    if browser_name == "chrome":
        driver = webdriver.Chrome(executable_path=os.path.join(os.environ.get('BROWSER_DRIVERS'),"chromedriver"))
    elif browser_name == "firefox":
        driver = webdriver.Firefox(executable_path=os.path.join(os.environ.get('BROWSER_DRIVERS'),"geckodriver"))

    request.cls.driver = driver
    yield
    print("Closing Browser")
    driver.quit() 


For Session Scope, following approach can be used to set the driver as class property

@pytest.fixture(scope="session")
def browser_setup(request, browser_name):
    if browser_name == "chrome":
        driver = webdriver.Chrome(executable_path=os.path.join(os.environ.get('BROWSER_DRIVERS'),"chromedriver"))
    elif browser_name == "firefox":
        driver = webdriver.Firefox(executable_path=os.path.join(os.environ.get('BROWSER_DRIVERS'),"geckodriver"))

    session = request.node  
    for item in session.items:
        cls = item.getparent(pytest.Class) 
        setattr(cls.obj, "driver", driver)
    yield
    print("Closing Browser")
    driver.quit()

"""