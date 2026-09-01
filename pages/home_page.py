from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HomePage(BasePage):

    # Locator'lar (Java @FindBy ve By karşiliklari)
    ADMIN_BTN = (By.XPATH, "//span[text()='Admin']")
    RECRUITMENT_BTN = (By.XPATH, "//span[text()='Recruitment']")
    BRAND_LOGO = (By.CSS_SELECTOR, ".oxd-brand-banner img")

    def __init__(self, driver):
        super().__init__(driver)

    def validate_home_page(self):
        # Logo görünürlük kontrolü
        logo_element = self.find(self.BRAND_LOGO)
        print(logo_element.is_displayed())

    def verify_title_of_page(self):
        pass

    def clicking_admin_btn(self):
        self.click(self.ADMIN_BTN)

    def clicking_recruitment(self):
        self.click(self.RECRUITMENT_BTN)