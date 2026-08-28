from appium import webdriver
from appium.options.android import UiAutomator2Options


class MobileDriver:
    @staticmethod
    def get_driver():
        # Appium / Android konfigürasyon nesnesini oluşturur
        options = UiAutomator2Options()

        # Test edilecek platform ve otomasyon motoru ayarları
        options.platform_name = "Android"
        options.automation_name = "UiAutomator2"
        options.device_name = "emulator-5554"  # ADB'de görünen emülatör adı

        # Test edilecek uygulamanın paket ve aktivite isimleri (Settings uygulaması)
        options.app_package = "com.android.settings"
        options.app_activity = ".Settings"

        # Uygulamayı her test öncesi sıfırlamadan/silmeden mevcut haliyle açar
        options.no_reset = True

        # Appium sunucusuna (localhost:4723) istek atarak oturumu (session) başlatır
        driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

        # Elementlerin yüklenmesi için 10 saniyeye kadar dinamik bekleme süresi tanır
        driver.implicitly_wait(10)
        return driver