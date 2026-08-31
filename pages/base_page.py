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
        # Artık anlık find_element yerine, elementin görünür (visible) olmasını bekliyor.
        # Chrome'da DOM'un geç render olduğu durumlarda NoSuchElementException'ı önler.
        return self.wait_for_element_to_be_visible(locator)

    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    def click(self, locator):
        # find() + click() yerine, elementin tıklanabilir (clickable) olmasını bekleyip tıklıyor.
        # Bu, hem "element bulunamadı" hem de "element var ama henüz tıklanamaz" durumlarını kapsar.
        element = self.wait_for_element_to_be_clickable(locator)
        element.click()

    def wait_for_element_to_be_clickable(self, locator):
        # return eklendi
        return self.commonmethods.wait_for_element_to_be_clickable(locator)

    def wait_for_element_to_be_visible(self, locator):
        # return eklendi (En kritik düzeltme)
        return self.commonmethods.wait_for_element_to_be_visible(locator)

    def wait_for_element_to_be_invisible(self, locator):
        # Loading/spinner gibi elementlerin kaybolmasını beklemek için
        return self.commonmethods.wait_for_element_to_be_invisible(locator)