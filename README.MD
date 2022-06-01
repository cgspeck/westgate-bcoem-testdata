# Westgate Brewers BCOE&M Test Data Generator

Our fork of [BCOE&M](https://github.com/cgspeck/brewcompetitiononlineentry).

This is run against the `v2.4.0.3-westgate` branch.

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
poetry install
```

## Entry generator

* Establish ssh reverse tunnel to database if necessary.
* Copy and set `.envrc` then `direnv allow`
* Execute: `poetry run python src/gen-entries.py`
