Feature: Menu item validation job options

  Tester -Ali

  Background:
    Given the user opens the website
    Then the login page is displayed
    When the user logs in with valid credentials
    And verify user is navigated to home page

  Scenario: validation of job options present on Adminpage
    When user click to Admin tab
    Then verify user on Adminpage
    When user click to job option
    Then verify all options showing in job menu

  # validation with data table
  @datatable
  Scenario: validation of job options present on Adminpage with data table
    When user click to Admin tab
    Then verify user on Adminpage
    When user click to job option
    Then verify Job sub menu items has following data
      | Job Menu Items    |
      | Job Titles        |
      | Pay Grades        |
      | Employment Status |
      | Job Categories    |
      | Work Shifts       |