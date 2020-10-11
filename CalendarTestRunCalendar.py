from datetime import datetime
import unittest
from unittest.mock import Mock, patch
import Calendar
import sys
from io import StringIO


class CalendarTestRunCalendar(unittest.TestCase):
    @patch("Calendar.get_calendar_api")
    @patch('sys.stdout', new_callable=StringIO)
    @patch('Calendar.input', create=True)
    def test_run_calendar_help(self, mocked_input, mocked_output, api):
        mocked_input.side_effect = ["help", "exit"]
        Calendar.run_calendar(api)
        # Special string printed when user ask for help
        self.assertIn("Contact devs at acho0057@student.monash.edu for further help", mocked_output.getvalue())

    @patch("Calendar.get_calendar_api")
    @patch('sys.stdout', new_callable=StringIO)
    @patch('Calendar.input', create=True)
    def test_run_calendar_invalid_command(self, mocked_input, mocked_output, api):
        mocked_input.side_effect = ["test", "exit"]
        Calendar.run_calendar(api)
        # Special string printed when user ask for help
        self.assertIn("Invalid command. Please try again!", mocked_output.getvalue())

    @patch("Calendar.get_calendar_api")
    @patch('sys.stdout', new_callable=StringIO)
    @patch('Calendar.input', create=True)
    def test_run_calendar_upcoming_events(self, mocked_input, mocked_output, api):
        ex_time = "2020-08-03T00:00:00.000000Z"  # Valid date is given
        api.events.return_value.list.return_value.execute.return_value = {
            "items": [
                {
                    "summary": "Monash Exam",
                    "start": {
                        "dateTime": "2020-10-03T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2020-10-03T02:45:00.000000Z"
                    },
                },

            ]}
        mocked_input.side_effect = ["upcoming -e", "exit"]
        Calendar.run_calendar(api)
        self.assertIn("Monash Exam,2020-10-03T02:00:00.000000Z", mocked_output.getvalue())

    @patch("Calendar.get_calendar_api")
    @patch('sys.stdout', new_callable=StringIO)
    @patch('Calendar.input', create=True)
    def test_run_calendar_upcoming_reminders(self, mocked_input, mocked_output, api):
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
        mocked_input.side_effect = ["upcoming -r", "exit"]
        Calendar.run_calendar(api)
        self.assertIn("popup 10", mocked_output.getvalue())
        self.assertIn("email 1", mocked_output.getvalue())

    @patch("Calendar.get_calendar_api")
    @patch('sys.stdout', new_callable=StringIO)
    @patch('Calendar.input', create=True)
    def test_run_calendar_past_events(self, mocked_input, mocked_output, api):
        api.events.return_value.list.return_value.execute.return_value = {
            "items": [
                {
                    "summary": "Monash Exam",
                    "start": {
                        "dateTime": "2020-10-03T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2020-10-03T02:45:00.000000Z"
                    },
                },

            ]}
        mocked_input.side_effect = ["past -e", "2020-10-10", "exit"]
        Calendar.run_calendar(api)
        self.assertIn("Monash Exam,2020-10-03T02:00:00.000000Z", mocked_output.getvalue())

    @patch("Calendar.get_calendar_api")
    @patch('sys.stdout', new_callable=StringIO)
    @patch('Calendar.input', create=True)
    def test_run_calendar_past_reminders(self, mocked_input, mocked_output, api):
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
        mocked_input.side_effect = ["past -r", "2020-10-01", "exit"]
        Calendar.run_calendar(api)
        self.assertIn("email 1", mocked_output.getvalue())
        self.assertIn("popup 10", mocked_output.getvalue())


    @patch("Calendar.get_calendar_api")
    @patch('sys.stdout', new_callable=StringIO)
    @patch('Calendar.input', create=True)
    def test_run_calendar_wrong_date_input(self, mocked_input, mocked_output, api):
        # Wrong date input in getting events and reminder
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
        mocked_input.side_effect = ["past -r", "2020-100-11", "2020-10-01", "past -e", "20202-110-1", "2020-10-01",
                                    "exit"]
        Calendar.run_calendar(api)
        #String printed to console if date input wrong
        self.assertIn("Wrong format please try again",mocked_output.getvalue())

    @patch("Calendar.get_calendar_api")
    @patch('sys.stdout',new_callable=StringIO)
    @patch('Calendar.input', create=True)
    def test_run_calendar_navigate_calendar_wrong_navigation_type(self,mocked_input,mocked_output,api):
        mocked_input.side_effect=["navigate","5","0","23 October 2020","y"," ","0","-","exit"]
        api.events.return_value.list.return_value.execute.return_value = {
            "items": [
                {
                    "summary": "COVID",
                    "start": {
                        "dateTime": "2020-10-03T02:00:00.000000Z"
                    },
                    "status": "confirmed",
                    'creator': {'email': 'donaldtrump@gmail.com', 'self': True},
                    'created': '2020-10-09T04:10:47.000Z',
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
        Calendar.run_calendar(api)
        #String printed to console if user input wrong navigation type
        self.assertIn("Wrong input. Try again",mocked_output.getvalue())

    @patch("Calendar.get_calendar_api")
    @patch('sys.stdout', new_callable=StringIO)
    @patch('Calendar.input', create=True)
    def test_run_calendar_navigate_calendar_view_but_no_delete(self, mocked_input, mocked_output, api):
        mocked_input.side_effect = ["navigate", "0", "23 October 2020", "y", " ", "0", "-", "exit"]
        api.events.return_value.list.return_value.execute.return_value = {
            "items": [
                {
                    "summary": "COVID",
                    "start": {
                        "dateTime": "2020-10-03T02:00:00.000000Z"
                    },
                    "status": "confirmed",
                    'creator': {'email': 'donaldtrump@gmail.com', 'self': True},
                    'created': '2020-10-09T04:10:47.000Z',
                    "end": {
                        "dateTime": "2020-10-03T02:45:00.000000Z"
                    }, "reminders": {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 1},
                        {'method': 'popup', 'minutes': 10},
                    ]}
                },
            ]}
        Calendar.run_calendar(api)

        self.assertIn("Status: confirmed",
                      mocked_output.getvalue())  # simple assertion check to test get_detailed_event been called
        self.assertIn("email 1",
                      mocked_output.getvalue())  # simple assertion check to test get_detailed_reminders been called
        self.assertIn("popup 10", mocked_output.getvalue())

        @patch("Calendar.get_calendar_api")
        @patch('sys.stdout', new_callable=StringIO)
        @patch('Calendar.input', create=True)
        def test_run_calendar_navigate_calendar_view_and_delete(self, mocked_input, mocked_output, api):
            mocked_input.side_effect = ["navigate", "0", "23 October 2020", "y", " ", "0", "del", "exit"]
            api.events.return_value.list.return_value.execute.return_value = {
                "items": [
                    {
                        "summary": "COVID",
                        "start": {
                            "dateTime": "2020-10-03T02:00:00.000000Z"
                        },
                        "status": "confirmed",
                        'creator': {'email': 'donaldtrump@gmail.com', 'self': True},
                        'created': '2020-10-09T04:10:47.000Z',
                        "end": {
                            "dateTime": "2020-10-03T02:45:00.000000Z"
                        }, "reminders": {
                        'useDefault': False,
                        'overrides': [
                            {'method': 'email', 'minutes': 1},
                            {'method': 'popup', 'minutes': 10},
                        ]}
                    },
                ]}
            Calendar.run_calendar(api)
            self.assertEqual("Deleted event successfully", mocked_output.getvalue())

        @patch("Calendar.get_calendar_api")
        @patch('sys.stdout', new_callable=StringIO)
        @patch('Calendar.input', create=True)
        def test_run_calendar_navigate_calendar_view_and_delete_reminders(self, mocked_input, mocked_output, api):
            mocked_input.side_effect = ["navigate", "0", "23 October 2020", "y", " ", "0", "del -r", "0", "exit"]
            api.events.return_value.list.return_value.execute.return_value = {
                "items": [
                     {
                            "summary": "COVID",
                            "start": {
                                "dateTime": "2020-10-03T02:00:00.000000Z"
                        },
                            "status": "confirmed",
                            'creator': {'email': 'donaldtrump@gmail.com', 'self': True},
                            'created': '2020-10-09T04:10:47.000Z',
                            "end": {
                                "dateTime": "2020-10-03T02:45:00.000000Z"
                        }, "reminders": {
                            'useDefault': False,
                            'overrides': [
                         {'method': 'email', 'minutes': 1},
                                {'method': 'popup', 'minutes': 10},
                            ]}
                    },
                ]}
            Calendar.run_calendar(api)
            self.assertEqual("Reminder deleted succfully", mocked_output.getvalue())


        @patch("Calendar.get_calendar_api")
        @patch('sys.stdout', new_callable=StringIO)
        @patch('Calendar.input', create=True)
        def test_run_calendar_search_events(self, mocked_input, mocked_output, api):
            api.events.return_value.list.return_value.execute.return_value = {
                "items": [
                    {
                        "summary": "Monash Exam",
                        "start": {
                            "dateTime": "2020-10-03T02:00:00.000000Z"
                        },
                        "end": {
                            "dateTime": "2020-10-03T02:45:00.000000Z"
                        }
                    }
                    ]}
            mocked_input.side_effect = ["search -e", "Monash Exam", "exit"]
            Calendar.run_calendar(api)
            self.assertIn("Monash Exam,2020-10-03T02:00:00.000000Z", mocked_output.getvalue())


    @patch("Calendar.get_calendar_api")
    @patch('sys.stdout', new_callable=StringIO)
    @patch('Calendar.input', create=True)
    def test_run_calendar_search_events(self, mocked_input, mocked_output, api):
        ex_time = "2020-08-03T00:00:00.000000Z"  # Valid date is given
        api.events.return_value.list.return_value.execute.return_value = {
            "items": [
                {
                    "summary": "Monash Exam",
                    "start": {
                        "dateTime": "2020-10-03T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2020-10-03T02:45:00.000000Z"
                    },
                },

            ]}
        mocked_input.side_effect = ["search -e","Monash Exam", "exit"]
        Calendar.run_calendar(api)
        self.assertIn("Monash Exam,2020-10-03T02:00:00.000000Z", mocked_output.getvalue())

        @patch("Calendar.get_calendar_api")
        @patch('sys.stdout', new_callable=StringIO)
        @patch('Calendar.input', create=True)
        def test_run_calendar_search_reminders(self, mocked_input, mocked_output, api):
            api.events.return_value.list.return_value.execute.return_value = {
                "items": [
                    {
                        "summary": "Monash Exam",
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
                ]}
            mocked_input.side_effect = ["search -r", "Monash Exam", "exit"]
            Calendar.run_calendar(api)
            self.assertIn("email,1", mocked_output.getvalue())
            self.assertIn("popup,10", mocked_output.getvalue())


def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(CalendarTestRunCalendar)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)


main()
