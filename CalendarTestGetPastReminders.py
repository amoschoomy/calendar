from datetime import datetime
import unittest
from unittest.mock import Mock, patch
import Calendar

# NOTE: ALL THE TESTS HERE ARE FOR THE get_past_reminders METHOD IN Calendar.py
# Test Strategy : Path Coverage

class CalendarTestGetPastReminders(unittest.TestCase):
    @patch("Calendar.get_calendar_api")
    def test_get_past_reminders_path1_starttime_wrong_format(self, api):
        # This test for the first path where the starting time is of wrong format
        # therefore ending execution immediately
        start_time = "04 October 2020"
        end_time = "2020-10-15T00:00:00.000000Z"
        with self.assertRaises(ValueError):
            Calendar.get_past_reminders(api, start_time, end_time)

    @patch("Calendar.get_calendar_api")
    def test_get_past_reminders_path2_endtime_wrong_format(self, api):
        # This test for second path where the end time is of wrong format
        # therefore ending execution immediately
        start_time = "2020-10-15T00:00:00.000000Z"
        end_time = "11 October 2020"
        with self.assertRaises(ValueError):
            Calendar.get_past_reminders(api, start_time, end_time)

    @patch("Calendar.get_calendar_api")
    def test_get_past_reminders_path3_starttime_exceeded_endtime(self, api):
        # This test for third path where the start time has exceeded
        # end time therefore ending execution immediately
        end_time = "2020-10-15T00:00:00.000000Z"
        start_time = "2020-10-16T00:00:00.000000Z"
        with self.assertRaises(ValueError):
            Calendar.get_past_reminders(api, start_time, end_time)

    @patch("Calendar.get_calendar_api")
    def test_get_past_reminders_path4_no_event(self, api):
        # This test for 4th path in the method, where
        # no exceptions are raised but the outer for loop
        # is not executed which means no events present
        start_time = "2020-10-10T00:00:00.000000Z"
        end_time = "2020-10-16T00:00:00.000000Z"
        api.events.return_value.list.return_value.execute.return_value = {}
        reminders = Calendar.get_past_reminders(api, start_time, end_time)
        self.assertEqual(
            api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(reminders, "")

    @patch("Calendar.get_calendar_api")
    def test_get_past_reminders_path5_default_reminder(self, api):
        # This test for the 5th path in the method, where no exceptions
        # are raised, the outer for loop is executed and the if branch is
        # executed
        start_time = "2020-10-10T00:00:00.000000Z"
        end_time = "2020-10-16T00:00:00.000000Z"
        api.events.return_value.list.return_value.execute.return_value = {
            "items": [
                {
                    "summary": "test",
                    "start": {
                        "dateTime": "2020-10-10T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2020-10-11T02:45:00.000000Z"
                    }, "reminders": {
                    'useDefault': True,
                    'overrides': [

                    ]
                },
                },

            ]}
        reminders = Calendar.get_past_reminders(api, start_time, end_time)
        self.assertEqual(
            api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(reminders, "test,Reminder through popup 10 minutes before event starts\n")

    @patch("Calendar.get_calendar_api")
    def test_get_past_reminders_path6_two_custom_reminders_set(self, api):
        # This test for the 6th path where no exceptions
        # are raised, the outer for loop is executed and the else branch is
        # executed and the for loop inside the else branch
        # is executed
        start_time = "2020-10-10T00:00:00.000000Z"
        end_time = "2020-10-16T00:00:00.000000Z"
        api.events.return_value.list.return_value.execute.return_value = {
            "items": [
                {
                    "summary": "test",
                    "start": {
                        "dateTime": "2020-10-10T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2020-10-14T02:45:00.000000Z"
                    }, "reminders": {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 2},
                        {'method': 'popup', 'minutes': 1},
                    ], },
                },

            ]}
        reminders = Calendar.get_past_reminders(api, start_time, end_time)
        self.assertEqual(
            api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertIn("email 2", reminders)
        self.assertIn("popup 1", reminders)

    @patch("Calendar.get_calendar_api")
    def test_get_past_reminders_path7_no_reminders_set(self, api):
        # This test for the 6th path where no exceptions
        # are raised, the outer for loop is executed and the else branch is
        # executed and the for loop inside the else branch
        # is executed
        start_time = "2020-10-10T00:00:00.000000Z"
        end_time = "2020-10-16T00:00:00.000000Z"
        api.events.return_value.list.return_value.execute.return_value = {
            "items": [
                {
                    "summary": "test",
                    "start": {
                        "dateTime": "2020-10-10T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2020-10-14T02:45:00.000000Z"
                    }, "reminders": {
                    'useDefault': False,
                    'overrides': [
                    ], },
                },

            ]}
        reminders = Calendar.get_past_reminders(api, start_time, end_time)
        self.assertEqual(
            api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual("\n", reminders)  # A new line is returned since the outer for loopm is executed
def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(CalendarTestGetPastReminders)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)


main()