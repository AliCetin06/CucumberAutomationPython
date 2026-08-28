from appium.webdriver.common.appiumby import AppiumBy

class SettingsPage:
    def __init__(self, driver):
        self.driver = driver
        self.SEARCH_BAR = (AppiumBy.ID, "com.android.settings:id/search_action_bar_title")

    def verify_search_bar_displayed(self):
        element = self.driver.find_element(*self.SEARCH_BAR)
        assert element.is_displayed(), "Arama çubuğu ekranda görüntülenemedi!"