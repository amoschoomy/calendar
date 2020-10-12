import unittest
from unittest.mock import Mock, patch
import Calendar
from io import StringIO

class CalendarTestGetSelectedReminders(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    @patch('Calendar.input', create=True)
    def test_get_selected_reminders_value_error(self,mocked_input,mocked_output):
        mocked_input.side_effect = ["abc"]
        event = {
            "summary": "test1",
            "start": {
                "dateTime": "2020-10-03T02:00:00.000000Z"
            },
            "end": {
                "dateTime": "2020-10-03T02:45:00.000000Z"
            }, "reminders": {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 1},
                    {'method': 'popup', 'minutes': 10},
                ]}
        }

        userselect = Calendar.get_selected_reminders(event)
        self.assertIsNone(userselect)
        self.assertNotIn("Selected reminder:", mocked_output.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    @patch('Calendar.input', create=True)
    def test_get_selected_reminders_key_error(self, mocked_input,mocked_output):
        mocked_input.side_effect = ["25"]
        event = {
            "summary": "test1",
            "start": {
                "dateTime": "2020-10-03T02:00:00.000000Z"
            },
            "end": {
                "dateTime": "2020-10-03T02:45:00.000000Z"
            }, "reminders": {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 1},
                    {'method': 'popup', 'minutes': 10},
                ]}
        }

        userselect = Calendar.get_selected_reminders(event)
        self.assertIsNone(userselect)
        self.assertNotIn("Selected reminder:", mocked_output.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    @patch('Calendar.input', create=True)
    def test_get_selected_reminders_correct_input(self,mocked_input,mocked_output):
        mocked_input.side_effect = ["1"]
        event = {
            "summary": "test1",
            "start": {
                "dateTime": "2020-10-03T02:00:00.000000Z"
            },
            "end": {
                "dateTime": "2020-10-03T02:45:00.000000Z"
            }, "reminders": {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 1},
                    {'method': 'popup', 'minutes': 10},
                ]}
        }

        userselect = Calendar.get_selected_reminders(event)
        self.assertIsNotNone(userselect)
        self.assertEqual(1,userselect)
        self.assertIn("Selected reminder: Reminder through popup 10 minutes before event starts",mocked_output.getvalue())

    @patch('Calendar.input', create=True)
    def test_get_selected_reminders_default(self, mocked_input):
        mocked_input.side_effect = ["1"]
        event = {
            "summary": "test1",
            "start": {
                "dateTime": "2020-10-03T02:00:00.000000Z"
            },
            "end": {
                "dateTime": "2020-10-03T02:45:00.000000Z"
            }, "reminders": {
                'useDefault': True,
                'overrides': [
                    {'method': 'email', 'minutes': 1},
                    {'method': 'popup', 'minutes': 10},
                ]}
        }

        userselect = Calendar.get_selected_reminders(event)
        self.assertIsNotNone(userselect)
        self.assertEqual(-1, userselect)