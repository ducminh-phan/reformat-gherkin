Feature: Login

  Scenario: Successful login
    Given I have a username
    And I have a password

    When I submit the login form

    Then I should be logged in

  Scenario: No blank lines between steps
    Given I have a username
    When I submit the form
    Then I see the result
