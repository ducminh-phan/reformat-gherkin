@tag-1
@tag-2
Feature: Some meaningful feature

  Some meaningful feature description

  Background: A solid background

  Some description for this background
    This description has multiple lines

    Given A lot of money
      | EUR |
      | USD |
      | VND |

  @tag-no-1
  @decorate-1
  @fixture-1
  Scenario: Gain a lot of money
  This is a description for this scenario

    Given I go to the bank
    Then  I rob the bank

  @tag-no-2
  @decorate-2
  # Some comment here...
  @prepare-2 @fixture-2
  # Another comment...
  Scenario Outline: Break the bank's vault

  A description for this scenario outline

    # Is it helpful to put a comment here?
    Given I stand in front of the bank's vault
    And   I break the vault's door
    """
    Some docstring here
      A docstring can have multiple lines
        With indentation
    """
    Then  I enter the vault
    ```
    Some docstring there
    ```
    And   I see a lot of money


    # Examples can have tags? Hmmm...
  @test-examples-tags
    Examples: Continents

    This is the description for these examples

      | Asia    | 111 |
      | Europe  | 22  |
      # We can even have a comment in the middle of a table
      | America | 3   |
      # Pipe characters in table cells need to be escaped
      | a \| b        | 4 |

  Scenario: Escaping the bank
     When I exit the bank
     Then the police will start to chase me

  Rule: There can be only One

    Background: A rule can has a background
      A description for this background

    @tag-for-example-in-rule
    Example: Only One -- More than one alive
      # Comment in step in example in rule
      Given there are 3 ninjas
      And there are more than one ninja alive
      When 2 ninjas meet, they will fight
      Then one ninja dies (but not me)
      And there is one ninja less alive

    Example: Only One -- One alive
      Given there is only 1 ninja alive
      Then he (or she) will live forever ;-)

      Rule: A rule, looks like nested, but actually not

      A very meaningful description for this rule

        Scenario Outline: A scenario in a rule
          # Another comment in step in example in rule
          Given a setup step
          Then a condition is satisfied
          And the answer is <Answer>

          @examples-tag
            Examples: Examples
            This is the description for these examples
              | Answer | 42 |

    # The next line is a comment with spaces only, it should be stripped
    #         
    # Some random comment at the end of the document
