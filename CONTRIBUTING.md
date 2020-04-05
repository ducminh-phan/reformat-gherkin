# Contributing

Welcome to the reformat-gherkin project! Thank you for taking the time to
contribute. We welcome all contributions, whether that's reporting a bug,
requesting a new feature, submitting a fix, or adding documentation.

## Reporting bugs and requesting features

To report a bug or request a new feature,
[create a new issue on GitHub](https://github.com/ducminh-phan/reformat-gherkin/issues/new).

## Contributing code

### Prerequisites

- [Python 3.6+](https://www.python.org/downloads/)
- [Poetry](https://poetry.eustace.io/)

### Setting up a development environment

1. Clone this repository

   ```bash
   git clone https://github.com/ducminh-phan/reformat-gherkin.git
   ```

2. Install dependencies

   ```bash
   cd reformat-gherkin
   poetry install
   ```

3. Install `pre-commit` hooks

   ```bash
   poetry run pre-commit install
   ```

### Running tests

The tests are run with `pytest`.

```bash
poetry run pytest tests
```

Please add/update the tests along with your contribution.

### Pull requests

- Please create a GitHub Pull Request with the base branch of `develop`.
- Ensure the PR description clearly describes the problem and solution. Include the relevant issue number if applicable.
- Before submitting, update README.md with details of changes to the usage if applicable.
