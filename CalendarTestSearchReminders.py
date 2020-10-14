import unittest
from unittest.mock import Mock, patch
import Calendar


class CalenderTestSearchReminders(unittest.TestCase):

    @patch("Calendar.get_calendar_api")
    def test_none_reminder_query(self, api):
        query = None

        with self.assertRaises(TypeError):
            Calendar.get_searched_reminders(api, query)

    @patch("Calendar.get_calendar_api")
    def test_empty_reminder_query(self, api):
        query = ""

        with self.assertRaises(ValueError):
            Calendar.get_searched_reminders(api, query)

        query = " "

        with self.assertRaises(ValueError):
            Calendar.get_searched_reminders(api, query)

    def test_no_reminders(self):
        api = Mock()
        api.events.return_value.list.return_value.execute.return_value = {}

        query = "John"

        reminders = Calendar.get_searched_reminders(api, query)
        self.assertEqual(reminders, "")

    def test_reminders_found(self):
        query = "testing this string"

        api = Mock()
        api.events.return_value.list.return_value.execute.return_value = {
            "items": [
                {
                    "summary": query,
                    "reminders": {
                        'useDefault': False,
                        'overrides': [
                            {'method': 'email', 'minutes': 1},
                            {'method': 'popup', 'minutes': 10},
                        ], },
                },
            ]}

        reminders = Calendar.get_searched_reminders(api, query)
        self.assertEqual(api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertIn("email 1", reminders)
        self.assertIn("popup 10", reminders)

    def test_reminders_found_default(self):
        query = "testing this string"
        api = Mock()
        api.events.return_value.list.return_value.execute.return_value = {
            "items": [
                {
                    "summary": query,
                    "reminders": {
                        'useDefault': True,
                        'overrides': [], },
                },

            ]}

        reminders = Calendar.get_searched_reminders(api, query)
        self.assertEqual(api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(reminders, query + ",Reminder through popup 10 minutes before event starts\n")


def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(CalenderTestSearchReminders)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)


main()