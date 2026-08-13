from behave import given, then
from pages.data_table_home_page import DataTableHomePage
from utils.driver_utils import DriverUtils


@given('user open the datatables website')
def user_open_the_datatables_website(context):
    context.datatable_page = DataTableHomePage(DriverUtils.get_driver())
    context.datatable_page.open_data_table_website()


@then('verify user is on datatables homepage')
def verify_user_is_on_datatables_homepage(context):
    context.datatable_page.verify_of_data_home_page()


@then('verify Table datas has following data')
def verify_table_datas_following_data(context):
    # Header ve tüm satırları birleştirerek ilk satırı kaybetmiyoruz:
    list_of_items = [context.table.headings] + [list(row) for row in context.table]
    context.datatable_page.verify_data_table_data(list_of_items)


@then('verify Table datas has following data with header')
def verify_table_datas_has_following_data_with_header(context):
    list_of_map = [dict(zip(context.table.headings, row)) for row in context.table]
    context.datatable_page.verify_data_table_data_with_header(list_of_map)