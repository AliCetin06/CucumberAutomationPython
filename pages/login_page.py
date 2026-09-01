from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.property_reader import PropertyReader


class LoginPage(BasePage):
    # Locator'lar (XPath sonlarindaki gereksiz boşluklar temizlendi)
    FORGOT_PASSWORD = (By.XPATH, "//p[contains(., 'Forgot your password?')]")
    USER_NAME_INPUT = (By.NAME, "username")
    USER_PASSWORD = (By.NAME, "password")
    CLICKING_SUBMIT = (By.XPATH, "//button[@type='submit']")
    REQUIRED_ELEMENTS = (By.XPATH, "//span[text()='Required']")
    ERROR_MESSAGE = (By.XPATH, "//p[text()='Invalid credentials']")

    def __init__(self, driver):
        super().__init__(driver)

    def open_website(self):
        # Config / PropertyReader üzerinden URL alma
        url = PropertyReader.get_property("app.url")
        self.driver.get(url)

    def do_login(self, username, password):
        # Eğer parametre olarak "login.username" string'i gelirse config'den oku
        if username == "login.username":
            username = PropertyReader.get_property("login.username")
        if password == "login.password":
            password = PropertyReader.get_property("login.password")

        # Elemanlarin görünür olmasini bekle
        user_input_el = self.wait_for_element_to_be_visible(self.USER_NAME_INPUT)
        pass_input_el = self.wait_for_element_to_be_visible(self.USER_PASSWORD)

        # None Kontrolü (NoneType hatasini önler)
        assert user_input_el is not None, "Username input elemani bulunamadi/görünür değil!"
        assert pass_input_el is not None, "Password input elemani bulunamadi/görünür değil!"

        user_input_el.clear()
        user_input_el.send_keys(username if username else "")

        pass_input_el.clear()
        pass_input_el.send_keys(password if password else "")

        self.click(self.CLICKING_SUBMIT)

    def clicking_forget_password(self):
        self.click(self.FORGOT_PASSWORD)

    def validate_login_error_msg_invalid(self):
        err_el = self.wait_for_element_to_be_visible(self.ERROR_MESSAGE)
        assert err_el is not None and err_el.is_displayed(), "Invalid credentials hata mesaji görüntülenemedi"

    def validate_login_error_msg_blank(self):
        elements = self.find_elements(self.REQUIRED_ELEMENTS)
        assert len(elements) >= 1, "'Required' alan uyarilari görüntülenemedi"

    def verify_login_of_page(self):
        user_el = self.wait_for_element_to_be_visible(self.USER_NAME_INPUT)
        pass_el = self.wait_for_element_to_be_visible(self.USER_PASSWORD)

        assert user_el is not None and user_el.is_displayed(), "Username alani görünmüyor"
        assert pass_el is not None and pass_el.is_displayed(), "Password alani görünmüyor"

    def verify_login_of_page(self):
        # Düz find yerine bekleme yapan metodu kullaniyoruz:
        user_el = self.wait_for_element_to_be_visible(self.USER_NAME_INPUT)
        pass_el = self.wait_for_element_to_be_visible(self.USER_PASSWORD)

        assert user_el is not None and user_el.is_displayed(), "Username alani görünmüyor"
        assert pass_el is not None and pass_el.is_displayed(), "Password alani görünmüyor"
    def verify_title_of_page(self):
        return self.driver.title