#!/usr/bin/env python3
import csv
import _csv
from dataclasses import dataclass
import itertools
from pathlib import Path
import argparse
from random import randint, shuffle
import sys

AROMA_MAX=10
APPEARANCE_MAX=5
FLAVOUR_MAX=20
BODY_MAX=5
OVERALL_MAX=10

SCORE_SPREAD_MAX=7
SCORES_PER_ENTRY=3

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
    def write_csv_header(cls, writer: '_csv._writer'):
        writer.writerow([
            "Entry Number",
            "Aroma",
            "Appearance",
            "Flavour",
            "Body",
            "Overall"
        ])

    def emit_csv_row(self):
        return [
            self.entry_id,
            self.aroma,
            self.appearance,
            self.flavour,
            self.body,
            self.overall
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

def main(reader: '_csv._reader', writer: '_csv._writer'):
    entry_ids: list[int] = []
    for row in reader:
        if len(row) > 0:
            entry_ids.append(int(row[0]))
    
    entry_ids.sort()
    print(f"{len(entry_ids)} entries: {entry_ids}")
    memo: list[list[ScoreSheet]] = []
    
    for entry_id in entry_ids:
        print(f"Generating scores for entry {entry_id}")
        entry_memo: list[ScoreSheet] = []
        
        while len(entry_memo) < SCORES_PER_ENTRY:
            print('.', end='')
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
    print("hello world")
    parser = argparse.ArgumentParser(
        description='Generate a matrix of scores',
        usage="%(prog)s entry-ids.csv results.csv"
    )
    parser.add_argument('input_filepath', help='Path to CSV of entry ids')
    parser.add_argument('--output_filepath', '-O', default="results.csv", help='Path to output CSVs, will be overwritten')
    parser.set_defaults()
    args = parser.parse_args()

    reader = csv.reader(Path(args.input_filepath).read_text().splitlines())
    expected_header = "Entry Number" 
    header_row = next(reader)
    if len(header_row) == 0:
        print(f"Unable to read file {args.input_filepath}")
        sys.exit(1)

    if header_row[0] != expected_header:
        print(f"Expected header '{expected_header}' not found, got '{header_row}'")
        sys.exit(1)
    
    print(f"Opening {args.output_filepath}")
    
    with Path(args.output_filepath).open('wt') as fh:
        writer = csv.writer(fh)
        main(reader, writer)
