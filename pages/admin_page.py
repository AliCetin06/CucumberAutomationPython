from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class AdminPage(BasePage):
    # Locator'lar (Java @FindBy karşiliği Tuple yapilari)
    TITLE_OF_PAGE = (By.XPATH, "//span[@class='oxd-topbar-header-breadcrumb']")
    JOB_OPTION = (By.XPATH, "(//span[@class='oxd-topbar-body-nav-tab-item'])[2]")
    LIST_OF_JOB = (By.XPATH, "//ul[@class='oxd-dropdown-menu']/li")

    def __init__(self, driver):
        super().__init__(driver)

    def verify_title_of_page(self):
        element = self.find(self.TITLE_OF_PAGE)
        assert element.is_displayed(), "Title is not display in Admin Page"

    def clicking_to_job_option(self):
        self.wait_for_element_to_be_clickable(self.JOB_OPTION)
        self.click(self.JOB_OPTION)

    def verifying_all_options(self):
        self.wait_for_element_to_be_visible(self.JOB_OPTION)
        job_elements = self.find_elements(self.LIST_OF_JOB)
        for item in job_elements:
            print(item.text)

    # Behave / Cucumber DataTable doğrulamasi için metot
    def verify_job_sub_menu_items(self, expected_items):
        actual_elements = self.find_elements(self.LIST_OF_JOB)

        for i, element in enumerate(actual_elements):
            actual_data = element.text.strip()
            expected_data = expected_items[i]

            assert actual_data == expected_data, f"Expected: {expected_data} Actual: {actual_data}"