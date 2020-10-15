import unittest
from unittest.mock import Mock, patch
import Calendar

# NOTE: ALL THE TESTS HERE ARE FOR THE delete_reminders METHOD IN Calendar.py
# Test Strategy : Branch Coverage

class CalendarTestDeleteReminders(unittest.TestCase):

    @patch("Calendar.get_calendar_api")
    def test_none_event(self, api):
        event = None
        with self.assertRaises(TypeError):
            Calendar.delete_reminders(api, event, -1)

    @patch("Calendar.get_calendar_api")
    def test_none_reminder_index(self, api):
        event = {
            'id': "test123",
            'reminders': {"useDefault": False, "overrides": [
                {'method': 'email', 'minutes': 1},
                {'method': 'popup', 'minutes': 10},
            ]}
        }
        with self.assertRaises(TypeError):
            Calendar.delete_reminders(api, event, None)

    @patch("Calendar.get_calendar_api")
    def test_reminder_index_out_of_bounds(self, api):
        event = {
            'id': "test123",
            'reminders': {"useDefault": False, "overrides": [
                {'method': 'email', 'minutes': 1},
                {'method': 'popup', 'minutes': 10},
            ]}
        }

        with self.assertRaises(IndexError):
            Calendar.delete_reminders(api, event, 5)

    def test_reminder_deleted(self):
        event = {
            'id': "test123",
            'reminders': {"useDefault": False, "overrides": [
                {'method': 'email', 'minutes': 1},
                {'method': 'popup', 'minutes': 10},
            ]}
        }

        api = Mock()
        api.events.return_value.update.return_value.execute.return_value = {
            'id': "test123",
            'reminders': {"useDefault": False, "overrides": [
                {'method': 'email', 'minutes': 1}
            ]},
            'updated': "2020-10-10T23:20:50.52Z"
        }

        result = Calendar.delete_reminders(api, event, 1)
        self.assertEqual(api.events.return_value.update.return_value.execute.call_count, 1)
        self.assertTrue(result)

    def test_reminder_deleted_default(self):
        event = {
            'id': "test123",
            'reminders': {"useDefault": True, "overrides": []}
        }

        api = Mock()
        api.events.return_value.update.return_value.execute.return_value = {
            'id': "test123",
            'reminders': {"useDefault": False, "overrides": []},
            'updated': "2020-10-10T23:20:50.52Z"
        }

        result = Calendar.delete_reminders(api, event)
        self.assertEqual(api.events.return_value.update.return_value.execute.call_count, 1)
        self.assertTrue(result)


def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(CalendarTestDeleteReminders)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)


main()
