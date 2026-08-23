from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from typing import Optional
import os


class DriverUtils:
    _driver: Optional[webdriver.Chrome] = None

    @classmethod
    def create_driver(cls) -> None:
        """
        Chrome WebDriver oturumunu Selenium 4 standartlarına göre otomatik başlatır.
        CI ortamında (GitHub Actions) otomatik olarak headless modda çalışır.
        """
        options = Options()

        is_ci = os.environ.get("CI") == "true" or os.environ.get("GITHUB_ACTIONS") == "true"

        if is_ci:
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--window-size=1920,1080")

        cls._driver = webdriver.Chrome(options=options)
        cls._driver.implicitly_wait(60)

        if not is_ci:
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