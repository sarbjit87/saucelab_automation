from common.base_testcase import TestBaseClass
from pageObjects.LoginPage import LoginPage

class TestLogin(TestBaseClass):

    def test_logininvalidpassword(self):
        self.log.info("Running test for standard user and invalid password")
        self.loginPage = LoginPage(self.driver)
        self.loginPage.do_login("standard_user", "InvalidPassword")
        assert self.loginPage.get_error_message() == "Epic sadface: Username and password do " \
                                                     "not match any user in this service"
    def test_loginlockeduser(self):
        self.log.info("Running test for locked user and valid password")
        self.loginPage = LoginPage(self.driver)
        self.loginPage.do_login("locked_out_user", "secret_sauce")
        assert self.loginPage.get_error_message() == "Epic sadface: Sorry, this user has been locked out."

    def test_loginwithnousername(self):
        self.log.info("Running test for empty user and valid password")
        self.loginPage = LoginPage(self.driver)
        self.loginPage.do_login("", "secret_sauce")
        assert self.loginPage.get_error_message() == "Epic sadface: Username is required"

    def test_loginwithnopassword(self):
        self.log.info("Running test for standard user and empty password")
        self.loginPage = LoginPage(self.driver)
        self.loginPage.do_login("standard_user", "")
        assert self.loginPage.get_error_message() == "Epic sadface: Password is required"