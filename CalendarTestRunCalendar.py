from datetime import datetime
import unittest
from unittest.mock import Mock, patch
import Calendar
import sys
from io import StringIO

class CalendarTestRunCalendar(unittest.TestCase):
    @patch("Calendar.get_calendar_api")
    @patch('sys.stdout',new_callable=StringIO)
    @patch('Calendar.input', create=True)
    def test_run_calendar_help(self,mocked_input,mocked_output,api):
        mocked_input.side_effect=["help","exit"]
        Calendar.run_calendar(api)
        #Special string printed when user ask for help
        self.assertIn("Contact devs at acho0057@student.monash.edu for further help",mocked_output.getvalue())
    
    @patch("Calendar.get_calendar_api")
    @patch('sys.stdout',new_callable=StringIO)
    @patch('Calendar.input', create=True)
    def test_run_calendar_invalid_command(self,mocked_input,mocked_output,api):
        mocked_input.side_effect=["test","exit"]
        Calendar.run_calendar(api)
        #Special string printed when user ask for help
        self.assertIn("Invalid command. Please try again!",mocked_output.getvalue())
    
def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(CalendarTestRunCalendar)
        # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)
main()
