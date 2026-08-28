

Feature: add user functionity in this feature


  Scenario: Verify change to admin name on add userpage
    Given user open website
    When user login with username "login.username" and password "login.password"
    Then verify user is navigated to home page
    When user click to Admin tab
    And user click edit  in admin user on UserListingPage
    Then verify user is on addUserPage
    When user change to name of Admin to different name
    And user click to save button
    Then verify to back on  UserListingPage






