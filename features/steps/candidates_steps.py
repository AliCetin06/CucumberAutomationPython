from behave import when, then, step
from pages.candidates_page import CandidatesPage
from utils.driver_utils import DriverUtils

@then('verify user in Candidates page')
def verify_user_in_candidates_page(context):
    context.candidates_page = CandidatesPage(DriverUtils.get_driver())
    context.candidates_page.verify_title_of_page()

@when('user fillout the pages in Candidates page')
def user_fillout_the_pages(context):
    context.candidates_page.fillout_page()

@step('user click to search button in Candidates page')
def user_click_to_save_button_in_candidates_page(context):
    # Behave'de @step dekoratörü hem 'When' hem 'And' adimlari ile eşleşir
    context.candidates_page.clicking_search_btn()

@then('verify showing no record found')
def verify_showing_no_record_found(context):
    context.candidates_page.verify_no_record()