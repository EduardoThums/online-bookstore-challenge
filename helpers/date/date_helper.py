from datetime import datetime


class DateHelper:

    @staticmethod
    def now() -> datetime:
        return datetime.now()

    @staticmethod
    def serialize(date: datetime) -> str:
        datestr = date.isoformat()

        if '+' in datestr:
            datestr = datestr.split('+')[0]

        return datestr
