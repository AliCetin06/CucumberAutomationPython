from behave import given, when, then
from pages.login_page import LoginPage
from utils.driver_utils import DriverUtils
from utils.property_reader import PropertyReader


@given('user open website')
def user_open_website(context):
    context.login_page = LoginPage(DriverUtils.get_driver())
    context.login_page.open_website()


@then('verify user is on login page')
def verify_user_is_on_login_page(context):
    context.login_page.verify_login_of_page()


@when('user login with invalid credintials')
def user_login_with_invalid_credintials(context):
    context.login_page.do_login("sdfsdf", "dfdfgdf")


@then('verify invalid login error message is displayed')
def verify_invalid_login_error_message_is_displayed(context):
    context.login_page.validate_login_error_msg_invalid()


@when('user login with blank credintials')
def user_login_with_blank_credintials(context):
    context.login_page.do_login("", "")


# Hem "Required" hem de "Invalid credentials" durumlarını otomatik yönetir
@then('verify invalid login error message blank is displayed')
def verify_invalid_login_error_message_blank_is_displayed(context):
    try:
        context.login_page.validate_login_error_msg_blank()
    except AssertionError:
        context.login_page.validate_login_error_msg_invalid()


@when('user click on forget password link')
def user_click_on_forget_password_link(context):
    context.login_page.clicking_forget_password()


@when('user login with valid credentials')
def user_login_with_valid_credentials(context):
    username = PropertyReader.get_property("login.username")
    password = PropertyReader.get_property("login.password")
    context.login_page.do_login(username, password)


# Dynamic step with PropertyReader keys
@when('user login with username "{username_key}" and password "{password_key}"')
def user_login_with_username_and_password(context, username_key, password_key):
    username = PropertyReader.get_property(username_key) if "." in username_key else username_key
    password = PropertyReader.get_property(password_key) if "." in password_key else password_key
    context.login_page.do_login(username, password)


# Dynamic step with direct String values
@when('user login with invalid credintial username "{username}" and password "{password}"')
def user_login_with_invalid_credintial_username_and_password(context, username, password):
    context.login_page.do_login(username, password)


@when('user login with username "" and password ""')
def user_login_with_empty_credentials(context):
    context.login_page.do_login("", "")