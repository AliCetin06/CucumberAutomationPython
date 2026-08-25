import os
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


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

        # CI ortamı, Linux işletim sistemi (EC2) veya HEADLESS=true kontrolü
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
            # Linux headless modda stabiliteyi artıran ek bayraklar
            options.add_argument("--remote-debugging-pipe")
            options.add_argument("--disable-software-rasterizer")
            options.add_argument("--disable-extensions")

        # ChromeDriverManager ile uyumlu ChromeDriver otomatik indirilir/yönetilir
        service = Service(ChromeDriverManager().install())
        cls._driver = webdriver.Chrome(service=service, options=options)
        cls._driver.implicitly_wait(60)

        # Yerel Windows ortamında pencereyi büyüt
        if not is_ci_or_linux:
            cls._driver.maximize_window()

    @classmethod
    def get_driver(cls) -> Optional[webdriver.Chrome]:
        """Mevcut WebDriver oturumunu döndürür."""
        return cls._driver

    @classmethod
    def quit_driver(cls) -> None:
        """WebDriver oturumunu kapatır ve nesneyi sıfırlar."""
        if cls._driver is not None:
            try:
                cls._driver.quit()
            finally:
                cls._driver = None