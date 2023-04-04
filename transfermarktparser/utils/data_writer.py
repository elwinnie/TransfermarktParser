import csv
import datetime
from pathlib import Path
from dataclasses import dataclass, asdict


class DataWriter:
    _DATA_PATH = Path("data")

    def to_csv(self, data: list[dataclass], filename: str, use_timestamp: bool = True) -> None:
        if use_timestamp:
            timestamp = datetime.datetime.now()
            filename += f"_{timestamp.strftime('%d_%m_%Y_%H_%M')}"
        filename += ".csv"
        with open(self._DATA_PATH / filename, 'w', encoding="utf-8") as ouf:
            csv_writer = csv.writer(ouf)
            columns = asdict(data[0]).keys()
            csv_writer.writerow(columns)
            for row in data:
                row = asdict(row).values()
                csv_writer.writerow(row)
