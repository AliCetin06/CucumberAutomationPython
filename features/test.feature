Feature: We are testing the Candidates page  functionality in this features

 @wip
 Scenario: verify to showing no record found in system when you search
    Given user open website
		When user login with valid credentials
		Then verify user is navigated to home page
    When user click to recruitment tab in Homepage
    Then  verify user in Candidates page
    When user fillout the pages in Candidates page
    And user click to search button in Candidates page
    Then verify showing no record found
