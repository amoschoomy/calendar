from datetime import datetime
import unittest
from unittest.mock import Mock, patch
import Calendar

class CalendarTestRunCalendar(unittest.TestCase):
    @patch("Calendar.get_calendar_api")
    @patch('builtins.input', lambda *args: 'exit')
    def test_run_calendar_exit(self,api):
        with self.assertRaises(SystemExit):
            Calendar.run_calendar(api)


def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(CalendarTestRunCalendar)
        # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)
main()
