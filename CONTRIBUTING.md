# Contributing to `reformat-gherkin`

Thank you for taking the time to contribute!

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

## Testing

We use `pytest` for unit and integration tests. Please add/update the tests along with your contribution.

## Submitting Changes

- Please create a GitHub Pull Request with the base branch of `develop`.
- Ensure the PR description clearly describes the problem and solution. Include the relevant issue number if applicable.
- Before submitting, update README.md with details of changes to the usage if applicable.
