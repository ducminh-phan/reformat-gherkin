Feature: Docstrings with spaces

  Scenario: Removing spaces from docstrings
    Given I have a docstring
    """
    This docstring has spaces after the last word
    """
    And There is a docstring with populated blank lines in it
    """
    This docstring has an empty line in it

    That empty line has spaces on it
    """
    And There is a docstring with unpopulated blank lines in it
    """
    This docstring has an empty line in it

    That empty line has no spaces on it
    """
