from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Union, Tuple


class CommonMethods:

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def wait_for_element_to_be_invisible(self, locator_or_element: Union[Tuple[str, str], WebElement],
                                         timeout: int = 60):
        """
        Elementin görünmez hale gelmesini (kaybolmasini) bekler.
        Genelde loading/spinner elementleri için kullanilir.
        """
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.invisibility_of_element_located(locator_or_element))

    def wait_for_element_to_be_visible(self, locator_or_element: Union[Tuple[str, str], WebElement], timeout: int = 60):
        """
        Elementin görünür olmasini bekler.
        Eğer locator (tuple) verilirse visibility_of_element_located kullanir,
        böylece 'tuple object has no attribute is_displayed' hatasi alinmaz.
        """
        wait = WebDriverWait(self.driver, timeout)

        if isinstance(locator_or_element, tuple):
            return wait.until(EC.visibility_of_element_located(locator_or_element))

        return wait.until(EC.visibility_of(locator_or_element))

    def wait_for_element_to_be_clickable(self, locator_or_element: Union[Tuple[str, str], WebElement],
                                         timeout: int = 60):
        """
        Elementin tiklanabilir olmasini bekler.
        Hem Tuple (locator) hem de WebElement kabul eder.
        Tiklanabilir olmadan önce elementi görünür alana kaydirir (Edge/Firefox'ta
        viewport disindaki elementler bazen clickable sayilmiyor).
        """
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(EC.presence_of_element_located(locator_or_element)) \
            if isinstance(locator_or_element, tuple) else locator_or_element

        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

        return wait.until(EC.element_to_be_clickable(locator_or_element))

    def switch_to_new_window(self, current_window: str):
        """Mevcut pencereden farkli olan ilk yeni sekmeye/pencereye geçiş yapar."""
        window_list = self.driver.window_handles

        for window in window_list:
            if window != current_window:
                self.driver.switch_to.window(window)
                break