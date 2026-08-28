from behave import given, then
from pages.data_table_home_page import DataTableHomePage


@given('user open the datatables website')
def step_open_website(context):
    if not hasattr(context, 'datatable_page'):
        context.datatable_page = DataTableHomePage(context.driver)

    context.datatable_page.open_data_table_website()


@then('verify user is on datatables homepage')
def step_verify_homepage(context):
    context.datatable_page.verify_of_data_home_page()


@then('verify Table datas has following data')
def step_verify_table_data(context):
    # context.table artık header satırını (name, position, office, age, start_date)
    # otomatik olarak ayırıyor; context.table.rows sadece veri satırlarını içerir.
    list_of_items = [list(row) for row in context.table]
    context.datatable_page.verify_data_table_data(list_of_items)