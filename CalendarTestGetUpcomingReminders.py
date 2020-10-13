from datetime import datetime
import unittest
from unittest.mock import Mock, patch
import Calendar
class CalendarTestGetUpcomingReminders(unittest.TestCase):
    def test_get_upcoming_reminders_invalid_date(self):
        # Path 1 where execution stops after invalid date given
        ex_time = "January 1 2020"  # Date is of an invalid date so will throw Value Error
        mock_api = Mock()  # Mock api
        with self.assertRaises(ValueError):
            Calendar.get_upcoming_reminders(mock_api, ex_time)

    @patch("Calendar.get_calendar_api")
    def test_get_upcoming_reminders_path2_two_custom_reminders(self, api):
        # Path 2 where the if statement of date validation succeeds, outer for loop is executed, else branch is executed
        # inside the loop, and from there the for loop in else branch is executed
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
                    }, "reminders": {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 1},
                        {'method': 'popup', 'minutes': 10},
                    ], },
                },

            ]}
        reminders = Calendar.get_upcoming_reminders(api, ex_time)
        # Two seperate assertion checks for each method of reminder is present in method output
        self.assertEqual(
            api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertIn("email 1", reminders)
        self.assertIn("popup 10", reminders)

    @patch("Calendar.get_calendar_api")
    def test_get_upcoming_reminders_path3_no_event(self, api):
        # Path 3 where the if branch of date validity succeeded, the outer for loop doesn't get executed.
        ex_time = "2020-10-03T00:00:00.000000Z"
        api.events.return_value.list.return_value.execute.return_value = {}
        reminders = Calendar.get_upcoming_reminders(api, ex_time)
        self.assertEqual(
            api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(reminders, "")

    @patch("Calendar.get_calendar_api")
    def test_get_upcoming_reminders_path4_no_reminder_set(self, api):
        # Path 4 where if branch of date validity succeeded, outer for loop is executed, else branch is executed but the for
        # loop in else branch is not executed
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
                    }, "reminders": {
                    'useDefault': False,
                    'overrides': [
                    ], },
                },

            ]}
        reminders = Calendar.get_upcoming_reminders(api, ex_time)
        self.assertEqual(
            api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(reminders, "\n")  # A newline is returned due to the outer for loop being executed

    @patch("Calendar.get_calendar_api")
    def test_get_upcoming_reminders_path5_default_reminder(self, api):
        # Path 5 where if statement to check date validity succeeds, outer for loop is executed, and if
        # branch is executed which is default reminders
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
                    }, "reminders": {
                    'useDefault': True,
                    'overrides': [
                    ], },
                },

            ]}
        reminders = Calendar.get_upcoming_reminders(api, ex_time)
        self.assertEqual(
            api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(reminders, "test,Reminder through popup 10 minutes before event starts\n")
def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(CalendarTestGetUpcomingReminders)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)


main()