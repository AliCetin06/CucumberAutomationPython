from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ForgetPasswordPage(BasePage):

    # Locator'lar (Java @FindBy karşiliği Tuple tanimlamalari)
    USER_NAME = (By.XPATH, "//input[@name='username']")
    RESET_BUTTON = (By.XPATH, "//button[@type='submit']")
    VALIDATION = (By.XPATH, "//div[@class='orangehrm-card-container']")

    def __init__(self, driver):
        super().__init__(driver)

    def enter_user_name(self, username):
        element = self.find(self.USER_NAME)
        element.send_keys(username)

    def click_reset_btn(self):
        self.wait_for_element_to_be_clickable(self.RESET_BUTTON)
        self.click(self.RESET_BUTTON)

    def validation_reset_password(self):
        element = self.find(self.VALIDATION)
        print(element.is_displayed())
        print(element.text)

    def verify_title_of_page(self):
        pass

    def verify_incorrect_username_msg(self):
        pass

    def verify_forget_password_page(self):
        username_el = self.find(self.USER_NAME)
        reset_btn_el = self.find(self.RESET_BUTTON)

        assert username_el.is_displayed(), "Forget password page is not displayed"
        assert reset_btn_el.is_displayed(), "Forget password page is not displayed"