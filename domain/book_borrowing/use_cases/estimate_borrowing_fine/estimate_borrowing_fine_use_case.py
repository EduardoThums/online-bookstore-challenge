from datetime import datetime

from domain.base.use_cases.base_use_case import BaseUseCase
from helpers.date.date_helper import DateHelper

_FINE_UNTIL_THREE_DAYS = 0.03
_FINE_ABOVE_THREE_DAYS = 0.05
_FINE_ABOVE_FIVE_DAYS = 0.07

_INTEREST_PER_DAY_UNTIL_THREE_DAYS = 0.002
_INTEREST_PER_DAY_ABOVE_THREE_DAYS = 0.004
_INTEREST_PER_DAY_ABOVE_FIVE_DAYS = 0.006


class EstimateBorrowingFineUseCase(BaseUseCase):

    def __init__(self, borrow_date: datetime, book_cost: float):
        self.borrow_date = borrow_date
        self.book_cost = book_cost

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
            interest_per_day = difference_in_days * _INTEREST_PER_DAY_UNTIL_THREE_DAYS

        elif 3 < difference_in_days <= 5:
            fine_percent = _FINE_ABOVE_THREE_DAYS
            interest_per_day = difference_in_days * _INTEREST_PER_DAY_ABOVE_THREE_DAYS

        else:
            fine_percent = _FINE_ABOVE_FIVE_DAYS
            interest_per_day = difference_in_days * _INTEREST_PER_DAY_ABOVE_FIVE_DAYS

        self.total_fine = (self.book_cost * fine_percent) * interest_per_day
