from src.generator.PageFactory import callable_find_by as find_by
from selenium.webdriver.common.keys import Keys


class GoogleSearchPage:

    _field_search = find_by(name="q", cacheable=True)
    _button_search = find_by(name="btnK", cacheable=True)

    def __init__(self, driver):
        self._driver = driver
        self._driver.get("https://www.google.com/")

    def search_positive(self, searchText):
        self._field_search().send_keys(searchText)
        self._field_search().send_keys(Keys.RETURN)
        assert "search" in self._driver.current_url

    def search_negative(self, searchText):
        self._field_search().send_keys(searchText)
        self._field_search().send_keys(Keys.RETURN)
        assert "search" not in self._driver.current_url
