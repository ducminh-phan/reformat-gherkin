Feature: search Wikipedia

  Background:
    Given Open http://en.wikipedia.org
    And Do login

  Scenario Outline:
    Given Enter search term '<searchTerm>'
    When Do search
    Then Multiple results are shown for '<result>'

    Examples:
