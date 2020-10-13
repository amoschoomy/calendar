from datetime import datetime
import unittest
from unittest.mock import Mock, patch
import Calendar

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
        #navigate through a month of 30 days
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
        #navigate through year
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
        #navigate through day
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
        #navigating in February
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
        #navigate through feb in leap year
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
def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(CalendarTestNavigateCalendar)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)


main()