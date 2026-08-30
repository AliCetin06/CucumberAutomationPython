import os
from typing import Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from utils.property_reader import PropertyReader


class DriverUtils:
    _driver: Optional[webdriver.Remote] = None

    @classmethod
    def _is_ci_or_linux(cls) -> bool:
        # Sadece GERÇEK CI/headless sinyallerine bakiyoruz.
        # 'os.name != "nt"' kontrolünü kasitli olarak KALDIRDIK, çünkü bu
        # macOS'u da (os.name == 'posix', Linux ile ayni) yanlişlikla
        # "CI/sunucu" sanip yerel Mac'te bile tarayiciyi görünmez (headless)
        # açiyordu. Artik yerelde (Mac/Windows/Linux fark etmeksizin)
        # tarayici her zaman görünür açilir; sadece CI ortaminda ya da
        # HEADLESS=true elle ayarlandiğinda headless moda geçilir.
        return (
            os.environ.get("CI") == "true"
            or os.environ.get("GITHUB_ACTIONS") == "true"
            or os.environ.get("HEADLESS", "false").lower() == "true"
        )

    @classmethod
    def _resolve_browser(cls) -> str:
        """
        Hangi tarayicinin başlatilacağini belirler.
        Öncelik sirasi:
          1) BROWSER ortam değişkeni (CI'da matrix strategy bunu set eder)
          2) config.properties içindeki 'browser' key'i
          3) varsayilan: chrome
        """
        browser = os.environ.get("BROWSER")
        if not browser:
            browser = PropertyReader.get_property("browser")
        if not browser:
            browser = "chrome"
        return browser.strip().lower()

    @classmethod
    def _build_chrome_driver(cls, headless: bool) -> webdriver.Chrome:
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--remote-debugging-pipe")
            options.add_argument("--disable-software-rasterizer")
            options.add_argument("--disable-extensions")

        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    @classmethod
    def _build_firefox_driver(cls, headless: bool) -> webdriver.Firefox:
        options = FirefoxOptions()
        if headless:
            options.add_argument("-headless")
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")

        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)

    @classmethod
    def _build_edge_driver(cls, headless: bool) -> webdriver.Edge:
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")

        service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=options)

    @classmethod
    def create_driver(cls) -> None:
        """
        Seçilen tarayiciya göre WebDriver oturumunu Selenium 4 standartlarina
        göre başlatir. CI/CD (GitHub Actions), AWS EC2 (Linux) veya
        HEADLESS=true durumlarinda otomatik olarak headless modda çalişir.
        """
        browser = cls._resolve_browser()
        headless = cls._is_ci_or_linux()

        builders = {
            "chrome": cls._build_chrome_driver,
            "firefox": cls._build_firefox_driver,
            "edge": cls._build_edge_driver,
        }

        builder = builders.get(browser)
        if builder is None:
            raise ValueError(
                f"Desteklenmeyen tarayici: '{browser}'. "
                f"Geçerli seçenekler: {', '.join(builders.keys())}"
            )

        cls._driver = builder(headless)
        cls._driver.implicitly_wait(60)

        if not headless:
            cls._driver.maximize_window()

    @classmethod
    def get_driver(cls) -> Optional[webdriver.Remote]:
        """Mevcut WebDriver oturumunu döndürür."""
        return cls._driver

    @classmethod
    def quit_driver(cls) -> None:
        """WebDriver oturumunu kapatir ve nesneyi sifirlar."""
        if cls._driver is not None:
            try:
                cls._driver.quit()
            finally:
                cls._driver = None