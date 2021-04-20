import pytest

class TestBaseClass:

    @pytest.fixture(autouse=True)
    def setupTestBrowser(self, driver_get):
        self.driver = driver_get

    @pytest.fixture(autouse=True)
    def setupTestLog(self, get_logger_instance):
        self.log = get_logger_instance
