from datetime import datetime

from bs4 import Tag


class TextHandler:
    @staticmethod
    def parse_date(date: str) -> datetime.date:
        format_date = "%m/%d/%y"
        if date:
            date = datetime.strptime(date, format_date).date()
            return date
        return None

    @staticmethod
    def parse_time(time: str) -> datetime.time:
        format_time = "%I:%M %p"
        if time and 'unknown' not in time.lower():
            time = datetime.strptime(time, format_time).time()
            return time
        return None
