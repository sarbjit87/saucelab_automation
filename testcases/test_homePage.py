from common.base import TestBaseClass

class TestOne(TestBaseClass):
    
    def test_case1(self):
        self.log.info("Running test 1")
        # Open the URL in the browser
        self.driver.get("http://www.google.com")

        # Get the title of the Page
        print("Title of the webpage is {}".format(self.driver.title))
        #assert False

