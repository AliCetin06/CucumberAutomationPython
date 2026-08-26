
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class AddUserPage(BasePage):

    # Locator'lar (Java @FindBy karşılığı Tuple yapısı)
    CHANGE_NAME_INPUT = (By.XPATH, "//input[@placeholder='Type for hints...']")
    SAVE_BTN = (By.XPATH, "//button[@type='submit']")
    TITLE_OF_PAGE = (By.XPATH, "//div[@class='oxd-topbar-header']")

    def __init__(self, driver):
        super().__init__(driver)

    def click_on_save_btn(self):
        # Önce loading ekranının kaybolmasını bekle
        self.wait_for_element_to_be_invisible((By.CLASS_NAME, "oxd-form-loader"))
        # Sonra normal akış
        self.wait_for_element_to_be_clickable(self.SAVE_BTN)
        self.click(self.SAVE_BTN)

    def fill_required_user_details(self, name="Radha  Borra"):
        self.wait_for_element_to_be_clickable(self.CHANGE_NAME_INPUT)
        element = self.find(self.CHANGE_NAME_INPUT)
        element.clear()
        element.send_keys(name)

    def verify_title_of_page(self):
        self.wait_for_element_to_be_visible(self.TITLE_OF_PAGE)
        element = self.find(self.TITLE_OF_PAGE)
        # Java Assert.assertTrue karşılığı
        assert element.is_displayed(), "Page's title is not displayed"