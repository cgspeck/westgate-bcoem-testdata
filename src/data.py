from dataclasses import dataclass
from pathlib import Path
import json
from pprint import pformat
import sys

from src.datadefs import Style, Suburb
from src.db import get_db

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

GET_SELECTED_STYLES_SQL = """
SELECT prefsSelectedStyles FROM preferences;
"""


@dataclass
class PrefsSelectedStyle:
    id: str
    brewStyle: str  # 'English Porter [BJCP 13C]'
    brewStyleGroup: str  # '10'
    brewStyleNum: str  # '01'
    brewStyleVersion: str  # 'AABC2022'


if len(STREET_NAMES) == 0:
    STREET_NAMES = Path("data/street_names.csv").read_text().splitlines()

if len(STYLES) == 0:
    db = get_db()
    cursor = db.cursor()
    cursor.execute(GET_SELECTED_STYLES_SQL)
    raw = cursor.fetchone()[0]
    data = json.loads(raw)
    styles: list[PrefsSelectedStyle] = []
    for k, v in data.items():
        styles.append(PrefsSelectedStyle(id=k, **v))

    for style in styles:
        STYLES.append(
            Style(
                id=style.id,
                brew_style_group=style.brewStyleGroup,
                brew_style_name=style.brewStyle,
                brew_style_num=style.brewStyleNum,
            )
        )
    print("Loaded selected styles:")
    print(pformat(STYLES))

if len(SUBURBS) == 0:
    SUBURBS = [
        Suburb(rec[0], str(rec[1]))
        for rec in [
            r.split(",") for r in Path("data/postcodes.csv").read_text().splitlines()
        ]
    ]
