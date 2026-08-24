from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pages.base_page import BasePage


class DataTableHomePage(BasePage):
    VERIFY_DATA = (By.XPATH, "//table[@id='myTable']")
    TABLE_ROWS = (By.XPATH, "//table[@id='myTable']/tbody/tr")

    def __init__(self, driver):
        super().__init__(driver)

    def verify_title_of_page(self):
        actual_title = self.driver.title
        assert "DataTables" in actual_title, f"Title mismatch! Actual: '{actual_title}'"

    def open_data_table_website(self):
        self.driver.get("https://datatables.net/")

    def verify_of_data_home_page(self):
        element = self.wait_for_element_to_be_visible(self.VERIFY_DATA)
        assert element is not None and element.is_displayed(), "Data table is not displayed"

    def verify_data_table_data(self, list_of_items):
        """Header'sız tablo doğrulaması (Dinamik XPath ile garanti çözüm)."""
        self.wait_for_element_to_be_visible(self.VERIFY_DATA)

        for i, expected_row in enumerate(list_of_items):
            for j, expected_value in enumerate(expected_row):
                # Doğrudan ilgili satır (i+1) ve sütun (j+1) hücresini XPath ile hedefliyoruz
                cell_xpath = (By.XPATH, f"//table[@id='myTable']/tbody/tr[{i + 1}]/td[{j + 1}]")

                # Hücrenin yüklenmesini bekleyip metnini çekiyoruz
                cell_element = self.wait_for_element_to_be_visible(cell_xpath)

                # Hücrenin AJAX verisiyle dolmasını bekle (Loading... olmamalı)
                WebDriverWait(self.driver, 10).until(
                    lambda d: d.find_element(*cell_xpath).get_attribute("innerText").strip() != "Loading..."
                )

                actual_value = cell_element.get_attribute("innerText").strip()

                assert actual_value == expected_value, (
                    f"Row {i + 1} Col {j + 1} mismatch! Expected: '{expected_value}', Actual: '{actual_value}'"
                )

    def verify_data_table_data_with_header(self, list_of_map):
        """Header'lı (Map) tablo doğrulaması."""
        self.wait_for_element_to_be_visible(self.VERIFY_DATA)

        # Tablonun AJAX verisiyle dolmasını bekle
        first_cell_xpath = (By.XPATH, "//table[@id='myTable']/tbody/tr[1]/td[1]")
        WebDriverWait(self.driver, 10).until(
            lambda d: d.find_element(*first_cell_xpath).get_attribute("innerText").strip() != "Loading..."
        )

        rows = self.driver.find_elements(*self.TABLE_ROWS)

        for i, expected_map in enumerate(list_of_map):
            cells = rows[i].find_elements(By.TAG_NAME, "td")
            actual_name = cells[0].get_attribute("innerText").strip()
            expected_name = expected_map.get("Name")

            assert actual_name == expected_name, (
                f"Row {i + 1} Name mismatch! Expected: '{expected_name}', Actual: '{actual_name}'"
            )