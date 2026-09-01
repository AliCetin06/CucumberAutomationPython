from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CandidatesPage(BasePage):
    # Locator'lar (Java @FindBy ve By.xpath karşiliği Tuple tanimlamalari)
    TITLE_OF_PAGE = (By.XPATH, "//a[text()='Candidates']")
    JOB_TITLE = (By.XPATH, "//div[text()='Account Assistant']")
    VACANCY = (By.XPATH, "//a[text()='Associate IT Manager']")
    HIRING_MANAGER = (By.XPATH, "//a[text()='Odis Adalwin']")
    STATUS = (By.XPATH, "//a[text()='Application Initiated']")
    CANDIDATE_NAME = (By.XPATH, "//div[@class='oxd-autocomplete-wrapper']/div")
    DATE_OF_APPLICATION_FROM = (By.XPATH, "(//div[@class='oxd-date-wrapper']/div)[1]")
    DATE_OF_APPLICATION_TO = (By.XPATH, "(//div[@class='oxd-date-wrapper']/div)[2]")
    SEARCH_BTN = (By.XPATH, "//button[@type='submit']")
    NO_RECORD_MSG = (By.XPATH, "//span[text() ='No Records Found']")

    JOB_TITLE_DROPDOWN = (By.XPATH, "(//div[@class='oxd-select-wrapper'])[1]")
    DROPDOWN_LIST = (By.XPATH, "//div[@class='oxd-select-text oxd-select-text--active']")

    def __init__(self, driver):
        super().__init__(driver)

    def verify_title_of_page(self):
        element = self.find(self.TITLE_OF_PAGE)
        assert element.is_displayed(), "Title is not shown on page"

    def select_job_title(self):
        # Dropdown açilir
        self.click(self.JOB_TITLE_DROPDOWN)
        # ActionChains ile elemente gidip tiklanir
        job_element = self.find(self.JOB_TITLE)
        self.action.move_to_element(job_element).click().perform()

    def fillout_page(self):
        self.select_job_title()
        # Yorum satirina alinan alanlar gerektiğinde aktif edilebilir:
        # dropdowns = self.find_elements(self.DROPDOWN_LIST)
        # for item in dropdowns:
        #     self.wait_for_element_to_be_clickable(item)
        #     item.click()

    def fill_out_job_title(self):
        pass

    def clicking_search_btn(self):
        self.click(self.SEARCH_BTN)

    def verify_no_record(self):
        element = self.find(self.NO_RECORD_MSG)
        assert element.is_displayed(), "Error message is not displayed"