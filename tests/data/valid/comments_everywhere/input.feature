# Comment 1
@tag-1
# Comment 2
@tag-2
# Comment 3
Feature: Some meaningful feature
  Some meaningful feature description

  # Comment 5
  Background: A solid background

  Some description for this background
  This description has multiple lines
    
    # Comment 7
    Given A lot of money
      # Comment 8
      | EUR |
      # Comment 9
      | USD |
      | VND |

  # Comment 10
  @tag-no-1
  @decorate-1
  @fixture-1
  # Comment 11
  Scenario: Gain a lot of money
  This is a description for this scenario

    # Comment 12
    Given I go to the bank
    Then  I rob the bank

  @tag-no-2
  @decorate-2
  @prepare-2 @fixture-2
  Scenario Outline: Break the bank's vault

  A description for this scenario outline

    # # Comment 13
    Given I stand in front of the bank's vault
    And   I break the vault's door
    """
    Some docstring here
    """
    Then  I enter the vault
    ```
    Some docstring there
    ```
    And   I see a lot of money


  @test-examples-tags
    # Comment 14
    Examples: Continents

    This is the description for these examples

      # Comment 15
      | Asia    | 111 |
      | Europe  | 22  |
      # Comment 17
      | America | 3   |


    # Comment 18
