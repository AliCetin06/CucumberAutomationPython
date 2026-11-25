Feature: Login functionality

  Developer - Chirag
  Tester - Ali

  Background:
    Given the user opens the website
    Then the login page is displayed

  @smoke @chirag @ie
  Scenario: Successful login with valid credentials
    When the user logs in with valid credentials
    Then verify user is navigated to home page

  @regression @ali
  Scenario Outline: Login fails with <description>
    When the user logs in with username "<username>" and password "<password>"
    Then an invalid credentials error message is displayed

    Examples:
      | description                      | username | password    |
      | invalid username and password    | demo     | test1234234 |
      | valid username, invalid password | admin    | fghjfghjn   |
      | invalid username, valid password | sdvsdf   | admin123    |

  @regression @ali
  Scenario: Login fails with blank credentials
    When the user logs in with blank credentials
    Then a required field error message is displayed

  @smoke @regression
  Scenario: Error message for forgot password with an incorrect username
    When user click on forget password link
    Then verify user is on forget password page
    When user enter invalid username on forget password page
    And click on reset password button
    Then verify invalid username error message is displayed on forget password page

  @smoke @regression
  Scenario: Logged in user can open the Admin tab
    When the user logs in with valid credentials
    Then verify user is navigated to home page
    When user click to Admin tab

  @regression @edge
  Scenario: Login fails with only username filled
    When the user logs in with only username "Admin"
    Then a required field error message is displayed

  @regression @edge
  Scenario: Login fails with only password filled
    When the user logs in with only password "admin123"
    Then a required field error message is displayed

  @regression @security
  Scenario Outline: Login is rejected for <description>
    When the user logs in with username "<username>" and password "<password>"
    Then an invalid credentials error message is displayed

    Examples:
      | description              | username | password    |
      | SQL injection input      | ' OR '1'='1 | ' OR '1'='1 |
      | special characters       | !@#$%^&* | !@#$%^&*    |
      | wrong password case      | Admin    | ADMIN123    |