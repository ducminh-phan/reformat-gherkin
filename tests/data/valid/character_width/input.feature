Feature: Character width

  Scenario: Aligning tables
    Given a table of strings containing wide characters
      | aaa |
      | あああ |
    And a table of strings containing combining characters
      | aaa |
      | ááá |
    When I run reformat-gherkin
    Then the tables should be aligned

  Scenario Outline: Aligning wide character examples
    Then examples tables containing '<string>' should be aligned

    Examples:
      | string |
      | aaaaaaaa |
      | ああああああああ |

  Scenario Outline: Aligning combining character examples
    Then examples tables containing '<string>' should be aligned

    Examples:
      | string |
      | aaaaaaaa |
      | áááááááá |
