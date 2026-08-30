from appium import webdriver
from appium.options.android import UiAutomator2Options


class MobileDriver:
    @staticmethod
    def get_driver():
        # Appium / Android konfigürasyon nesnesini oluşturur
        options = UiAutomator2Options()

        # Test edilecek platform ve otomasyon motoru ayarlari
        options.platform_name = "Android"
        options.automation_name = "UiAutomator2"
        options.device_name = "emulator-5554"  # ADB'de görünen emülatör adi

        # Test edilecek uygulamanin paket ve aktivite isimleri (Settings uygulamasi)
        options.app_package = "com.android.settings"
        options.app_activity = ".Settings"

        # Uygulamayi her test öncesi sifirlamadan/silmeden mevcut haliyle açar
        options.no_reset = True

        # Appium sunucusuna (localhost:4723) istek atarak oturumu (session) başlatir
        driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

        # Elementlerin yüklenmesi için 10 saniyeye kadar dinamik bekleme süresi tanir
        driver.implicitly_wait(10)
        return driver