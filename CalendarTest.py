from datetime import datetime
import unittest
from unittest.mock import Mock, patch
import Calendar


# Add other imports here if needed
class CalendarTestGetUpcomingEvents(unittest.TestCase):
    # Test Suite for User Story 1

    def test_get_upcoming_events_invalid_date(self):
        """This test for the if statement branch for date validity"""

        ex_time = "January 1 2020"  # Date is of an invalid date so will throw Value Error
        mock_api = Mock()  # Mock api
        with self.assertRaises(ValueError):
            Calendar.get_upcoming_events(mock_api, ex_time)

    @patch("Calendar.get_calendar_api")
    def test_get_upcoming_events_valid_date(self, api):
        """This test for the succesful branch of if statement of date validity
            A patched call to calendar api is mocked
        """

        ex_time = "2020-08-03T00:00:00.000000Z"  # Valid date is given
        events = Calendar.get_upcoming_events(api, ex_time)
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

            ]}
        self.assertEqual(
            api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(Calendar.get_upcoming_events(api, ex_time), "test,2020-10-03T02:00:00.000000Z\n")

    @patch("Calendar.get_calendar_api")
    def test_get_upcoming_events_non_empty_events(self, api):
        """This test is to test getting upcoming events but for non empty events(for loop is executed) """
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
                    },
                },

            ]}
        upcoming_events = Calendar.get_upcoming_events(api, ex_time)
        self.assertEqual(
            api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(upcoming_events, "test,2020-10-03T02:00:00.000000Z\n")


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


class CalendarTestGetPastEvents(unittest.TestCase):
    """Test Suite for Getting Past Events"""

    def test_get_past_events_invalid_past_date_format(self):
        """Invalid start date format, branch of date validation throws ValueError executed"""

        past_time = "03 October 2020"
        time_now = "2020-10-03T00:00:00.000000Z"
        api = Mock()
        with self.assertRaises(ValueError):
            Calendar.get_past_events(api, past_time, time_now)

    def test_get_past_events_invalid_end_date_format(self):
        """Invalid start date format, branch of date validation throws ValueError executed"""

        past_time = "2020-10-03T00:00:00.000000Z"
        time_now = "15 October 2020"
        api = Mock()
        with self.assertRaises(ValueError):
            Calendar.get_past_events(api, past_time, time_now)

    def test_get_past_events_exceeded_date(self):
        """Past date has exceeded start date, branch of date validation of time comparison executed"""
        past_time = "2020-10-03T00:00:00.000000Z"
        time_now = "2020-01-03T00:00:00.000000Z"
        api = Mock()
        with self.assertRaises(ValueError):
            Calendar.get_past_events(api, past_time, time_now)

    @patch("Calendar.get_calendar_api")
    def test_get_past_events_same_date(self, api):
        """Same date in calendar test, boundary of ending time is the same as past time"""
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


class CalendarTestNavigateCalendar(unittest.TestCase):
    @patch("Calendar.get_calendar_api")
    def test_navigate_calendar_path1_invalid_date_format(self, api):
        # invalid date is given as a parameter
        # will throw Attribute Error when trying to get the month,day,year attribute
        date = "12 October 2020"
        with self.assertRaises(AttributeError):
            Calendar.navigate_calendar(api, date, "MONTH")

    @patch("Calendar.get_calendar_api")
    def test_naivgate_calendar_path2_invalid_navigation_type(self, api):
        # Invalid navigation type given as parametter
        # Path where it will raise ValueError and stop execution immediately
        # date="2020-10-09 01:14:28.238512"
        date = datetime.strptime('Oct 15 2020  1:30AM', '%b %d %Y %I:%M%p')
        navigation_type = "CENTURY"
        with self.assertRaises(ValueError):
            Calendar.navigate_calendar(api, date, navigation_type)

    @patch("Calendar.get_calendar_api")
    def test_navigate_calendar_path3_navigation_month_31days(self, api):
        # Navigation path for Month of 31 days
        # Executes the try statement only succesfully
        date = datetime.strptime('Oct 10 2020  1:30AM', '%b %d %Y %I:%M%p')
        navigation_type = "MONTH"
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
                {
                    "summary": "Halloween",
                    "start": {
                        "dateTime": "2020-10-30T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2020-10-31T02:45:00.000000Z"
                    }, "reminders": {
                    'useDefault': True,
                    'overrides': [

                    ]
                },
                },

            ]}
        result = Calendar.navigate_calendar(api, date, navigation_type)
        self.assertEqual(
            api.events.return_value.list.return_value.execute.call_count, 2)  # Mock method called twice
        # First in getting events, second in getting reminders

        self.assertIn("Halloween", result)  # Assert title of calendar in result string returned
        self.assertIn("test", result)  # Assert title of calendar in result string returned
        self.assertIn("popup 10", result)  # Assert reminder in result string returned

    @patch("Calendar.get_calendar_api")
    def test_navigate_calendar_path4_month_30days(self, api):
        date = datetime.strptime('Jun 10 2020  1:30AM', '%b %d %Y %I:%M%p')
        navigation_type = "MONTH"
        api.events.return_value.list.return_value.execute.return_value = {
            "items": [
                {
                    "summary": "test",
                    "start": {
                        "dateTime": "2020-06-10T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2020-06-11T02:45:00.000000Z"
                    }, "reminders": {
                    'useDefault': True,
                    'overrides': [

                    ]
                },
                },
                {
                    "summary": "Birthday Party",
                    "start": {
                        "dateTime": "2020-06-30T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2020-06-30T02:45:00.000000Z"
                    }, "reminders": {
                    'useDefault': True,
                    'overrides': [

                    ]
                },
                },

            ]}
        result = Calendar.navigate_calendar(api, date, navigation_type)
        self.assertEqual(
            api.events.return_value.list.return_value.execute.call_count, 2)  # Mock method called twice
        # First in getting events, second in getting reminders
        self.assertIn("test", result)  # Assert title in result
        self.assertIn("Birthday Party", result)  # Assert title in result
        self.assertIn("popup 10", result)  # Assert reminder in result

    @patch("Calendar.get_calendar_api")
    def test_navigate_calendar_path5_year(self, api):
        date = datetime.strptime('Jun 10 2020  1:30AM', '%b %d %Y %I:%M%p')
        navigation_type = "YEAR"
        api.events.return_value.list.return_value.execute.return_value = {
            "items": [
                {
                    "summary": "test",
                    "start": {
                        "dateTime": "2020-06-10T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2020-06-11T02:45:00.000000Z"
                    }, "reminders": {
                    'useDefault': True,
                    'overrides': [

                    ]
                },
                },
                {
                    "summary": "Birthday Party",
                    "start": {
                        "dateTime": "2020-02-30T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2020-04-30T02:45:00.000000Z"
                    }, "reminders": {
                    'useDefault': True,
                    'overrides': [

                    ]
                },
                },
                {
                    "summary": "New Year Day Countdown",
                    "start": {
                        "dateTime": "2020-30-31T23:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2020-30-31T223:59:00.000000Z"
                    }, "reminders": {
                    'useDefault': True,
                    'overrides': [

                    ]
                },
                },

            ]}
        result = Calendar.navigate_calendar(api, date, navigation_type)
        self.assertEqual(
            api.events.return_value.list.return_value.execute.call_count, 2)  # Mock method called twice
        # First in getting events, second in getting reminders
        self.assertIn("test", result)  # Assert title in result
        self.assertIn("Birthday Party", result)  # Assert title in result
        self.assertIn("New Year Day Countdown", result)  # Assert title in result
        self.assertIn("popup 10", result)  # Assert reminder in result

    @patch("Calendar.get_calendar_api")
    def test_navigate_calendar_path6_day(self, api):
        date = datetime.strptime('Jun 10 2020  1:30AM', '%b %d %Y %I:%M%p')
        navigation_type = "DAY"
        api.events.return_value.list.return_value.execute.return_value = {
            "items": [
                {
                    "summary": "test",
                    "start": {
                        "dateTime": "2020-06-10T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2020-06-10T02:45:00.000000Z"
                    }, "reminders": {
                    'useDefault': True,
                    'overrides': [

                    ]
                },
                },
                {
                    "summary": "Birthday Party",
                    "start": {
                        "dateTime": "2020-06-10T12:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2020-06-10T12:45:00.000000Z"
                    }, "reminders": {
                    'useDefault': True,
                    'overrides': [

                    ]
                },
                },

            ]}
        result = Calendar.navigate_calendar(api, date, navigation_type)
        self.assertEqual(
            api.events.return_value.list.return_value.execute.call_count, 2)  # Mock method called twice
        # First in getting events, second in getting reminders
        self.assertIn("test", result)  # Assert title in result
        self.assertIn("Birthday Party", result)  # Assert title in result
        self.assertIn("popup 10", result)  # Assert reminder in result

    @patch("Calendar.get_calendar_api")
    def test_navigate_calendar_path7_feb_28days(self, api):
        date = datetime.strptime('Feb 28 2017  1:30AM', '%b %d %Y %I:%M%p')
        navigation_type = "MONTH"
        api.events.return_value.list.return_value.execute.return_value = {
            "items": [
                {
                    "summary": "test",
                    "start": {
                        "dateTime": "2017-02-10T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2017-02-11T02:45:00.000000Z"
                    }, "reminders": {
                    'useDefault': True,
                    'overrides': [

                    ]
                },
                },
                {
                    "summary": "Birthday Party",
                    "start": {
                        "dateTime": "2017-02-30T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2017-02-30T02:45:00.000000Z"
                    }, "reminders": {
                    'useDefault': True,
                    'overrides': [

                    ]
                },
                },

            ]}
        result = Calendar.navigate_calendar(api, date, navigation_type)
        self.assertEqual(
            api.events.return_value.list.return_value.execute.call_count, 2)  # Mock method called twice
        # First in getting events, second in getting reminders
        self.assertIn("test", result)  # Assert title in result
        self.assertIn("Birthday Party", result)  # Assert title in result
        self.assertIn("popup 10", result)  # Assert reminder in result

    @patch("Calendar.get_calendar_api")
    def test_navigate_calendar_path7_feb_29days(self, api):
        date = datetime.strptime('Feb 29 2020  1:30AM', '%b %d %Y %I:%M%p')
        navigation_type = "MONTH"
        api.events.return_value.list.return_value.execute.return_value = {
            "items": [
                {
                    "summary": "test",
                    "start": {
                        "dateTime": "2017-02-10T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2017-02-11T02:45:00.000000Z"
                    }, "reminders": {
                    'useDefault': True,
                    'overrides': [

                    ]
                },
                },
                {
                    "summary": "Birthday Party",
                    "start": {
                        "dateTime": "2017-02-30T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2017-02-30T02:45:00.000000Z"
                    }, "reminders": {
                    'useDefault': True,
                    'overrides': [

                    ]
                },
                },

            ]}
        result = Calendar.navigate_calendar(api, date, navigation_type)
        self.assertEqual(
            api.events.return_value.list.return_value.execute.call_count, 2)  # Mock method called twice
        # First in getting events, second in getting reminders
        self.assertIn("test", result)  # Assert title in result
        self.assertIn("Birthday Party", result)  # Assert title in result
        self.assertIn("popup 10", result)  # Assert reminder in result

class CalendarTestGetDetailedEvent(unittest.TestCase):

    def test_get_detailed_event_raise_value_error(self):
        event = {
            'irrelevant':"nonsense"

        }
        with self.assertRaises(ValueError):
            Calendar.get_detailed_event(event)

    def test_get_detailed_event_raise_attribute_error(self):
        event = "FAKE EVENT"
        with self.assertRaises(AttributeError):
            Calendar.get_detailed_event(event)

    def test_get_detailed_event_no_visibility_set_attendees_set_no_location_set(self):
        # This test for the events that have no visibility key aka
        # default visibility
        event = {
            "summary": "Debate",
            "start": {
                "dateTime": "2020-06-10T02:00:00.000000Z"
            },
            "end": {
                "dateTime": "2020-06-10T02:45:00.000000Z"
            }, "reminders": {
                'useDefault': True,
                'overrides': [

                ]
            },
            "status": "confirmed",
            'creator': {'email': 'donaldtrump@gmail.com', 'self': True},
            'created': '2020-10-09T04:10:47.000Z',
            'attendees': [{'email': 'trump@monash.edu', 'responseStatus': 'needsAction'},
                          {'email': 'donald@monash.edu', 'responseStatus': 'needsAction'}],

        }
        detailed_event = Calendar.get_detailed_event(event)
        # Attendees are included in the event but not visiblity or location
        # Asserts the presence of string information of attendees
        self.assertIn("Attendees: trump@monash.edu, donald@monash.edu", detailed_event)

    def test_get_detailed_event_visibility_set_no_attendees_set_no_location_set(self):
        # This test for the events that have no visibility key aka
        # default visibility
        event = {
            "summary": "Debate",
            "start": {
                "dateTime": "2020-06-10T02:00:00.000000Z"
            },
            "end": {
                "dateTime": "2020-06-10T02:45:00.000000Z"
            }, "reminders": {
                'useDefault': True,
                'overrides': [

                ]
            },
            "status": "confirmed",
            'creator': {'email': 'donaldtrump@gmail.com', 'self': True},
            'created': '2020-10-09T04:10:47.000Z',
            'visibility': "private",

        }
        detailed_event = Calendar.get_detailed_event(event)
        # Assert this method output change where visiblity is part of the event
        self.assertIn("Visibility: private", detailed_event)

    def test_get_detailed_event_no_visibility_set_no_attendees_set_location_set(self):
        # This test for the events that have no visibility key aka
        # default visibility
        event = {
            "summary": "Debate",
            "start": {
                "dateTime": "2020-06-10T02:00:00.000000Z"
            },
            "end": {
                "dateTime": "2020-06-10T02:45:00.000000Z"
            }, "reminders": {
                'useDefault': True,
                'overrides': [

                ]
            },
            "status": "confirmed",
            'creator': {'email': 'donaldtrump@gmail.com', 'self': True},
            'created': '2020-10-09T04:10:47.000Z',
            'location': 'Monash University, Wellington Rd, Clayton VIC 3800, Australia',
            'attendees': [{'email': 'trump@monash.edu', 'responseStatus': 'needsAction'},
                          {'email': 'donald@monash.edu', 'responseStatus': 'needsAction'}],

        }
        detailed_event = Calendar.get_detailed_event(event)
        # Assert this  method output change where location is included in the event
        self.assertIn("Location: Monash University, Wellington Rd, Clayton VIC 3800, Australia", detailed_event)

    def test_get_detailed_event_visibility_set_attendees_set_location_set(self):
        # This test for the events that have no visibility key aka
        # default visibility
        event = {
            "summary": "Debate",
            "start": {
                "dateTime": "2020-06-10T02:00:00.000000Z"
            },
            "end": {
                "dateTime": "2020-06-10T02:45:00.000000Z"
            }, "reminders": {
                'useDefault': True,
                'overrides': [

                ]
            },
            "status": "confirmed",
            'creator': {'email': 'donaldtrump@gmail.com', 'self': True},
            'created': '2020-10-09T04:10:47.000Z',
            'visibility': "private",
            'location': 'Monash University, Wellington Rd, Clayton VIC 3800, Australia',
            'attendees': [{'email': 'trump@monash.edu', 'responseStatus': 'needsAction'},
                          {'email': 'donald@monash.edu', 'responseStatus': 'needsAction'}],

        }
        detailed_event = Calendar.get_detailed_event(event)

        # Assert all keys found succesfully and string containing the information is printed
        self.assertIn("Visibility: private", detailed_event)
        self.assertIn("Location: Monash University, Wellington Rd, Clayton VIC 3800, Australia", detailed_event)
        self.assertIn("Attendees: trump@monash.edu, donald@monash.edu", detailed_event)


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


class CalendarTestDeleteEvents(unittest.TestCase):

    @patch("Calendar.get_calendar_api")
    def test_none_event_id(self, api):
        event_id = None
        with self.assertRaises(TypeError):
            Calendar.delete_events(api, event_id)

    @patch("Calendar.get_calendar_api")
    def test_empty_event_id(self, api):
        event_id = " "
        with self.assertRaises(ValueError):
            Calendar.delete_events(api, event_id)

        event_id = ""
        with self.assertRaises(ValueError):
            Calendar.delete_events(api, event_id)

    def test_events_deleted(self):
        api = Mock()

        event_id = "test123"
        Calendar.delete_events(api, event_id)
        self.assertEqual(api.events.return_value.delete.return_value.execute.call_count, 1)


class CalendarTestDeleteReminders(unittest.TestCase):

    @patch("Calendar.get_calendar_api")
    def test_none_event_id(self, api):
        event_id = None
        with self.assertRaises(TypeError):
            Calendar.delete_reminders(api, event_id)

    @patch("Calendar.get_calendar_api")
    def test_empty_event_id(self, api):
        event_id = " "
        with self.assertRaises(ValueError):
            Calendar.delete_reminders(api, event_id)

        event_id = ""
        with self.assertRaises(ValueError):
            Calendar.delete_reminders(api, event_id)

    def test_reminder_deleted(self):
        event_id = "test123"

        api = Mock()
        api.events.return_value.get.return_value.execute.return_value = {
            'id': event_id,
            'reminders': {"useDefault": False, "overrides": [
                            {'method': 'email', 'minutes': 1},
                            {'method': 'popup', 'minutes': 10},
                        ]}
        }
        api.events.return_value.update.return_value.execute.return_value ={
            'id': event_id,
            'reminders': {"useDefault": False, "overrides": []},
            'updated': "2020-10-10T23:20:50.52Z"
        }

        result = Calendar.delete_reminders(api, event_id)
        self.assertEqual(api.events.return_value.get.return_value.execute.call_count, 1)
        self.assertEqual(api.events.return_value.update.return_value.execute.call_count, 1)
        self.assertTrue(result)

class CalendarTestDateFormatter(unittest.TestCase):
    def test_date_formatter_invalid_date(self):
        date="15 October 2020"
        nav_type="MONTH"
        with self.assertRaises(AttributeError):
            Calendar.date_formatter(date,nav_type)
    
    def test_date_formatter_month(self):
        date="15 October 2020"
        date_inputted = datetime.strptime(date, '%d %B %Y')
        nav_type="MONTH"
        formatted_date="2020-10-01 00:00:00"
        self.assertEqual(formatted_date,str(Calendar.date_formatter(date_inputted,nav_type)))
    
    def test_date_formatter_year(self):
        date="15 October 2020"
        date_inputted = datetime.strptime(date, '%d %B %Y')
        nav_type="YEAR"
        formatted_date="2020-01-01 00:00:00"
        self.assertEqual(formatted_date,str(Calendar.date_formatter(date_inputted,nav_type)))
    
    def test_date_formatter_no_change(self):
        date="15 October 2020"
        date_inputted = datetime.strptime(date, '%d %B %Y')
        nav_type="DAY"
        formatted_date="2020-10-15 00:00:00"
        self.assertEqual(formatted_date,str(Calendar.date_formatter(date_inputted,nav_type)))

    
class CalendarTestGetDetailedReminders(unittest.TestCase):
    def test_get_detailed_reminders_raise_value_error(self):
        event = {
            'irrelevant':"nonsense"

        }
        with self.assertRaises(ValueError):
            Calendar.get_detailed_reminders(event)


    def test_get_detailed_reminders_path2_two_custom_reminders(self):
        
        event ={
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
        self.assertIn("email 1", reminders)
        self.assertIn("popup 10", reminders)


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

    



def main():
    # Create the test suite from the cases above.
    test_classes = [CalendarTestGetUpcomingEvents, CalendarTestGetUpcomingReminders,
                    CalendarTestGetPastReminders, CalendarTestNavigateCalendar,
                    CalendarTestGetDetailedEvent,
                    CalendarTestGetPastEvents, CalenderTestSearchEvents,
                    CalenderTestSearchReminders, CalendarTestDeleteEvents,
                    CalendarTestDeleteReminders, CalendarTestDateFormatter,
                    CalendarTestGetDetailedReminders]  # Test Classes
    for classes in test_classes:
        suite = unittest.TestLoader().loadTestsFromTestCase(classes)
        # This will run the test suite.
        unittest.TextTestRunner(verbosity=2).run(suite)


main()
