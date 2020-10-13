from datetime import datetime
import unittest
from unittest.mock import Mock, patch
import Calendar

class CalendarTestGetPastEvents(unittest.TestCase):
    """Test Suite for Getting Past Events"""

    def test_get_past_events_invalid_past_date_format(self):
        #Invalid start date format, branch of date validation throws ValueError executed"""

        past_time = "03 October 2020"
        time_now = "2020-10-03T00:00:00.000000Z"
        api = Mock()
        with self.assertRaises(ValueError):
            Calendar.get_past_events(api, past_time, time_now)

    def test_get_past_events_invalid_end_date_format(self):
        #Invalid start date format, branch of date validation throws ValueError executed"""

        past_time = "2020-10-03T00:00:00.000000Z"
        time_now = "15 October 2020"
        api = Mock()
        with self.assertRaises(ValueError):
            Calendar.get_past_events(api, past_time, time_now)

    def test_get_past_events_exceeded_date(self):
        #Past date has exceeded start date, branch of date validation of time comparison executed"""
        past_time = "2020-10-03T00:00:00.000000Z"
        time_now = "2020-01-03T00:00:00.000000Z"
        api = Mock()
        with self.assertRaises(ValueError):
            Calendar.get_past_events(api, past_time, time_now)

    @patch("Calendar.get_calendar_api")
    def test_get_past_events_same_date(self, api):
        #Same date in calendar test, boundary of ending time is the same as past time"""
        past_time = "2020-10-03T00:00:00.000000Z"
        time_now = "2020-10-03T00:00:00.000000Z"

        # If its the same date and time, only events of start and end at same time can be returned
        api.events.return_value.list.return_value.execute.return_value = {
            "items": [
                {
                    "summary": "test",
                    "start": {
                        "dateTime": "2020-10-03T00:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2020-10-03T00:00:00.000000Z"
                    },
                },

            ]}
        past_events = Calendar.get_past_events(api, past_time, time_now)
        self.assertEqual(
            api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(past_events, "test,2020-10-03T00:00:00.000000Z\n")

    @patch("Calendar.get_calendar_api")
    def test_get_past_events_valid_date_and_time(self, api):
        # Test for the other branch of date format validity in the if statement
        # No exceptions will be raised
        past_time = "2020-10-03T00:00:00.000000Z"
        time_now = "2020-10-15T00:00:00.000000Z"
        api.events.return_value.list.return_value.execute.return_value = {
            "items": [
                {
                    "summary": "test",
                    "start": {
                        "dateTime": "2020-10-07T00:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2020-10-09T00:00:00.000000Z"
                    },
                },

            ]}
        past_events = Calendar.get_past_events(api, past_time, time_now)
        self.assertEqual(
            api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(past_events, "test,2020-10-07T00:00:00.000000Z\n")

    @patch("Calendar.get_calendar_api")
    def test_get_past_events_empty_events(self, api):
        # Test for non execution of the for loop when retrieving event list
        # Which means no events found in that time frame
        past_time = "2020-10-03T00:00:00.000000Z"
        time_now = "2020-10-15T00:00:00.000000Z"
        api.events.return_value.list.return_value.execute.return_value = {}
        past_events = Calendar.get_past_events(api, past_time, time_now)
        self.assertEqual(
            api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(past_events, "")

    @patch("Calendar.get_calendar_api")
    def test_get_past_events_non_empty_events(self, api):
        #   Test for non empty events
        past_time = "2020-10-03T00:00:00.000000Z"
        time_now = "2020-10-15T00:00:00.000000Z"
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
                {
                    "summary": "Hello World",
                    "start": {
                        "dateTime": "2020-10-07T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2020-10-14T02:45:00.000000Z"
                    },
                },

            ]}
        past_events = Calendar.get_past_events(api, past_time, time_now)
        self.assertEqual(
            api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertIn("test", past_events)
        self.assertIn("Hello World", past_events)

def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(CalendarTestGetPastEvents)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)


main()
