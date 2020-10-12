import unittest
from unittest.mock import Mock, patch
import Calendar


class TestCalendarGetSelectedEvents(unittest.TestCase):

    @patch('Calendar.input', create=True)
    def test_get_selected_events_value_error(self, mocked_input):
        mocked_input.side_effect = ["abc"]
        results = [
            {
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
            },
            {
                "summary": "test2",
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
        ]

        userselect = Calendar.get_selected_event(results)
        self.assertIsNone(userselect)

    @patch('Calendar.input', create=True)
    def test_get_selected_events_key_error(self,mocked_input):

        mocked_input.side_effect = ["25"]
        results = [
            {
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
            },
            {
                "summary": "test2",
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
        ]

        userselect = Calendar.get_selected_event(results)
        self.assertIsNone(userselect)

    @patch('Calendar.input', create=True)
    def test_get_selected_events_correct_input(self, mocked_input):
        mocked_input.side_effect = ["1"]
        results = [
            {
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
            },
            {
                "summary": "test2",
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
        ]

        userselect = Calendar.get_selected_event(results)
        self.assertIsNotNone(userselect)
        self.assertEqual(userselect,results[1])

