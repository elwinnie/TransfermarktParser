import csv
from pathlib import Path
from dataclasses import dataclass, asdict


class DataExporter:
    _DATA_PATH = Path("data")
    _CSV_EXT = ".csv"

    def to_csv(self, data: list[dataclass], filename: str, timestamp: str | None = None, mode='w') -> None:
        if timestamp:
            filename += timestamp + self._CSV_EXT
        else:
            filename += self._CSV_EXT
        with open(self._DATA_PATH / filename, mode, encoding="utf-8") as ouf:
            csv_writer = csv.writer(ouf)
            columns = asdict(data[0]).keys()
            csv_writer.writerow(columns)
            for row in data:
                row = asdict(row).values()
                csv_writer.writerow(row)
