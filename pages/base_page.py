from abc import ABC, abstractmethod
from selenium.webdriver.common.action_chains import ActionChains
from utils.common_methods import CommonMethods


class BasePage(ABC):

    def __init__(self, driver):
        self.driver = driver
        # CommonMethods sınıfından bir nesne türetilir
        self.commonmethods = CommonMethods(driver)
        # Java'daki Actions nesnesinin Python karşılığı
        self.action = ActionChains(driver)

    @abstractmethod
    def verify_title_of_page(self):
        """Alt sınıfların (child class) ezmek (override) zorunda olduğu soyut metot."""
        pass

    # Locator ile element bulmayı kolaylaştıran yardımcı metotlar
    def find(self, locator):
        return self.driver.find_element(*locator)

    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    def click(self, locator):
        self.find(locator).click()

    def wait_for_element_to_be_clickable(self, locator):
        # return eklendi
        return self.commonmethods.wait_for_element_to_be_clickable(locator)

    def wait_for_element_to_be_visible(self, locator):
        # return eklendi (En kritik düzeltme)
        return self.commonmethods.wait_for_element_to_be_visible(locator)