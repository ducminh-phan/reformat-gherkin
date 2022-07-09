Feature: Docstrings

  Scenario: Escaping docstrings
    Given I have a docstring
      """
      This docstring has \"escaped\" double quotes.
      It also has \`escaped\` backticks.
      """
    And I have a docstring with an escaped docstring in
      """
      This is another docstring.
        \"\"\"
        It has an escaped docstring inside it.
        \"\"\"
      """
    And I have a backtick docstring
      """
      This docstring has \"escaped\" double quotes.
      It also has \`escaped\` backticks.
      """
    And I have a nested single-quote docstring
      """
      This is a backtick docstring.
        ```
        It also has an escaped docstring inside it.
        ```
      """
    Then the escaped characters are printed when the document is reformatted
