from abc import ABC, abstractmethod
from selenium.webdriver.common.action_chains import ActionChains
from utils.common_methods import CommonMethods


class BasePage(ABC):

    def __init__(self, driver):
        self.driver = driver
        # CommonMethods sinifindan bir nesne türetilir
        self.commonmethods = CommonMethods(driver)
        # Java'daki Actions nesnesinin Python karşiliği
        self.action = ActionChains(driver)

    @abstractmethod
    def verify_title_of_page(self):
        """Alt siniflarin (child class) ezmek (override) zorunda olduğu soyut metot."""
        pass

    # Locator ile element bulmayi kolaylaştiran yardimci metotlar
    def find(self, locator):
        # Artik anlik find_element yerine, elementin görünür (visible) olmasini bekliyor.
        # Chrome'da DOM'un geç render olduğu durumlarda NoSuchElementException'i önler.
        return self.wait_for_element_to_be_visible(locator)

    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    def click(self, locator):
        # find() + click() yerine, elementin tiklanabilir (clickable) olmasini bekleyip tikliyor.
        # Bu, hem "element bulunamadi" hem de "element var ama henüz tiklanamaz" durumlarini kapsar.
        element = self.wait_for_element_to_be_clickable(locator)
        element.click()

    def wait_for_element_to_be_clickable(self, locator):
        # return eklendi
        return self.commonmethods.wait_for_element_to_be_clickable(locator)

    def wait_for_element_to_be_visible(self, locator):
        # return eklendi (En kritik düzeltme)
        return self.commonmethods.wait_for_element_to_be_visible(locator)

    def wait_for_element_to_be_invisible(self, locator):
        # Loading/spinner gibi elementlerin kaybolmasini beklemek için
        return self.commonmethods.wait_for_element_to_be_invisible(locator)