#  @smoke --> you can categorize feature level or sceneraio level
Feature: We are testing the login functionality in this feature

  Developer - Chirag
  Tester - Ali

  Background:
    Given user open website
    Then verify user is on login page

  @smoke @chirag @ie
  Scenario: verify Login Sucessful With Valid Credentials
    When user login with username "login.username" and password "login.password"
    Then verify user is navigated to home page

  # Scenario Outline way for all negative scenarios  , there is no error message with blank credintial ,so did not add to Outline
  @regression @yusuf
  Scenario Outline: verify Error Message UnSuccesful With InValid Credentials
    When user login with invalid credintial username "<username>" and password "<password>"
    Then verify invalid login error message is displayed

    Examples:
      | username | password    |
      | demo     | test1234234 |
      | admin    | fghjfghjn   |
      | sdvsdf   | admin123    |

  @regression @ali
  Scenario: verify Error Message UnSuccesful With  Blank Credentials
    When user login with username "" and password ""
    Then verify invalid login error message blank is displayed

  @regression @ali
  Scenario: verify Error Message UnSuccesful With InValid Credentials
    When user login with username "demo" and password "test1234234"
    Then verify invalid login error message is displayed

  @regression @ali
  Scenario: verify Error Message With Valid username Invalid password
    When user login with username "admin" and password "fghjfghjn"
    Then verify invalid login error message is displayed

  @regression @ali
  Scenario: verify Error Message With  InValid username Valid password
    When user login with username "sdvsdf" and password "admin123"
  Then verify invalid login error message is displayed

  @smoke @wip
  Scenario: verify Error Message For Forget Password Incorrect User
    When user click on forget password link
    Then verify user is on forget password page
    When user enter invalid username on forget password page
    And click on reset password button
    Then verify invalid username error message is displayed on forget password page
