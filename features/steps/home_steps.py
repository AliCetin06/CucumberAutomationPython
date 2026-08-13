from behave import when, then
from pages.home_page import HomePage
from utils.driver_utils import DriverUtils


@then('verify user is navigated to home page')
def verify_user_is_navigated_to_homepage(context):
    context.home_page = HomePage(DriverUtils.get_driver())
    context.home_page.validate_home_page()


@when('user click to Admin tab')
def user_click_to_admin_tab(context):
    if not hasattr(context, 'home_page'):
        context.home_page = HomePage(DriverUtils.get_driver())
    context.home_page.clicking_admin_btn()


@when('user click to recruitment tab in Homepage')
def user_click_to_recruitment_tab_in_homepage(context):
    if not hasattr(context, 'home_page'):
        context.home_page = HomePage(DriverUtils.get_driver())
    context.home_page.clicking_recruitment()