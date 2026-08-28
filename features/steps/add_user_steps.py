from behave import when, then
from pages.add_user_page import AddUserPage
from pages.user_listing_page import UserListingPage
from utils.driver_utils import DriverUtils


@then('verify user is on addUserPage')
def verify_user_is_on_user_details_page(context):
    # DriverUtils.get_driver() üzerinden driver alınıp sayfa başlatılır
    context.add_user_page = AddUserPage(DriverUtils.get_driver())
    context.add_user_page.verify_title_of_page()


@when('user change to name of Admin to different name')
def user_change_to_name_of_admin_to_different_name(context):
    context.add_user_page.fill_required_user_details()


@when('user click to save button')
def user_click_to_save_button(context):
    context.add_user_page.click_on_save_btn()


@when('user click edit  in admin user on UserListingPage')
def user_click_edit_admin_user(context):
    if not hasattr(context, 'user_listing_page'):
        context.user_listing_page = UserListingPage(DriverUtils.get_driver())
    context.user_listing_page.click_on_edition_btn()


@then('verify to back on  UserListingPage')
def verify_to_back_on_user_listing_page(context):
    if not hasattr(context, 'user_listing_page'):
        context.user_listing_page = UserListingPage(DriverUtils.get_driver())
    context.user_listing_page.verify_title_of_page()