import csv
from pathlib import Path

from src.datadefs import Style, Suburb

CLUBS = [
    "Bayside Brewers",
    "Merri Mashers",
    "South West Homebrewers",
    "Way Out West",
    "Westgate Brewers",
    "Worthogs",
]
STREET_NAMES: list[str] = []
STYLES: list[Style] = []
SUBURBS: list[Suburb] = []

if len(STREET_NAMES) == 0:
    STREET_NAMES = Path("data/street_names.csv").read_text().splitlines()

if len(STYLES) == 0:
    # TODO: load this from the DB based on what styles are enabled!
    dr = csv.DictReader(Path("data/brew_styles.csv").open())
    for r in dr:
        STYLES.append(
            Style(
                id=str(r["id"]),
                brew_style_group=str(r["brewStyleGroup"]),
                brew_style_name=str(r["brewStyle"]),
                brew_style_num=str(r["brewStyleNum"]),
            )
        )

if len(SUBURBS) == 0:
    SUBURBS = [
        Suburb(rec[0], str(rec[1]))
        for rec in [
            r.split(",") for r in Path("data/postcodes.csv").read_text().splitlines()
        ]
    ]
