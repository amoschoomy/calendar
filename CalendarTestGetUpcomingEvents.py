from datetime import datetime
import unittest
from unittest.mock import Mock, patch
import Calendar

# NOTE: ALL THE TESTS HERE ARE FOR THE get_upcoming_events METHOD IN Calendar.py
# Test Strategy : Branch Coverage

class CalendarTestGetUpcomingEvents(unittest.TestCase):
    # Test Suite for User Story 1

    def test_get_upcoming_events_invalid_date(self):
        #This test for the if statement branch for date validity

        ex_time = "January 1 2020"  # Date is of an invalid date so will throw Value Error
        mock_api = Mock()  # Mock api
        with self.assertRaises(ValueError):
            Calendar.get_upcoming_events(mock_api, ex_time)

    @patch("Calendar.get_calendar_api")
    def test_get_upcoming_events_valid_date(self, api):
        #This test for the succesful branch of if statement of date validity

        ex_time = "2020-08-03T00:00:00.000000Z"  # Valid date is given
        events = Calendar.get_upcoming_events(api, ex_time)
        #Mock api return value of calendar. Will return one event
        api.events.return_value.list.return_value.execute.return_value = {
            "items": [
                {
                    "summary": "test",
                    "start": {
                        "dateTime": "2020-10-03T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2020-10-03T02:45:00.000000Z"
                    },
                },

            ]}
        self.assertEqual(
            api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(Calendar.get_upcoming_events(api, ex_time), "test,2020-10-03T02:00:00.000000Z\n")

    @patch("Calendar.get_calendar_api")
    def test_get_upcoming_events_non_empty_events(self, api):
        #This test is to test getting upcoming events but for non empty events(for loop is executed) """
        ex_time = "2020-10-03T00:00:00.000000Z"
        api.events.return_value.list.return_value.execute.return_value = {
            "items": [
                {
                    "summary": "test",
                    "start": {
                        "dateTime": "2020-10-03T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2020-10-03T02:45:00.000000Z"
                    },
                },

            ]}
        upcoming_events = Calendar.get_upcoming_events(api, ex_time)
        self.assertEqual(
            api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(upcoming_events, "test,2020-10-03T02:00:00.000000Z\n")

def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(CalendarTestGetUpcomingEvents)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)


main()