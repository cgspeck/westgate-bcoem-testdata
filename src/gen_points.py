#!/usr/bin/env python3
import csv
import _csv
from dataclasses import dataclass
import itertools
from pathlib import Path
import argparse
from random import randint, shuffle
from MySQLdb.cursors import Cursor
import sys

from src.db import get_db

AROMA_MAX = 10
APPEARANCE_MAX = 5
FLAVOUR_MAX = 20
BODY_MAX = 5
OVERALL_MAX = 10

SCORE_SPREAD_MAX = 7
SCORES_PER_ENTRY = 3

LOAD_ENTRY_IDS_SQL = """
SELECT id FROM `brewing` ORDER BY id ASC;
"""


@dataclass
class ScoreSheet:
    entry_id: int
    aroma: int
    appearance: int
    flavour: int
    body: int
    overall: int

    @property
    def total(self):
        return self.aroma + self.appearance + self.flavour + self.body + self.overall

    @classmethod
    def write_csv_header(cls, writer: "_csv._writer"):
        writer.writerow(
            ["Entry Number", "Aroma", "Appearance", "Flavour", "Body", "Overall"]
        )

    def emit_csv_row(self):
        return [
            self.entry_id,
            self.aroma,
            self.appearance,
            self.flavour,
            self.body,
            self.overall,
        ]


def generate_score_sheet(entry_id: int):
    return ScoreSheet(
        entry_id=entry_id,
        aroma=randint(0, AROMA_MAX),
        appearance=randint(0, APPEARANCE_MAX),
        flavour=randint(0, FLAVOUR_MAX),
        body=randint(0, BODY_MAX),
        overall=randint(0, OVERALL_MAX),
    )


def _load_entryids_from_csv(reader: "_csv._reader") -> list[int]:
    entry_ids: list[int] = []
    for row in reader:
        if len(row) > 0:
            entry_ids.append(int(row[0]))

    return sorted(entry_ids)


def _load_entryids_from_database() -> list[int]:
    entry_ids: list[int] = []
    db = get_db()
    cur: Cursor = db.cursor()
    cur.execute(LOAD_ENTRY_IDS_SQL)

    for row in cur:
        if len(row) > 0:
            entry_ids.append(row[0])

    return sorted(entry_ids)


def main(entry_ids: list[int], writer: "_csv._writer"):
    print(f"{len(entry_ids)} entries: {entry_ids}")
    memo: list[list[ScoreSheet]] = []

    for entry_id in entry_ids:
        print(f"Generating scores for entry {entry_id}")
        entry_memo: list[ScoreSheet] = []

        while len(entry_memo) < SCORES_PER_ENTRY:
            print(".", end="")
            tmp = generate_score_sheet(entry_id)

            if len(entry_memo) == 0:
                entry_memo.append(tmp)

            totals = [tmp.total]
            totals.extend([e.total for e in entry_memo])
            min_score = min(totals)
            max_score = max(totals)

            if max_score - min_score <= SCORES_PER_ENTRY:
                entry_memo.append(tmp)

        memo.append(entry_memo)
        print()

    if len(memo) == 0:
        print("No score sheets generated 🤷")
        return

    print("Shuffling the score sheets...")
    shuffle(memo)
    print("Writing header...")
    memo[0][0].write_csv_header(writer)
    flattened = list(itertools.chain.from_iterable(memo))
    values = [f.emit_csv_row() for f in flattened]
    print("Writing rows...")
    writer.writerows(values)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate a matrix of scores",
        usage="%(prog)s entry-ids.csv results.csv",
    )
    parser.add_argument(
        "input_filepath", help="Path to CSV of entry ids", nargs="?", default=None
    )
    parser.add_argument(
        "--output_filepath",
        "-O",
        default="results.csv",
        help="Path to output CSVs, will be overwritten",
    )
    parser.set_defaults()
    args = parser.parse_args()

    if args.input_filepath is not None:
        print("Loading Entry IDs from CSV")
        reader = csv.reader(Path(args.input_filepath).read_text().splitlines())
        expected_header = "Entry Number"
        header_row = next(reader)
        if len(header_row) == 0:
            print(f"Unable to read file {args.input_filepath}")
            sys.exit(1)

        if header_row[0] != expected_header:
            print(f"Expected header '{expected_header}' not found, got '{header_row}'")
            sys.exit(1)

        entry_ids = _load_entryids_from_csv(reader)
    else:
        print("Loading Entry IDs from the Database")
        entry_ids = _load_entryids_from_database()

    print(f"Opening {args.output_filepath}")

    with Path(args.output_filepath).open("wt") as fh:
        writer = csv.writer(fh)
        main(entry_ids, writer)
        print(f"Closing {args.output_filepath}")
