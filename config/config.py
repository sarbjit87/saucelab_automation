import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    BASE_URL = "https://www.saucedemo.com/"
    BASE_DIR = os.path.abspath(os.path.join(basedir, os.pardir))
    SCREENSHOT_PATH = os.path.join(BASE_DIR, "screenshots")
    LOGS_PATH = os.path.join(BASE_DIR, "logs")
    REPORTS_PATH = os.path.join(BASE_DIR, "reports")