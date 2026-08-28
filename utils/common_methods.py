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
        Elementin görünmez hale gelmesini (kaybolmasını) bekler.
        Genelde loading/spinner elementleri için kullanılır.
        """
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.invisibility_of_element_located(locator_or_element))
    def wait_for_element_to_be_visible(self, locator_or_element: Union[Tuple[str, str], WebElement], timeout: int = 60):
        """
        Elementin görünür olmasını bekler.
        Eğer locator (tuple) verilirse visibility_of_element_located kullanır,
        böylece 'tuple object has no attribute is_displayed' hatası alınmaz.
        """
        wait = WebDriverWait(self.driver, timeout)

        # Eğer gönderilen parametre Tuple (örn: (By.NAME, 'username')) ise:
        if isinstance(locator_or_element, tuple):
            return wait.until(EC.visibility_of_element_located(locator_or_element))

        # Eğer doğrudan WebElement gönderildiyse:
        return wait.until(EC.visibility_of(locator_or_element))

    def wait_for_element_to_be_clickable(self, locator_or_element: Union[Tuple[str, str], WebElement],
                                         timeout: int = 60):
        """
        Elementin tıklanabilir olmasını bekler.
        Hem Tuple (locator) hem de WebElement kabul eder.
        """
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator_or_element))

    def switch_to_new_window(self, current_window: str):
        """Mevcut pencereden farklı olan ilk yeni sekmeye/pencereye geçiş yapar."""
        window_list = self.driver.window_handles

        for window in window_list:
            if window != current_window:
                self.driver.switch_to.window(window)
                break