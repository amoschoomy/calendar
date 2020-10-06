import unittest
from unittest.mock import Mock
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
    #Test Suite for Usr Story 1

    def test_get_upcoming_events_date(self):
        #This test for the if statement branch
        ex_time="January 1 2020"
        mock_api=Mock()
        with self.assertRaises(ValueError):
            Calendar.get_upcoming_events_2(mock_api,ex_time)





def main():
    # Create the test suite from the cases above.
    test_classes=[CalendarTest,CalendarTestViewUpcomingEvents] #Test 
    for classes in test_classes:
        suite = unittest.TestLoader().loadTestsFromTestCase(classes)
        # This will run the test suite.
        unittest.TextTestRunner(verbosity=2).run(suite)
   

main()
