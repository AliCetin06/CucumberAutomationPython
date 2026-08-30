from behave import when, then
from pages.forget_password_page import ForgetPasswordPage
from pages.login_page import LoginPage
from utils.driver_utils import DriverUtils


@then('verify user is on forget password page')
def verify_user_is_on_forget_password_page(context):
    # Sayfa nesneleri initialize ediliyor ve context'e ataniyor
    driver = DriverUtils.get_driver()
    context.login_page = LoginPage(driver)
    context.forget_password_page = ForgetPasswordPage(driver)

    context.forget_password_page.verify_forget_password_page()


@when('user enter invalid username on forget password page')
def user_enter_invalid_username_on_forget_password_page(context):
    context.forget_password_page.enter_user_name("sdfsdf")


@then('verify invalid username error message is displayed on forget password page')
def verify_invalid_username_error_message_is_displayed_on_forget_password_page(context):
    context.forget_password_page.verify_incorrect_username_msg()


@when('click on reset password button')
def click_on_reset_password_button(context):
    context.forget_password_page.click_reset_btn()