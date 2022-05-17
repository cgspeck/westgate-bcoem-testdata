from csv import DictReader
from pathlib import Path

dr = DictReader(Path('data_sources/victorian_postcodes.csv').read_text().split("\n"))

memo = set()


[memo.add((row["locality"].title(), row["postcode"])) for row in dr if row["type"] == "Delivery Area"]

Path('data/postcodes.csv').write_text("\n".join([f"{m[0]}, {m[1]}" for m in memo]))
