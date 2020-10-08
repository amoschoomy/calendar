from time import time
import unittest
from unittest.mock import Mock,patch
import Calendar
# Add other imports here if needed

class CalendarTest(unittest.TestCase):
    # This test tests number of upcoming events.
    def test_get_upcoming_events_number(self):
        num_events = 2
        time = "2020-08-03T00:00:00.000000Z"

        mock_api = Mock()
        events = Calendar.get_upcoming_events(mock_api, time, num_events)

        self.assertEqual(
            mock_api.events.return_value.list.return_value.execute.return_value.get.call_count, 1)

        args, kwargs = mock_api.events.return_value.list.call_args_list[0]
        self.assertEqual(kwargs['maxResults'], num_events)

    # Add more test cases here
    #This test tests for assertion error raised if number of events
    def test_get_upcoming_events_negative_number(self):
        num_events=-1
        ex_time="2020-08-03T00:00:00.000000Z"

        mock_api=Mock()
        with self.assertRaises(ValueError):
            Calendar.get_upcoming_events(mock_api,ex_time,num_events)

class CalendarTestViewUpcomingEvents(unittest.TestCase):
    #Test Suite for User Story 1

    def test_get_upcoming_events_invalid_date(self):
        """This test for the if statement branch for date validity"""

        ex_time="January 1 2020" #Date is of an invalid date so will throw Value Error
        mock_api=Mock() #Mock api
        with self.assertRaises(ValueError):
            Calendar.get_upcoming_events_2(mock_api,ex_time)


    @patch("Calendar.get_calendar_api")
    def test_get_upcoming_events_valid_date(self,api):
        """This test for the succesful branch of if statement of date validity
            A patched call to calendar api is mocked
        """

        ex_time="2020-08-03T00:00:00.000000Z" #Valid date is given
        events=Calendar.get_upcoming_events_2(api,ex_time)
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
        self.assertEqual(Calendar.get_upcoming_events_2(api,ex_time),"test,2020-10-03T02:00:00.000000Z")

    @patch("Calendar.get_calendar_api")
    def test_get_upcoming_events_non_empty_events(self,api):
        """This test is to test getting upcoming events but for non empty events(for loop is executed) """
        ex_time="2020-10-03T00:00:00.000000Z"
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
        upcoming_events=Calendar.get_upcoming_events_2(api,ex_time)
        self.assertEqual(
            api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(upcoming_events,"test,2020-10-03T02:00:00.000000Z")

class CalendarTestGetUpcomingReminders(unittest.TestCase):
    def test_get_upcoming_reminders_invalid_date(self):
        #Path 1 where execution stops after invalid date given
        ex_time="January 1 2020" #Date is of an invalid date so will throw Value Error
        mock_api=Mock() #Mock api
        with self.assertRaises(ValueError):
            Calendar.get_upcoming_reminders(mock_api,ex_time)

    @patch("Calendar.get_calendar_api")
    def test_get_upcoming_reminders_path2(self,api):

        #Path 2 where the if statement of date validation succeeds, outer for loop is executed, else branch is executed
        #inside the loop, and from there the for loop in else branch is executed
        ex_time="2020-10-03T00:00:00.000000Z"
        api.events.return_value.list.return_value.execute.return_value = {
        "items": [
                    {
                        "summary": "test",
                        "start": {
                            "dateTime": "2020-10-03T02:00:00.000000Z"
                        },
                        "end": {
                            "dateTime": "2020-10-03T02:45:00.000000Z"
                        },"reminders":{
                            'useDefault': False,
                            'overrides': [
                                        {'method': 'email', 'minutes': 1},
                                        {'method': 'popup', 'minutes': 10},
    ],},
                    },
                       
        ]}
        reminders=Calendar.get_upcoming_reminders(api,ex_time)
        # Two seperate assertion checks for each method of reminder is present in method output
        self.assertEqual(
            api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertIn("email 1",reminders)
        self.assertIn("popup 10",reminders)

    @patch("Calendar.get_calendar_api")
    def test_get_upcoming_reminders_path3(self,api):

        #Path 3 where the if branch of date validity succeeded, the outer for loop doesn't get executed.
        ex_time="2020-10-03T00:00:00.000000Z"
        api.events.return_value.list.return_value.execute.return_value ={}
        reminders=Calendar.get_upcoming_reminders(api,ex_time)
        self.assertEqual(
            api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(reminders,"")


    @patch("Calendar.get_calendar_api")
    def test_get_upcoming_reminders_path4(self,api):
        #Path 4 where if branch of date validity succeeded, outer for loop is executed, else branch is executed but the for
        #loop in else branch is not executed
        ex_time="2020-10-03T00:00:00.000000Z"
        api.events.return_value.list.return_value.execute.return_value = {
        "items": [
                    {
                        "summary": "test",
                        "start": {
                            "dateTime": "2020-10-03T02:00:00.000000Z"
                        },
                        "end": {
                            "dateTime": "2020-10-03T02:45:00.000000Z"
                        },"reminders":{
                            'useDefault': False,
                            'overrides': [
                                            ],},
                    },
        
        ]}
        reminders=Calendar.get_upcoming_reminders(api,ex_time)
        self.assertEqual(
            api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(reminders,"\n") #A newline is returned due to the outer for loop being executed

    @patch("Calendar.get_calendar_api")
    def test_get_upcoming_reminders_path5(self,api):
        #Path 5 where if statement to check date validity succeeds, outer for loop is executed, and if
        #branch is executed which is default reminders
        ex_time="2020-10-03T00:00:00.000000Z"
        api.events.return_value.list.return_value.execute.return_value = {
        "items": [
                    {
                        "summary": "test",
                        "start": {
                            "dateTime": "2020-10-03T02:00:00.000000Z"
                        },
                        "end": {
                            "dateTime": "2020-10-03T02:45:00.000000Z"
                        },"reminders":{
                            'useDefault': True,
                            'overrides': [
                                            ],},
                    },
        
        ]}
        reminders=Calendar.get_upcoming_reminders(api,ex_time)
        self.assertEqual(
            api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(reminders,"test,Reminder through popup 10 minutes before event starts\n")


class CalendarTestGetPastEvents(unittest.TestCase):
    """Test Suite for Getting Past Events"""
    def test_get_past_events_invalid_past_date_format(self):
        """Invalid start date format, branch of date validation throws ValueError executed"""

        past_time="03 October 2020"
        time_now="2020-10-03T00:00:00.000000Z"
        api=Mock()
        with self.assertRaises(ValueError):
            Calendar.get_past_events(api,past_time,time_now)
    
    def test_get_past_events_invalid_end_date_format(self):
        """Invalid start date format, branch of date validation throws ValueError executed"""

        past_time="2020-10-03T00:00:00.000000Z"
        time_now="15 October 2020"
        api=Mock()
        with self.assertRaises(ValueError):
            Calendar.get_past_events(api,past_time,time_now)

    def test_get_past_events_exceeded_date(self):
        """Past date has exceeded start date, branch of date validation of time comparison executed"""
        past_time="2020-10-03T00:00:00.000000Z"
        time_now="2020-01-03T00:00:00.000000Z"
        api=Mock()
        with self.assertRaises(ValueError):
            Calendar.get_past_events(api,past_time,time_now)


    @patch("Calendar.get_calendar_api")
    def test_get_past_events_same_date(self,api):
        """Same date in calendar test, boundary of ending time is the same as past time"""
        past_time="2020-10-03T00:00:00.000000Z"
        time_now="2020-10-03T00:00:00.000000Z"

        #If its the same date and time, only events of start and end at same time can be returned
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
        past_events=Calendar.get_past_events(api,past_time,time_now)
        self.assertEqual(
            api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(past_events,"test,2020-10-03T00:00:00.000000Z")

    @patch("Calendar.get_calendar_api")
    def test_get_past_events_valid_date_and_time(self,api):
        #Test for the other branch of date format validity in the if statement
        #No exceptions will be raised
        past_time="2020-10-03T00:00:00.000000Z"
        time_now="2020-10-15T00:00:00.000000Z"
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
        past_events=Calendar.get_past_events(api,past_time,time_now)
        self.assertEqual(
            api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(past_events,"test,2020-10-07T00:00:00.000000Z")

    @patch("Calendar.get_calendar_api")
    def test_get_past_events_empty_events(self,api):
        #Test for non execution of the for loop when retrieving event list
        # Which means no events found in that time frame
        past_time="2020-10-03T00:00:00.000000Z"
        time_now="2020-10-15T00:00:00.000000Z"
        api.events.return_value.list.return_value.execute.return_value={}
        past_events=Calendar.get_past_events(api,past_time,time_now)
        self.assertEqual(
            api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(past_events,"")

    @patch("Calendar.get_calendar_api")
    def test_get_past_events_non_empty_events(self,api):
        past_time="2020-10-03T00:00:00.000000Z"
        time_now="2020-10-15T00:00:00.000000Z"
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
        past_events=Calendar.get_past_events(api,past_time,time_now)
        self.assertEqual(
            api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertIn("test",past_events)
        self.assertIn("Hello World",past_events)


def main():
    # Create the test suite from the cases above.
    test_classes=[CalendarTest,CalendarTestViewUpcomingEvents,CalendarTestGetUpcomingReminders,CalendarTestGetPastEvents] #Test Classes 
    for classes in test_classes:
        suite = unittest.TestLoader().loadTestsFromTestCase(classes)
        # This will run the test suite.
        unittest.TextTestRunner(verbosity=2).run(suite)
   

main()
