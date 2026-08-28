from behave import when, then
from pages.admin_page import AdminPage
from utils.driver_utils import DriverUtils


@then('verify user on Adminpage')
def verify_user_on_adminpage(context):
    context.admin_page = AdminPage(DriverUtils.get_driver())
    context.admin_page.verify_title_of_page()


@when('user click to job option')
def user_click_to_job_option(context):
    context.admin_page.clicking_to_job_option()


@then('verify all options showing in job menu')
def verify_all_options_showing_in_job_menu(context):
    context.admin_page.verifying_all_options()


@then('verify Job sub menu items has following data')
def verify_job_sub_menu_items_has_following_data(context):
    # 'Job Menu Items' başlığının altındaki verileri listeler
    list_of_items = [row['Job Menu Items'] for row in context.table]

    context.admin_page.verify_job_sub_menu_items(list_of_items)