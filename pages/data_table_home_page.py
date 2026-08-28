from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class DataTableHomePage(BasePage):
    TABLE = (By.CSS_SELECTOR, "table#example, table.dataTable")
    TABLE_ROWS = (By.CSS_SELECTOR, "table#example tbody tr, table.dataTable tbody tr")

    def __init__(self, driver):
        super().__init__(driver)

    def verify_title_of_page(self):
        """BasePage içindeki abstract metodu implement ediyoruz."""
        actual_title = self.driver.title
        assert "DataTables" in actual_title, f"Title mismatch! Actual: '{actual_title}'"

    def open_data_table_website(self):
        self.driver.get("https://datatables.net/")

    def verify_of_data_home_page(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.TABLE)
        )
        assert element is not None and element.is_displayed(), "Data table is not displayed"

    def verify_data_table_data(self, list_of_items):
        """Tüm satırları sırasıyla hücre hücre doğrular."""
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(self.TABLE_ROWS)
        )

        # DataTables JS'in ilk hücreyi doldurmasını bekle (race condition fix).
        # TABLE_ROWS ile aynı (fallback'li) locator'ı kullanıyoruz ki
        # id/class farkından kaynaklanan "element bulunamadı" riskini ortadan kaldıralım.
        def first_cell_filled(driver):
            rows = driver.find_elements(*self.TABLE_ROWS)
            if not rows:
                return False
            first_cells = rows[0].find_elements(By.TAG_NAME, "td")
            return bool(first_cells) and first_cells[0].text.strip() != ""

        WebDriverWait(self.driver, 20).until(first_cell_filled)

        rows = self.driver.find_elements(*self.TABLE_ROWS)
        assert len(rows) >= len(list_of_items), (
            f"Expected at least {len(list_of_items)} rows, but found {len(rows)}"
        )

        for i, expected_row in enumerate(list_of_items):
            cells = rows[i].find_elements(By.TAG_NAME, "td")
            for j, expected_value in enumerate(expected_row):
                actual_value = cells[j].text.strip() or cells[j].get_attribute("innerText").strip()
                assert actual_value == expected_value, (
                    f"Row {i + 1} Col {j + 1} mismatch! Expected: '{expected_value}', Actual: '{actual_value}'"
                )