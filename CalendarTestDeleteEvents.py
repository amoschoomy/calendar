import unittest
from unittest.mock import Mock, patch
import Calendar

class CalendarTestDeleteEvents(unittest.TestCase):

    @patch("Calendar.get_calendar_api")
    def test_none_event_id(self, api):
        event = None
        with self.assertRaises(TypeError):
            Calendar.delete_events(api, event)

    @patch("Calendar.get_calendar_api")
    def test_empty_event_id(self, api):
        event = {}
        with self.assertRaises(ValueError):
            Calendar.delete_events(api, event)

        event = {}
        with self.assertRaises(ValueError):
            Calendar.delete_events(api, event)

    def test_events_deleted(self):
        api = Mock()
        event = {"id": "test123"}
        Calendar.delete_events(api, event)
        self.assertEqual(api.events.return_value.delete.return_value.execute.call_count, 1)



def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(CalendarTestDeleteEvents)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)


main()