Feature: User Greeting
  Scenario: User greeting login
    Given I am login as "root"
    When I visit the homepage
    Then I should see "Welcome root"
