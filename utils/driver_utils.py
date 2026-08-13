from selenium import webdriver
from typing import Optional


class DriverUtils:
    _driver: Optional[webdriver.Chrome] = None

    @classmethod
    def create_driver(cls) -> None:
        """
        Chrome WebDriver oturumunu Selenium 4 standartlarına göre otomatik başlatır.
        """
        # Service veya manuel dosya yolu tanımı kaldırıldı.
        # Selenium 4 tarayıcınıza uygun driver'ı otomatik olarak yönetir.
        cls._driver = webdriver.Chrome()
        cls._driver.implicitly_wait(60)
        cls._driver.maximize_window()

    @classmethod
    def get_driver(cls) -> webdriver.Chrome:
        """Mevcut WebDriver oturumunu döndürür."""
        if cls._driver is None:
            raise RuntimeError("Driver henüz başlatılmadı! Lütfen önce create_driver() metodunu çağırın.")
        return cls._driver

    @classmethod
    def quit_driver(cls) -> None:
        """WebDriver oturumunu kapatır."""
        if cls._driver is not None:
            cls._driver.quit()
            cls._driver = None