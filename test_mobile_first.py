import time
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy


def test_settings_app_launch():
    # Options Ayarları
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = "emulator-5554"

    # Android Dahili Ayarlar Uygulaması
    options.app_package = "com.android.settings"
    options.app_activity = ".Settings"
    options.no_reset = True

    # Appium Server Bağlantısı
    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

    try:
        time.sleep(3)

        # Ayarlar sayfasındaki arama çubuğunun veya başlığının varlığını doğrulama
        search_box = driver.find_element(
            by=AppiumBy.ID, value="com.android.settings:id/search_action_bar"
        )
        assert search_box.is_displayed(), "Arama çubuğu ekranda görünmüyor!"
        print("\nAyarlar uygulaması başarıyla açıldı ve arama kutusu doğrulandı! ✅\n")

    finally:
        driver.quit()