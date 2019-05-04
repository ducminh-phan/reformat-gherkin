from pathlib import Path

from setuptools import setup

CURRENT_DIR = Path(__file__).parent
# Get the long description from the README file
with open(CURRENT_DIR / "README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    # https://packaging.python.org/specifications/core-metadata/#name
    name="reformat-gherkin",  # Required
    # https://www.python.org/dev/peps/pep-0440/
    # https://packaging.python.org/en/latest/single_source_version.html
    version="1.0.0",  # Required
    # https://packaging.python.org/specifications/core-metadata/#summary
    description="Formatter for gherkin language",  # Required
    # https://packaging.python.org/specifications/core-metadata/#description-optional
    long_description=long_description,
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
