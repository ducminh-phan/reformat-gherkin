# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.1] - 2020-11-02

### Fixed

- Update `attrs` and `cattrs` to resolve dependencies conflict

## [2.0.0] - 2020-04-06

### Added

- Make indentation configurable ([#35](https://github.com/ducminh-phan/reformat-gherkin/issues/35))

### Changed

- Make single-line tags the default option to format tags ([#22](https://github.com/ducminh-phan/reformat-gherkin/issues/22))

### Fixed

- A RecursionError raised if there is a block of many consecutive comments ([#33](https://github.com/ducminh-phan/reformat-gherkin/issues/33))

- An error when formatting a file larger than 32 KB on Windows ([#34](https://github.com/ducminh-phan/reformat-gherkin/issues/34))

## [1.1.0] - 2020-01-25 - Lunar New Year

### Added

- Support for Python 3.8 ([#23](https://github.com/ducminh-phan/reformat-gherkin/pull/23))

- Allow formatting tags on a single line ([#22](https://github.com/ducminh-phan/reformat-gherkin/issues/22))

### Fixed

- Step keywords are not aligned correctly when specifying an alignment ([#27](https://github.com/ducminh-phan/reformat-gherkin/issues/27))

- Triple quotes in docstrings are not escaped ([#31](https://github.com/ducminh-phan/reformat-gherkin/issues/31))

## [1.0.2] - 2020-01-06

### Fixed

- Tables containing wide characters or zero-width characters are not aligned correctly ([#18](https://github.com/ducminh-phan/reformat-gherkin/issues/18))

- Pipe characters are not escaped in tables ([#21](https://github.com/ducminh-phan/reformat-gherkin/issues/21))

## [1.0.1] - 2019-12-12

### Fixed

- Fix error with non-English Gherkin files ([#15](https://github.com/ducminh-phan/reformat-gherkin/issues/15))

## [1.0.0] - 2019-08-25

- Initial release

[unreleased]: https://github.com/ducminh-phan/reformat-gherkin/compare/v2.0.1...develop
[2.0.1]: https://github.com/ducminh-phan/reformat-gherkin/compare/v2.0.0...v2.0.1
[2.0.0]: https://github.com/ducminh-phan/reformat-gherkin/compare/v1.1.0...v2.0.0
[1.1.0]: https://github.com/ducminh-phan/reformat-gherkin/compare/v1.0.2...v1.1.0
[1.0.2]: https://github.com/ducminh-phan/reformat-gherkin/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/ducminh-phan/reformat-gherkin/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/ducminh-phan/reformat-gherkin/releases/tag/v1.0.0
