import unittest
from unittest.mock import Mock, patch
import Calendar


class CalenderTestSearchEvents(unittest.TestCase):
    @patch("Calendar.get_calendar_api")
    def test_none_event_query(self, api):
        query = None

        with self.assertRaises(TypeError):
            Calendar.get_searched_events(api, query)

    @patch("Calendar.get_calendar_api")
    def test_empty_event_query(self, api):
        query = ""

        with self.assertRaises(ValueError):
            Calendar.get_searched_events(api, query)

        query = " "

        with self.assertRaises(ValueError):
            Calendar.get_searched_events(api, query)

    def test_no_events(self):
        query = "John"

        api = Mock()
        api.events.return_value.list.return_value.execute.return_value = {}

        events = Calendar.get_searched_events(api, query)
        self.assertEqual(events, "")

    def test_events_found(self):
        query = "testing this string"

        api = Mock()
        api.events.return_value.list.return_value.execute.return_value = {
            "items": [
                {
                    "summary": query,
                    "description": "ok",
                    "start": {
                        "dateTime": "2020-06-10T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2020-06-10T02:45:00.000000Z"
                    },
                },
                {
                    "summary": "Hello World",
                    "description": query,
                    "start": {
                        "dateTime": "2020-06-10T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2020-06-10T02:45:00.000000Z"
                    },
                },
            ]}

        searched_events = Calendar.get_searched_events(api, query)
        self.assertEqual(api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertIn(query, searched_events)


def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(CalenderTestSearchEvents)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)


main()