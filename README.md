# Reformat-gherkin

[![Build Status](https://dev.azure.com/alephvn/reformat-gherkin/_apis/build/status/ducminh-phan.reformat-gherkin?branchName=master)](https://dev.azure.com/alephvn/reformat-gherkin/_build/latest?definitionId=1&branchName=master) &nbsp; [![Build Status](https://travis-ci.com/ducminh-phan/reformat-gherkin.svg?branch=master)](https://travis-ci.com/ducminh-phan/reformat-gherkin) &nbsp; [![Coverage Status](https://coveralls.io/repos/github/ducminh-phan/reformat-gherkin/badge.svg?branch=master)](https://coveralls.io/github/ducminh-phan/reformat-gherkin?branch=master)

[![Maintainability](https://api.codeclimate.com/v1/badges/16718a231901c293215d/maintainability)](https://codeclimate.com/github/ducminh-phan/reformat-gherkin/maintainability) &nbsp; [![Codacy Badge](https://api.codacy.com/project/badge/Grade/e675ca51b6ac436a980facbcf04b8e5a)](https://www.codacy.com/app/ducminh-phan/reformat-gherkin)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) &nbsp; [![PyPI](https://img.shields.io/pypi/v/reformat-gherkin.svg)](https://pypi.org/project/reformat-gherkin/) &nbsp; [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

## Table of Contents

- [About](#about)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Pre-commit hook](#pre-commit-hook)
- [Acknowledgements](#acknowledgements)

## About

This tool is a formatter for Gherkin files. It ensures consistent look regardless of the project and authors.

`reformat-gherkin` can be used either as a command-line tool, or a `pre-commit` hook.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- [Python 3.6+](https://www.python.org/downloads/)
- [Poetry](https://poetry.eustace.io/)

### Installing

1. Clone this repository

   ```bash
   git clone https://github.com/ducminh-phan/reformat-gherkin.git
   ```

2. Install dependencies

   ```bash
   cd reformat-gherkin
   poetry install
   ```

3. Install `pre-commit` hooks (if you want to contribute)

   ```bash
   pre-commit install
   ```

## Usage

```text
Usage: reformat-gherkin [OPTIONS] [SRC]...

  Reformat the given Gherkin files and all files in the given directories
  recursively.

Options:
  --check                         Don't write the files back, just return the
                                  status. Return code 0 means nothing would
                                  change. Return code 1 means some files would
                                  be reformatted. Return code 123 means there
                                  was an internal error.
  -a, --alignment [left|right]    Specify the alignment of step keywords
                                  (Given, When, Then,...). If specified, all
                                  statements after step keywords are left-
                                  aligned, spaces are inserted before/after
                                  the keywords to right/left align them. By
                                  default, step keywords are left-aligned, and
                                  there is a single space between the step
                                  keyword and the statement.
  -n, --newline [LF|CRLF]         Specify the line separators when formatting
                                  files inplace. If not specified, line
                                  separators are preserved.
  --fast / --safe                 If --fast given, skip the sanity checks of
                                  file contents. [default: --safe]
  --single-line-tags / --multi-line-tags
                                  If --single-line-tags given, output
                                  consecutive tags on one line. If --multi-
                                  line-tags given, output one tag per line.
                                  [default: --multi-line-tags]
  --config FILE                   Read configuration from FILE.
  --version                       Show the version and exit.
  --help                          Show this message and exit.
```

### Config file

The tool is able to read project-specific default values for its command line options from a `.reformat-gherkin.yaml` file.

By default, `reformat-gherkin` looks for the config file starting from the common base directory of all files and directories passed on the command line. If it's not there, it looks in parent directories. It stops looking when it finds the file, or a .git directory, or a .hg directory, or the root of the file system, whichever comes first.

Example config file

```yaml
check: False
alignment: left
```

## Pre-commit hook

Once you have installed [pre-commit](https://pre-commit.com/), add this to the `.pre-commit-config.yaml` in your repository:

```text
repos:
  - repo: https://github.com/ducminh-phan/reformat-gherkin
    rev: stable
    hooks:
      - id: reformat-gherkin
```

Then run `pre-commit install` and you're ready to go.

## Acknowledgements

This project is inspired by [black](https://github.com/psf/black). Some functions are taken from `black`'s source code.
