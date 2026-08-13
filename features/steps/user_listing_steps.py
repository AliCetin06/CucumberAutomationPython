from behave import when, then
from pages.user_listing_page import UserListingPage
from utils.driver_utils import DriverUtils

@when('user click edit in admin user on UserListingPage')
def user_click_edit_in_admin_user_on_user_listing_page(context):
    context.user_listing_page = UserListingPage(DriverUtils.get_driver())
    context.user_listing_page.verify_title_of_page()

@then('verify to back on UserListingPage')
def verify_to_back_on_user_listing_page(context):
    context.user_listing_page.verify_title_of_page()