from common.base import TestBaseClass

class TestTwo(TestBaseClass):
    
    def test_case2(self):
        self.log.info("Running test 2")
        # Open the URL in the browser
        self.driver.get("http://www.yahoo.com")

        # Get the title of the Page
        print("Title of the webpage is {}".format(self.driver.title))

    def test_case3(self):
        self.log.info("Running test 3")
        # Open the URL in the browser
        self.driver.get("http://www.reddit.com")

        # Get the title of the Page
        print("Title of the webpage is {}".format(self.driver.title))
        assert False