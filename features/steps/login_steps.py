"""Step definitions for the login feature."""
from behave import given, when, then

from pages.login_page import LoginPage
from utils.driver_utils import DriverUtils
from utils.property_reader import PropertyReader


# ---------- Setup ----------

@given('the user opens the website')
def open_website(context):
    """Precondition: launch the browser and open the application URL."""
    context.login_page = LoginPage(DriverUtils.get_driver())
    context.login_page.open_website()


@then('the login page is displayed')
def verify_login_page_displayed(context):
    """Confirm the app is reachable and the login form is visible."""
    context.login_page.verify_login_of_page()


# ---------- Login actions ----------

@when('the user logs in with valid credentials')
def login_with_valid_credentials(context):
    """Happy path: credentials are read from the config file, never hardcoded."""
    username = PropertyReader.get_property("login.username")
    password = PropertyReader.get_property("login.password")
    context.login_page.do_login(username, password)


@when('the user logs in with username "{username}" and password "{password}"')
def login_with_given_credentials(context, username, password):
    """Data-driven login: values come straight from the feature file."""
    context.login_page.do_login(username, password)


@when('the user logs in with blank credentials')
def login_with_blank_credentials(context):
    """Edge case: submit the form with both fields empty."""
    context.login_page.do_login("", "")


# ---------- Login assertions ----------

@then('an invalid credentials error message is displayed')
def verify_invalid_credentials_error(context):
    """Wrong username/password must be rejected with a clear message."""
    context.login_page.validate_login_error_msg_invalid()


@then('a required field error message is displayed')
def verify_required_field_error(context):
    """Empty fields must trigger the 'Required' validation message."""
    context.login_page.validate_login_error_msg_blank()


# ---------- Forgot password (remaining steps live in their own file) ----------

@when('user click on forget password link')
def click_forgot_password(context):
    """Navigate to the reset password flow."""
    context.login_page.clicking_forget_password()