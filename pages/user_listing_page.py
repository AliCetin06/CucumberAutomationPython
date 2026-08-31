from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class UserListingPage(BasePage):

    # Locator'lar (Java @FindBy karşılıkları)
    CHOOSING_ADMIN = (By.XPATH, "(//div[@role='row'][(.//div[@role='cell'])[2]//div[text()='Admin']]//i[contains(@class,'bi-pencil')]")
    VERIFYING_TITLE = (By.XPATH, "//div[@class='oxd-topbar-header-title']")

    def __init__(self, driver):
        super().__init__(driver)

    def click_on_edition_btn(self):
        self.click(self.CHOOSING_ADMIN)

    def validate_add_user_sucess_msg(self):
        pass

    def verify_title_of_page(self):
        title_el = self.find(self.VERIFYING_TITLE)
        assert title_el.is_displayed(), "Title is not in UserListingPage"