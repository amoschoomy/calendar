from datetime import datetime
import unittest
from unittest.mock import Mock, patch
import Calendar

# NOTE: ALL THE TESTS HERE ARE FOR THE get_detailed_remidner METHOD IN Calendar.py
# Test Strategy : Branch Coverage

class CalendarTestGetDetailedReminders(unittest.TestCase):
    def test_get_detailed_reminders_raise_value_error(self):
        event = {
            'irrelevant': "nonsense"

        }
        with self.assertRaises(ValueError):
            Calendar.get_detailed_reminders(event)

    def test_get_detailed_reminders_path2_two_custom_reminders(self):
            
        #below is an example of json string returned
        event = {
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
        }
        reminders = Calendar.get_detailed_reminders(event)
        self.assertIn("email 1", reminders) #Assert reminders detail is returned
        self.assertIn("popup 10", reminders) #Assert reminders detail is returned

    def test_get_detailed_reminders_path3_no_reminder_set(self):
        event = {
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
        }

        reminders = Calendar.get_detailed_reminders(event)
        self.assertEqual(reminders, "\n")  # A newline is returned due to the outer for loop being executed

    def test_get_detailed_reminders_path4_default_reminder(self):
        # Path 5 where if statement to check date validity succeeds, outer for loop is executed, and if
        # branch is executed which is default reminders
        event = {
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
        }
        reminders = Calendar.get_detailed_reminders(event)
        self.assertEqual(reminders, "test,Reminder through popup 10 minutes before event starts\n")
        #String for default reminders

def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(CalendarTestGetDetailedReminders)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)


main()