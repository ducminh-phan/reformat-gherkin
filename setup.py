import ast
import re
from pathlib import Path

from setuptools import setup

CURRENT_DIR = Path(__file__).parent


def get_long_description() -> str:
    readme_md = CURRENT_DIR / "README.md"
    with open(readme_md, encoding="utf8") as f:
        return f.read()


def get_version() -> str:
    version_file = CURRENT_DIR / "reformat_gherkin" / "version.py"
    version_re = re.compile(r"__version__\s+=\s+(?P<version>.*)")

    with open(version_file, "r", encoding="utf8") as f:
        match = version_re.search(f.read())
        version = match.group(1) if match is not None else '"unknown"'

        return str(ast.literal_eval(version))


setup(
    # https://packaging.python.org/specifications/core-metadata/#name
    name="reformat-gherkin",  # Required
    # https://www.python.org/dev/peps/pep-0440/
    # https://packaging.python.org/en/latest/single_source_version.html
    version=get_version(),  # Required
    # https://packaging.python.org/specifications/core-metadata/#summary
    description="Formatter for gherkin language",  # Required
    # https://packaging.python.org/specifications/core-metadata/#description-optional
    long_description=get_long_description(),
    # https://packaging.python.org/specifications/core-metadata/#description-content-type-optional
    long_description_content_type="text/markdown",
    url="https://github.com/ducminh-phan/reformat-gherkin",
    author="Duc-Minh Phan",
    author_email="alephvn@gmail.com",
    license="MIT",
    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Quality Assurance",
    ],
    packages=["reformat_gherkin"],  # Required
    python_requires=">=3.6",
    test_suite="tests",
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[
        "gherkin-official (>=4.1,<5.0)",
        "click (>=7.0,<8.0)",
        "attrs (>=19.1,<20.0)",
        "cattrs (>=0.9.0,<0.10.0)",
    ],
    entry_points={"console_scripts": ["reformat-gherkin=reformat_gherkin.cli:main"]},
)
