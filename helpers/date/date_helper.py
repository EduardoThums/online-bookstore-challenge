from datetime import datetime, timedelta


class DateHelper:

    @staticmethod
    def now() -> datetime:
        return datetime.now()

    @staticmethod
    def add_to(date: datetime, days: int = 0) -> datetime:
        return date + timedelta(days=days)

    @staticmethod
    def create(year: int, month: int, day: int, hour: int = 0, minute: int = 0, second: int = 0) -> datetime:
        return datetime(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=second
        )

    @staticmethod
    def serialize(date: datetime) -> str:
        datestr = date.isoformat()

        if '+' in datestr:
            datestr = datestr.split('+')[0]

        return datestr
