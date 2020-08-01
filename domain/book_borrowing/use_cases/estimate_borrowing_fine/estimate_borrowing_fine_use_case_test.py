from unittest import TestCase
from unittest.mock import patch

from domain.book_borrowing.use_cases.estimate_borrowing_fine.estimate_borrowing_fine_use_case import \
    EstimateBorrowingFineUseCase
from helpers.date.date_helper import DateHelper


class TestEstimateBorrowingFineUseCase(TestCase):

    def test_estimate_with_date_under_borrow_deadline_should_not_charge_fine(self):
        use_case = EstimateBorrowingFineUseCase(
            borrow_date=DateHelper.now()
        )
        use_case.exec()

        self.assertFalse(use_case.total_fine)

    def test_estimate_with_borrow_deadline_on_third_day_should_charge_fine(self):
        borrow_date = DateHelper.create(
            year=2020,
            month=8,
            day=1
        )

        fake_today = DateHelper.create(
            year=2020,
            month=8,
            day=7
        )

        with patch.object(DateHelper, 'now', return_value=fake_today):
            use_case = EstimateBorrowingFineUseCase(
                borrow_date=borrow_date
            )
            use_case.exec()

            self.assertEqual(3.6, use_case.total_fine)

    def test_estimate_with_borrow_deadline_on_fifth_day_should_charge_fine(self):
        borrow_date = DateHelper.create(
            year=2020,
            month=8,
            day=1
        )

        fake_today = DateHelper.create(
            year=2020,
            month=8,
            day=9
        )

        with patch.object(DateHelper, 'now', return_value=fake_today):
            use_case = EstimateBorrowingFineUseCase(
                borrow_date=borrow_date
            )
            use_case.exec()

            self.assertEqual(6.4, use_case.total_fine)

    def test_estimate_with_borrow_deadline_on_seventh_day_should_charge_fine(self):
        borrow_date = DateHelper.create(
            year=2020,
            month=8,
            day=1
        )

        fake_today = DateHelper.create(
            year=2020,
            month=8,
            day=11
        )

        with patch.object(DateHelper, 'now', return_value=fake_today):
            use_case = EstimateBorrowingFineUseCase(
                borrow_date=borrow_date
            )
            use_case.exec()

            self.assertEqual(9.6, use_case.total_fine)
