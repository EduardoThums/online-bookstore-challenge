from datetime import datetime, timedelta


class DateHelper:

    @staticmethod
    def now() -> datetime:
        return datetime.now()

    @staticmethod
    def add_to(date: datetime, days: int = 0) -> datetime:
        return date + timedelta(days=days)

    @staticmethod
    def serialize(date: datetime) -> str:
        datestr = date.isoformat()

        if '+' in datestr:
            datestr = datestr.split('+')[0]

        return datestr
