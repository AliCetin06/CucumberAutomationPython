from utils.driver_utils import DriverUtils
from utils.property_reader import PropertyReader


def before_scenario(context, scenario):
    """
    Her senaryo başlamadan önce çalışır.
    """
    # Property / Config verilerini yükle
    PropertyReader.init_property()

    # Senaryo ve Feature tag'lerini topla
    scenario_tags = set(scenario.tags) if hasattr(scenario, "tags") else set()
    feature_tags = set(scenario.feature.tags) if hasattr(scenario.feature, "tags") else set()
    all_tags = scenario_tags.union(feature_tags)

    # API veya DB senaryolarında web driver başlatma
    if "api" in all_tags or "db" in all_tags:
        context.driver = None
        return

    # Sadece UI senaryolarında WebDriver oturumunu başlat
    DriverUtils.create_driver()
    context.driver = DriverUtils.get_driver()


def before_tag(context, tag):
    if tag == "ie":
        pass


def after_scenario(context, scenario):
    """
    Her senaryo bittiğinde çalışır ve tarayıcı açıksa kapatır.
    """
    driver = DriverUtils.get_driver()
    if driver:
        DriverUtils.quit_driver()
        context.driver = None