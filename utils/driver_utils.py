import os
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class DriverUtils:
    _driver: Optional[webdriver.Chrome] = None

    @classmethod
    def create_driver(cls) -> None:
        """
        Chrome WebDriver oturumunu Selenium 4 standartlarına göre başlatır.
        CI/CD (GitHub Actions), AWS EC2 (Linux) veya HEADLESS=true durumlarında
        otomatik olarak headless modda çalışır.
        """
        options = Options()

        # CI ortamı (GitHub Actions vb.), Linux işletim sistemi (EC2) veya HEADLESS=true kontrolü
        is_ci_or_linux = (
            os.environ.get("CI") == "true"
            or os.environ.get("GITHUB_ACTIONS") == "true"
            or os.environ.get("HEADLESS", "false").lower() == "true"
            or os.name != "nt"  # Windows dışındaki sistemler (Linux/Ubuntu EC2)
        )

        if is_ci_or_linux:
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")

        cls._driver = webdriver.Chrome(options=options)
        cls._driver.implicitly_wait(60)

        # Yerel Windows ortamında pencereyi büyüt
        if not is_ci_or_linux:
            cls._driver.maximize_window()

    @classmethod
    def get_driver(cls) -> webdriver.Chrome:
        """Mevcut WebDriver oturumunu döndürür."""
        if cls._driver is None:
            raise RuntimeError("Driver henüz başlatılmadı! Lütfen önce create_driver() metodunu çağırın.")
        return cls._driver

    @classmethod
    def quit_driver(cls) -> None:
        """WebDriver oturumunu kapatır ve nesneyi sıfırlar."""
        if cls._driver is not None:
            cls._driver.quit()
            cls._driver = None