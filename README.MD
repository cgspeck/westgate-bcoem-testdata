# Westgate Brewers BCOE&M Test Data Generator

Our fork of [BCOE&M](https://github.com/cgspeck/brewcompetitiononlineentry).

This is run against the `v2.5.0.2-westgate` branch.

Victorian Postcode Data Extracted from [Australian Postcodes by Matthew Proctor](https://www.matthewproctor.com/australian_postcodes).

Street names from [Melbourne City Council](https://data.melbourne.vic.gov.au/Transport/Street-names/2x56-ai8r)

## Dependencies

Install:

* Poetry v1.2.0a2 or greater.
* pyenv
* direnv

Setup python and dependencies:

```shell
pyenv install
python -m venv .venv
source ./.venv/bin/activate
pip install poetry
poetry install
```

## Entry generator

* establish ssh reverse tunnel to database if necessary.
* copy and set `.envrc` then `direnv allow`
* execute: `python -m src.gen_entries`

## Score generator

* save column "Entry Number" from competition spreadsheet (including header)
* execute:

```shell
python -m src.gen_points
libreoffice results.csv
```

* Copy values from rows A - F back into tab "Score Entry" of competition spreadsheet
