from datetime import datetime
import unittest
import Calendar


# NOTE: ALL THE TESTS HERE ARE FOR THE date_formatter METHOD IN Calendar.py
# Test Strategy : Branch Coverage

class CalendarTestDateFormatter(unittest.TestCase):
    def test_date_formatter_invalid_date(self):
        date = "15 October 2020"
        nav_type = "MONTH"
        with self.assertRaises(AttributeError):
            Calendar.date_formatter(date, nav_type)

    def test_date_formatter_month(self):
        date = "15 October 2020"
        date_inputted = datetime.strptime(date, '%d %B %Y')
        nav_type = "MONTH"
        formatted_date = "2020-10-01 00:00:00"
        self.assertEqual(formatted_date, str(Calendar.date_formatter(date_inputted, nav_type)))

    def test_date_formatter_year(self):
        date = "15 October 2020"
        date_inputted = datetime.strptime(date, '%d %B %Y')
        nav_type = "YEAR"
        formatted_date = "2020-01-01 00:00:00"
        self.assertEqual(formatted_date, str(Calendar.date_formatter(date_inputted, nav_type)))

    def test_date_formatter_no_change(self):
        date = "15 October 2020"
        date_inputted = datetime.strptime(date, '%d %B %Y')
        nav_type = "DAY"
        formatted_date = "2020-10-15 00:00:00"
        self.assertEqual(formatted_date, str(Calendar.date_formatter(date_inputted, nav_type)))
def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(CalendarTestDateFormatter)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)


main()