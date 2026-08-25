from behave import given, then
from utils.mobile_driver import MobileDriver
from pages.settings_page import SettingsPage

@given('User launches the mobile Settings app')
def step_impl(context):
    context.driver = MobileDriver.get_driver()
    context.settings_page = SettingsPage(context.driver)

@then('User should see the search bar on the screen')
def step_impl(context):
    try:
        context.settings_page.verify_search_bar_displayed()
    finally:
        context.driver.quit()