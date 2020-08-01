from datetime import datetime

from domain.base.use_cases.base_use_case import BaseUseCase
from helpers.date.date_helper import DateHelper

_FINE_UNTIL_THREE_DAYS = 3
_FINE_ABOVE_THREE_DAYS = 5
_FINE_ABOVE_FIVE_DAYS = 7

_INTEREST_PER_DAY_UNTIL_THREE_DAYS = 0.2
_INTEREST_PER_DAY_ABOVE_THREE_DAYS = 0.4
_INTEREST_PER_DAY_ABOVE_FIVE_DAYS = 0.6


class EstimateBorrowingFineUseCase(BaseUseCase):

    def __init__(self, borrow_date: datetime):
        self.borrow_date = borrow_date

        self.total_fine = 0

    def exec(self):
        today = DateHelper.now()
        borrow_deadline = DateHelper.add_to(self.borrow_date, days=3)

        if today <= borrow_deadline:
            return 0

        difference = today - borrow_deadline
        difference_in_days = difference.days

        if difference_in_days <= 3:
            fine_percent = _FINE_UNTIL_THREE_DAYS
            interest_per_day = self._calculate_interests_until_third_day(difference_in_days)

        elif 3 < difference_in_days <= 5:
            difference_in_days -= 3

            interest_per_day = self._calculate_interests_until_third_day(difference_in_days=3)
            interest_per_day += self._calculate_interests_above_third_day(difference_in_days)

            fine_percent = _FINE_ABOVE_THREE_DAYS
        else:
            difference_in_days -= 5

            interest_per_day = self._calculate_interests_until_third_day(difference_in_days=3)
            interest_per_day += self._calculate_interests_above_third_day(difference_in_days=2)
            interest_per_day += self._calculate_interests_above_fifth_day(difference_in_days)

            fine_percent = _FINE_ABOVE_FIVE_DAYS

        self.total_fine = fine_percent + interest_per_day

    @staticmethod
    def _calculate_interests_until_third_day(difference_in_days: int) -> float:
        return difference_in_days * _INTEREST_PER_DAY_UNTIL_THREE_DAYS

    @staticmethod
    def _calculate_interests_above_third_day(difference_in_days: int) -> float:
        return difference_in_days * _INTEREST_PER_DAY_ABOVE_THREE_DAYS

    @staticmethod
    def _calculate_interests_above_fifth_day(difference_in_days: int) -> float:
        return difference_in_days * _INTEREST_PER_DAY_ABOVE_FIVE_DAYS
