# Reformat-gherkin

[![Build Status](https://travis-ci.com/ducminh-phan/reformat-gherkin.svg?branch=master)](https://travis-ci.com/ducminh-phan/reformat-gherkin) [![Coverage Status](https://coveralls.io/repos/github/ducminh-phan/reformat-gherkin/badge.svg?branch=master)](https://coveralls.io/github/ducminh-phan/reformat-gherkin?branch=master) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black) [![Maintainability](https://api.codeclimate.com/v1/badges/16718a231901c293215d/maintainability)](https://codeclimate.com/github/ducminh-phan/reformat-gherkin/maintainability) [![GitHub release](https://img.shields.io/github/release/ducminh-phan/reformat-gherkin.svg)](https://github.com/ducminh-phan/reformat-gherkin)

## Usage

    Usage: reformat-gherkin [OPTIONS] [SRC]...
    
      Reformat the given Gherkin files and all files in the given directories
      recursively.
    
    Options:
      --check                       Don't write the files back, just return the
                                    status. Return code 0 means nothing would
                                    change. Return code 1 means some files would
                                    be reformatted. Return code 123 means there
                                    was an internal error.
      -a, --alignment [left|right]  Specify the alignment of step keywords (Given,
                                    When, Then,...). If specified, all statements
                                    after step keywords are left-aligned, spaces
                                    are inserted before/after the keywords to
                                    right/left align them. By default, step
                                    keywords are left-aligned, and there is a
                                    single space between the step keyword and the
                                    statement.
      --fast / --safe               If --fast given, skip the sanity checks of
                                    file contents. [default: --safe]
      --version                     Show the version and exit.
      --help                        Show this message and exit.

## Pre-commit hook

Once you have installed [pre-commit](https://pre-commit.com/), add this to the `.pre-commit-config.yaml` in your repository:

    repos:
    -   repo: https://github.com/ducminh-phan/reformat-gherkin
        rev: stable
        hooks:
        - id: reformat-gherkin

Then run `pre-commit install` and you're ready to go.
