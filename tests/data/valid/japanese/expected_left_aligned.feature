# language: ja

フィーチャ: Japanese Gherkin documents

  シナリオ: Aligning step keywords with wide characters
    前提   I have a Japanese Gherkin document
    もし   I run reformat-gherkin with an alignment option
    ならば the step keywords should be aligned
