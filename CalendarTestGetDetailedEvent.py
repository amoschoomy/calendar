from datetime import datetime
import unittest
from unittest.mock import Mock, patch
import Calendar
class CalendarTestGetDetailedEvent(unittest.TestCase):

    def test_get_detailed_event_raise_value_error(self):
        event = {
            'irrelevant': "nonsense"

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
def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(CalendarTestGetDetailedEvent)
    # This will run the test suite.
    unittest.TextTestRunner(verbosity=2).run(suite)


main()