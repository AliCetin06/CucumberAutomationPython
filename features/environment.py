from utils.driver_utils import DriverUtils
from utils.property_reader import PropertyReader

#ava Cucumber Hooks sınıfının Python Behave karşılığı aşağıdadır.
def before_scenario(context, scenario):
    """
    Java'daki @Before karşılığı:
    Her senaryo başlamadan önce çalışır.
    """
    # Property / Config verilerini yükle
    PropertyReader.init_property()

    # WebDriver oturumunu başlat
    DriverUtils.create_driver()


def before_tag(context, tag):
    """
    Java'daki Conditional Hook (@Before("@ie")) karşılığı:
    Belirtilen tag çalıştırılmadan önce devreye girer.
    """
    if tag == "ie":
        # IE veya özel tag hazırlık verilerini buraya ekleyebilirsiniz
        pass


def after_scenario(context, scenario):
    """
    Java'daki @After karşılığı:
    Her senaryo bittiğinde çalışır ve tarayıcıyı kapatır.
    """
    driver = DriverUtils.get_driver()
    if driver:
        driver.quit()