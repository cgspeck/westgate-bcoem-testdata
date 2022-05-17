from csv import DictReader
from pathlib import Path

dr = DictReader(Path('data_sources/Street_Name_Labels.csv').read_text().split("\n"))

header_out = ["Street Name"]
memo = set()

for row in dr:
    memo.add(row["NAME"].replace("  ", " ").title())

Path('data/street_names.csv').write_text("\n".join([m for m in memo if len(m) > 6]))
