from datetime import datetime
import unittest
from unittest.mock import Mock, patch
import CalendarGUI

# NOTE: ALL THE TESTS HERE ARE FOR THE GUI
# EACH CLASS INDICATE A FUNCTION IN CalendarGUI.py

class CalendarGUITestGetDetailedEvent(unittest.TestCase):

    # METHOD UNDER TEST:  get_detailed_event
    # Strategy: MC/DC Coverage

    def test_get_detailed_event_raise_value_error(self):
        event = {
            'irrelevant': "nonsense"
        }
        with self.assertRaises(ValueError):
            CalendarGUI.get_detailed_event(event)

    def test_get_detailed_event_raise_attribute_error(self):
        event = "FAKE EVENT"
        with self.assertRaises(AttributeError):
            CalendarGUI.get_detailed_event(event)

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
        detailed_event = CalendarGUI.get_detailed_event(event)
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
        detailed_event = CalendarGUI.get_detailed_event(event)
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
        detailed_event = CalendarGUI.get_detailed_event(event)
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
        detailed_event = CalendarGUI.get_detailed_event(event)

        # Assert all keys found succesfully and string containing the information is printed
        self.assertIn("Visibility: private", detailed_event)
        self.assertIn("Location: Monash University, Wellington Rd, Clayton VIC 3800, Australia", detailed_event)
        self.assertIn("Attendees: trump@monash.edu, donald@monash.edu", detailed_event)


class CalendarGUITestReloadEventList(unittest.TestCase):

    # METHOD UNDER TEST: reload_event_list
    # Strategy: Path Coverage

    # These are each of the UI elements that require user inputs
    @patch.object(CalendarGUI, 'delete_event_btn')
    @patch.object(CalendarGUI, 'eventdetails')
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    @patch.object(CalendarGUI, 'nav_year')
    @patch.object(CalendarGUI, 'nav_month')
    @patch.object(CalendarGUI, 'nav_date')
    @patch.object(CalendarGUI, 'navigate_checked')
    @patch.object(CalendarGUI, 'dateIn')
    @patch.object(CalendarGUI, 'past_checked')
    @patch.object(CalendarGUI, 'searchIn')
    def test_reload_event_list_normal_upcoming_events(self, searchIn, past_checked, dateIn, navigate_checked,
                                                      nav_date, nav_month, nav_year, eventlist, reminderlist,
                                                      details,
                                                      deleteBtn):
        searchIn.get.return_value = ""
        past_checked.get.return_value = 0  # Do not include past events
        dateIn.return_value = ""
        navigate_checked.get.return_value = 0
        CalendarGUI.api = Mock()
        CalendarGUI.api.events.return_value.list.return_value.execute.return_value = {
            "items": [
                {
                    "summary": "test1",
                    "start": {
                        "dateTime": "2021-10-03T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2021-10-03T02:45:00.000000Z"
                    },
                    "reminders": {
                        "useDefault": False,
                        "overrides": [
                            {"method": "email", "minutes": 1},
                            {"method": "popup", "minutes": 10}
                        ]
                    }
                },
                {
                    "summary": "test2",
                    "start": {
                        "dateTime": "2021-10-03T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2021-10-03T02:45:00.000000Z"
                    },
                    "reminders": {
                        "useDefault": False,
                        "overrides": [
                            {"method": "email", "minutes": 1},
                            {"method": "popup", "minutes": 10}
                        ]
                    }
                }

            ]}
        CalendarGUI.reload_event_list()

        # changes
        self.assertEqual(searchIn.get.call_count, 1)
        self.assertEqual(navigate_checked.get.call_count, 1)
        self.assertEqual(nav_date.call_count, 0)
        self.assertEqual(nav_month.call_count, 0)
        self.assertEqual(nav_year.call_count, 0)
        self.assertEqual(eventlist.insert.call_count, 2)

        # constant
        self.assertEqual(past_checked.get.call_count, 1)
        self.assertEqual(dateIn.get.call_count, 1)
        self.assertEqual(CalendarGUI.api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(eventlist.delete.call_count, 1)
        self.assertEqual(reminderlist.delete.call_count, 1)
        self.assertEqual(details.delete.call_count, 1)
        self.assertEqual(deleteBtn.configure.call_count, 1)

    # These are each of the UI elements that require user inputs
    @patch.object(CalendarGUI, 'delete_event_btn')
    @patch.object(CalendarGUI, 'eventdetails')
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    @patch.object(CalendarGUI, 'nav_year')
    @patch.object(CalendarGUI, 'nav_month')
    @patch.object(CalendarGUI, 'nav_date')
    @patch.object(CalendarGUI, 'navigate_checked')
    @patch.object(CalendarGUI, 'dateIn')
    @patch.object(CalendarGUI, 'past_checked')
    @patch.object(CalendarGUI, 'searchIn')
    def test_reload_event_list_include_past_events(self, searchIn, past_checked, dateIn, navigate_checked,
                                                   nav_date_input, nav_month_input, nav_year_input,
                                                   eventlist, reminderlist, details, deleteBtn):
        searchIn.get.return_value = ""
        past_checked.get.return_value = 1  # Show past event checkbox checked
        dateIn.get.return_value = "1/10/2019"  # A valid date is inputted
        navigate_checked.get.return_value = 0
        CalendarGUI.api = Mock()
        CalendarGUI.api.events.return_value.list.return_value.execute.return_value = {
            "items": [
                {
                    "summary": "test1",
                    "start": {
                        "dateTime": "2021-10-03T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2021-10-03T02:45:00.000000Z"
                    },
                    "reminders": {
                        "useDefault": False,
                        "overrides": [
                            {"method": "email", "minutes": 1},
                            {"method": "popup", "minutes": 10}
                        ]
                    }
                },
                {
                    "summary": "test2",
                    "start": {
                        "dateTime": "2020-10-03T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2020-10-03T02:45:00.000000Z"
                    },
                    "reminders": {
                        "useDefault": False,
                        "overrides": [
                            {"method": "email", "minutes": 1},
                            {"method": "popup", "minutes": 10}
                        ]
                    }
                },
                {
                    "summary": "test3",
                    "start": {
                        "dateTime": "2019-10-03T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2019-10-03T02:45:00.000000Z"
                    },
                    "reminders": {
                        "useDefault": False,
                        "overrides": [
                            {"method": "email", "minutes": 1},
                            {"method": "popup", "minutes": 10}
                        ]
                    }
                }

            ]}
        CalendarGUI.reload_event_list()

        # changes
        self.assertEqual(searchIn.get.call_count, 1)
        self.assertEqual(navigate_checked.get.call_count, 0)
        self.assertEqual(nav_date_input.get.call_count, 0)
        self.assertEqual(nav_month_input.get.call_count, 0)
        self.assertEqual(nav_year_input.get.call_count, 0)
        self.assertEqual(eventlist.insert.call_count, 3)

        # constants
        self.assertEqual(past_checked.get.call_count, 1)
        self.assertEqual(dateIn.get.call_count, 1)
        self.assertEqual(CalendarGUI.api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(eventlist.delete.call_count, 1)
        self.assertEqual(reminderlist.delete.call_count, 1)
        self.assertEqual(details.delete.call_count, 1)
        self.assertEqual(deleteBtn.configure.call_count, 1)

    # These are each of the UI elements that require user inputs
    @patch.object(CalendarGUI, 'delete_event_btn')
    @patch.object(CalendarGUI, 'eventdetails')
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    @patch.object(CalendarGUI, 'nav_year')
    @patch.object(CalendarGUI, 'nav_month')
    @patch.object(CalendarGUI, 'nav_date')
    @patch.object(CalendarGUI, 'navigate_checked')
    @patch.object(CalendarGUI, 'dateIn')
    @patch.object(CalendarGUI, 'past_checked')
    @patch.object(CalendarGUI, 'searchIn')
    def test_reload_event_list_include_past_events_invalid_past_date(self, searchIn, past_checked, dateIn,
                                                                     navigate_checked, nav_date_input,
                                                                     nav_month_input, nav_year_input,
                                                                     eventlist, reminderlist, details,
                                                                     deleteBtn):
        searchIn.get.return_value = ""
        past_checked.get.return_value = 1  # Show past event checkbox checked
        dateIn.get.return_value = "39/15/2980"  # But invalid date inputted
        navigate_checked.get.return_value = 0
        CalendarGUI.api = Mock()
        CalendarGUI.api.events.return_value.list.return_value.execute.return_value = {
            "items": [
                {
                    "summary": "test1",
                    "start": {
                        "dateTime": "2021-10-03T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2021-10-03T02:45:00.000000Z"
                    },
                    "reminders": {
                        "useDefault": False,
                        "overrides": [
                            {"method": "email", "minutes": 1},
                            {"method": "popup", "minutes": 10}
                        ]
                    }
                },
                {
                    "summary": "test2",
                    "start": {
                        "dateTime": "2020-10-03T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2020-10-03T02:45:00.000000Z"
                    },
                    "reminders": {
                        "useDefault": False,
                        "overrides": [
                            {"method": "email", "minutes": 1},
                            {"method": "popup", "minutes": 10}
                        ]
                    }
                }

            ]}
        CalendarGUI.reload_event_list()

        # changes
        self.assertEqual(searchIn.get.call_count, 1)
        self.assertEqual(navigate_checked.get.call_count, 1)
        self.assertEqual(nav_date_input.get.call_count, 0)
        self.assertEqual(nav_month_input.get.call_count, 0)
        self.assertEqual(nav_year_input.get.call_count, 0)
        self.assertEqual(eventlist.insert.call_count, 2)

        # constants
        self.assertEqual(past_checked.get.call_count, 1)
        self.assertEqual(dateIn.get.call_count, 1)
        self.assertEqual(CalendarGUI.api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(eventlist.delete.call_count, 1)
        self.assertEqual(reminderlist.delete.call_count, 1)
        self.assertEqual(details.delete.call_count, 1)
        self.assertEqual(deleteBtn.configure.call_count, 1)

    # These are each of the UI elements that require user inputs
    @patch.object(CalendarGUI, 'delete_event_btn')
    @patch.object(CalendarGUI, 'eventdetails')
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    @patch.object(CalendarGUI, 'nav_year')
    @patch.object(CalendarGUI, 'nav_month')
    @patch.object(CalendarGUI, 'nav_date')
    @patch.object(CalendarGUI, 'navigate_checked')
    @patch.object(CalendarGUI, 'dateIn')
    @patch.object(CalendarGUI, 'past_checked')
    @patch.object(CalendarGUI, 'searchIn')
    def test_reload_event_list_navigate_specific_events(self, searchIn, past_checked, dateIn, navigate_checked,
                                                        nav_date_input, nav_month_input, nav_year_input,
                                                        eventlist, reminderlist, details,
                                                        deleteBtn):
        searchIn.get.return_value = ""
        past_checked.get.return_value = 0
        dateIn.get.return_value = ""
        navigate_checked.get.return_value = 1  # "Show events from" checkbox checked
        nav_date_input.get.return_value = "All"  # Show events on All dates of October 2020
        nav_month_input.get.return_value = "10"
        nav_year_input.get.return_value = "2020"
        CalendarGUI.api = Mock()
        CalendarGUI.api.events.return_value.list.return_value.execute.return_value = {
            "items": [
                {
                    "summary": "test1",
                    "start": {
                        "dateTime": "2021-10-03T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2021-10-03T02:45:00.000000Z"
                    },
                    "reminders": {
                        "useDefault": False,
                        "overrides": [
                            {"method": "email", "minutes": 1},
                            {"method": "popup", "minutes": 10}
                        ]
                    }
                },
                {
                    "summary": "test2",
                    "start": {
                        "dateTime": "2020-10-03T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2020-10-03T02:45:00.000000Z"
                    },
                    "reminders": {
                        "useDefault": False,
                        "overrides": [
                            {"method": "email", "minutes": 1},
                            {"method": "popup", "minutes": 10}
                        ]
                    }
                }
            ]}

        CalendarGUI.reload_event_list()
        # changes
        self.assertEqual(searchIn.get.call_count, 1)
        self.assertEqual(navigate_checked.get.call_count, 1)
        self.assertEqual(nav_date_input.get.call_count, 1)
        self.assertEqual(nav_month_input.get.call_count, 1)
        self.assertEqual(nav_year_input.get.call_count, 1)
        self.assertEqual(eventlist.insert.call_count, 2)

        # constants
        self.assertEqual(past_checked.get.call_count, 1)
        self.assertEqual(dateIn.get.call_count, 1)
        self.assertEqual(CalendarGUI.api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(eventlist.delete.call_count, 1)
        self.assertEqual(reminderlist.delete.call_count, 1)
        self.assertEqual(details.delete.call_count, 1)
        self.assertEqual(deleteBtn.configure.call_count, 1)

    # These are each of the UI elements that require user inputs
    @patch.object(CalendarGUI, 'delete_event_btn')
    @patch.object(CalendarGUI, 'eventdetails')
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    @patch.object(CalendarGUI, 'nav_year')
    @patch.object(CalendarGUI, 'nav_month')
    @patch.object(CalendarGUI, 'nav_date')
    @patch.object(CalendarGUI, 'navigate_checked')
    @patch.object(CalendarGUI, 'dateIn')
    @patch.object(CalendarGUI, 'past_checked')
    @patch.object(CalendarGUI, 'searchIn')
    def test_reload_event_list_search_upcoming_events(self, searchIn, past_checked, dateIn, navigate_checked,
                                                      nav_date_input, nav_month_input, nav_year_input, eventlist,
                                                      reminderlist, details,
                                                      deleteBtn):
        searchIn.get.return_value = "test"  # Search for events containing "test" keyword
        past_checked.get.return_value = 0
        dateIn.return_value = ""
        navigate_checked.get.return_value = 0
        CalendarGUI.api = Mock()
        CalendarGUI.api.events.return_value.list.return_value.execute.return_value = {
            "items": [
                {
                    "summary": "test1",
                    "start": {
                        "dateTime": "2021-10-03T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2021-10-03T02:45:00.000000Z"
                    },
                    "reminders": {
                        "useDefault": False,
                        "overrides": [
                            {"method": "email", "minutes": 1},
                            {"method": "popup", "minutes": 10}
                        ]
                    }
                },
                {
                    "summary": "test2",
                    "start": {
                        "dateTime": "2020-10-03T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2020-10-03T02:45:00.000000Z"
                    },
                    "reminders": {
                        "useDefault": False,
                        "overrides": [
                            {"method": "email", "minutes": 1},
                            {"method": "popup", "minutes": 10}
                        ]
                    }
                }

            ]}
        CalendarGUI.reload_event_list()

        # changes
        self.assertEqual(searchIn.get.call_count, 2)
        self.assertEqual(navigate_checked.get.call_count, 1)
        self.assertEqual(nav_date_input.get.call_count, 0)
        self.assertEqual(nav_month_input.get.call_count, 0)
        self.assertEqual(nav_year_input.get.call_count, 0)
        self.assertEqual(eventlist.insert.call_count, 2)

        # constants
        self.assertEqual(past_checked.get.call_count, 1)
        self.assertEqual(dateIn.get.call_count, 1)
        self.assertEqual(CalendarGUI.api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(eventlist.delete.call_count, 1)
        self.assertEqual(reminderlist.delete.call_count, 1)
        self.assertEqual(details.delete.call_count, 1)
        self.assertEqual(deleteBtn.configure.call_count, 1)

    # These are each of the UI elements that require user inputs
    @patch.object(CalendarGUI, 'delete_event_btn')
    @patch.object(CalendarGUI, 'eventdetails')
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    @patch.object(CalendarGUI, 'nav_year')
    @patch.object(CalendarGUI, 'nav_month')
    @patch.object(CalendarGUI, 'nav_date')
    @patch.object(CalendarGUI, 'navigate_checked')
    @patch.object(CalendarGUI, 'dateIn')
    @patch.object(CalendarGUI, 'past_checked')
    @patch.object(CalendarGUI, 'searchIn')
    def test_reload_event_list_search_past_events(self, searchIn, past_checked, dateIn, navigate_checked,
                                                  nav_date_input, nav_month_input, nav_year_input,
                                                  eventlist, reminderlist, details,
                                                  deleteBtn):
        searchIn.get.return_value = "test3"  # Search for events containing test keyword
        past_checked.get.return_value = 1       # AND include vents from the past
        dateIn.get.return_value = "10/10/2018"  # from the date of 10/10/2018
        navigate_checked.get.return_value = 0
        CalendarGUI.api = Mock()
        CalendarGUI.api.events.return_value.list.return_value.execute.return_value = {
            "items": [
                {
                    "summary": "test3",
                    "start": {
                        "dateTime": "2019-10-03T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2019-10-03T02:45:00.000000Z"
                    },
                    "reminders": {
                        "useDefault": False,
                        "overrides": [
                            {"method": "email", "minutes": 1},
                            {"method": "popup", "minutes": 10}
                        ]
                    }
                }

            ]}

        CalendarGUI.reload_event_list()
        # changes
        self.assertEqual(searchIn.get.call_count, 2)
        self.assertEqual(navigate_checked.get.call_count, 0)
        self.assertEqual(nav_date_input.get.call_count, 0)
        self.assertEqual(nav_month_input.get.call_count, 0)
        self.assertEqual(nav_year_input.get.call_count, 0)
        self.assertEqual(eventlist.insert.call_count, 1)

        # constants
        self.assertEqual(past_checked.get.call_count, 1)
        self.assertEqual(dateIn.get.call_count, 1)
        self.assertEqual(CalendarGUI.api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(eventlist.delete.call_count, 1)
        self.assertEqual(reminderlist.delete.call_count, 1)
        self.assertEqual(details.delete.call_count, 1)
        self.assertEqual(deleteBtn.configure.call_count, 1)

    # These are each of the UI elements that require user inputs
    @patch.object(CalendarGUI, 'delete_event_btn')
    @patch.object(CalendarGUI, 'eventdetails')
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    @patch.object(CalendarGUI, 'nav_year')
    @patch.object(CalendarGUI, 'nav_month')
    @patch.object(CalendarGUI, 'nav_date')
    @patch.object(CalendarGUI, 'navigate_checked')
    @patch.object(CalendarGUI, 'dateIn')
    @patch.object(CalendarGUI, 'past_checked')
    @patch.object(CalendarGUI, 'searchIn')
    def test_reload_event_list_search_in_navigated_events(self, searchIn, past_checked, dateIn, navigate_checked,
                                                          nav_date_input, nav_month_input, nav_year_input,
                                                          eventlist, reminderlist, details, deleteBtn):
        searchIn.get.return_value = "test2"  # Search for events with test2 keyword
        past_checked.get.return_value = 0
        dateIn.get.return_value = ""
        navigate_checked.get.return_value = 1   # AND from a specific period
        nav_date_input.get.return_value = "All"  # From All dates of october and 2020
        nav_month_input.get.return_value = "10"
        nav_year_input.get.return_value = "2020"
        CalendarGUI.api = Mock()
        CalendarGUI.api.events.return_value.list.return_value.execute.return_value = {
            "items": [
                {
                    "summary": "test2",
                    "start": {
                        "dateTime": "2020-10-03T02:00:00.000000Z"
                    },
                    "end": {
                        "dateTime": "2020-10-03T02:45:00.000000Z"
                    },
                    "reminders": {
                        "useDefault": False,
                        "overrides": [
                            {"method": "email", "minutes": 1},
                            {"method": "popup", "minutes": 10}
                        ]
                    }
                }
            ]}

        CalendarGUI.reload_event_list()
        # changes
        self.assertEqual(searchIn.get.call_count, 2)
        self.assertEqual(navigate_checked.get.call_count, 1)
        self.assertEqual(nav_date_input.get.call_count, 1)
        self.assertEqual(nav_month_input.get.call_count, 1)
        self.assertEqual(nav_year_input.get.call_count, 1)
        self.assertEqual(eventlist.insert.call_count, 1)

        # constants
        self.assertEqual(past_checked.get.call_count, 1)
        self.assertEqual(dateIn.get.call_count, 1)
        self.assertEqual(CalendarGUI.api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(eventlist.delete.call_count, 1)
        self.assertEqual(reminderlist.delete.call_count, 1)
        self.assertEqual(details.delete.call_count, 1)
        self.assertEqual(deleteBtn.configure.call_count, 1)


class CalendarGUITestLoadEventDetails(unittest.TestCase):

    # METHOD UNDER TEST: load_event_details
    # Strategy: Path Coverage

    def setUp(self):
        CalendarGUI.events = [
            {
                "summary": "test2",
                "start": {
                    "dateTime": "2020-10-03T02:00:00.000000Z"
                },
                "end": {
                    "dateTime": "2020-10-03T02:45:00.000000Z"
                },
                "status": "confirmed",
                'creator': {'email': 'donaldtrump@gmail.com', 'self': True},
                'created': '2020-10-09T04:10:47.000Z',
                'attendees': [{'email': 'trump@monash.edu', 'responseStatus': 'needsAction'},
                              {'email': 'donald@monash.edu', 'responseStatus': 'needsAction'}],
                "reminders": {
                    "useDefault": False,
                    "overrides": [
                        {"method": "email", "minutes": 1},
                        {"method": "popup", "minutes": 10}
                    ]
                }
            },
            {
                "summary": "test2",
                "start": {
                    "dateTime": "2020-10-03T02:00:00.000000Z"
                },
                "end": {
                    "dateTime": "2020-10-03T02:45:00.000000Z"
                },
                "status": "confirmed",
                'creator': {'email': 'donaldtrump@gmail.com', 'self': True},
                'created': '2020-10-09T04:10:47.000Z',
                'attendees': [{'email': 'trump@monash.edu', 'responseStatus': 'needsAction'},
                              {'email': 'donald@monash.edu', 'responseStatus': 'needsAction'}],
                "reminders": {
                    "useDefault": True,
                    "overrides": [
                        {"method": "email", "minutes": 1},
                        {"method": "popup", "minutes": 10}
                    ]
                }
            }
        ]

    # These are UI elements that require user inputs
    @patch.object(CalendarGUI, 'delete_reminder_btn')
    @patch.object(CalendarGUI, 'delete_event_btn')
    @patch.object(CalendarGUI, 'eventdetails')
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    def test_load_event_details_no_selection(self, eventlist, reminderlist, details, deleteBtn, deleteReminderBtn):

        eventlist.curselection.return_value = []  # No event was selected from the event list
        CalendarGUI.load_event_details()

        # constant
        self.assertEqual(eventlist.curselection.call_count, 1)

        # changes
        self.assertEqual(reminderlist.insert.call_count, 0)

        event_selected = 0
        self.assertEqual(details.delete.call_count, event_selected)
        self.assertEqual(details.insert.call_count, event_selected)
        self.assertEqual(reminderlist.delete.call_count, event_selected)
        self.assertEqual(deleteBtn.configure.call_count, event_selected)
        self.assertEqual(deleteReminderBtn.configure.call_count, event_selected)

    # These are UI elements that require user inputs
    @patch.object(CalendarGUI, 'delete_reminder_btn')
    @patch.object(CalendarGUI, 'delete_event_btn')
    @patch.object(CalendarGUI, 'eventdetails')
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    def test_load_event_details_has_selection(self, eventlist, reminderlist, details, deleteBtn, deleteReminderBtn):

        eventlist.curselection.return_value = ["0"] # Event 0 was selected from the event list
        CalendarGUI.load_event_details()

        # constant
        self.assertEqual(eventlist.curselection.call_count, 1)

        # changes
        self.assertEqual(reminderlist.insert.call_count, 2)

        event_selected = 1
        self.assertEqual(details.delete.call_count, event_selected)
        self.assertEqual(details.insert.call_count, event_selected)
        self.assertEqual(reminderlist.delete.call_count, event_selected)
        self.assertEqual(deleteBtn.configure.call_count, event_selected)
        self.assertEqual(deleteReminderBtn.configure.call_count, event_selected)

    # These are UI elements that require user inputs
    @patch.object(CalendarGUI, 'delete_reminder_btn')
    @patch.object(CalendarGUI, 'delete_event_btn')
    @patch.object(CalendarGUI, 'eventdetails')
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    def test_load_event_details_has_selection_default_reminder(self, eventlist, reminderlist, details, deleteBtn,
                                                               deleteReminderBtn):

        eventlist.curselection.return_value = ["1"]  # Event 1 was selected from the event list which has a default reminder setting
        CalendarGUI.load_event_details()

        # constant
        self.assertEqual(eventlist.curselection.call_count, 1)

        # changes
        self.assertEqual(reminderlist.insert.call_count, 1)

        event_selected = 1
        self.assertEqual(details.delete.call_count, event_selected)
        self.assertEqual(details.insert.call_count, event_selected)
        self.assertEqual(reminderlist.delete.call_count, event_selected)
        self.assertEqual(deleteBtn.configure.call_count, event_selected)
        self.assertEqual(deleteReminderBtn.configure.call_count, event_selected)


class CalendarGUITestDeleteEvent(unittest.TestCase):

    # METHOD UNDER TEST: delete_event
    # Strategy: Path Coverage

    def setUp(self):
        CalendarGUI.events = [{
            "summary": "test2",
            "id": "test12345",
            "start": {
                "dateTime": "2020-10-03T02:00:00.000000Z"
            },
            "end": {
                "dateTime": "2020-10-03T02:45:00.000000Z"
            },

            "status": "confirmed",
            'creator': {'email': 'donaldtrump@gmail.com', 'self': True},
            'created': '2020-10-09T04:10:47.000Z',
            'attendees': [{'email': 'trump@monash.edu', 'responseStatus': 'needsAction'},
                          {'email': 'donald@monash.edu', 'responseStatus': 'needsAction'}],
            "reminders": {
                "useDefault": True,
                "overrides": [
                    {"method": "email", "minutes": 1},
                    {"method": "popup", "minutes": 10}
                ]
            }
        }
        ]

    # This is a function that may be called
    @patch.object(CalendarGUI, 'reload_event_list')
    # These are UI elements that require user inputs
    @patch.object(CalendarGUI, 'eventlist')
    def test_delete_event_no_selection(self, eventlist, reload_event_list):
        eventlist.curselection.return_value = []  # No event was selected from the event list
        CalendarGUI.api = Mock()
        CalendarGUI.delete_event()

        # constant
        self.assertEqual(eventlist.curselection.call_count, 1)

        # changes
        event_selected = 0
        self.assertEqual(CalendarGUI.api.events.return_value.delete.return_value.execute.call_count, event_selected)
        self.assertEqual(reload_event_list.call_count, event_selected)

    # This is a function that may be called
    @patch.object(CalendarGUI, 'reload_event_list')
    # These are UI elements that require user inputs
    @patch.object(CalendarGUI, 'eventlist')
    def test_delete_event_has_selection(self, eventlist, reload_event_list):
        eventlist.curselection.return_value = ["0"]  # Event 0 was selected from the event list
        CalendarGUI.api = Mock()
        CalendarGUI.delete_event()

        # constant
        self.assertEqual(eventlist.curselection.call_count, 1)

        # changes
        event_selected = 1
        self.assertEqual(CalendarGUI.api.events.return_value.delete.return_value.execute.call_count, event_selected)
        self.assertEqual(reload_event_list.call_count, event_selected)


class CalendarGUITestDeleteReminder(unittest.TestCase):

    # METHOD UNDER TEST: delete_reminder
    # Strategy: Path Coverage

    def setUp(self):
        CalendarGUI.events = [{
            "summary": "test2",
            "id": "test12345",
            "start": {
                "dateTime": "2020-10-03T02:00:00.000000Z"
            },
            "end": {
                "dateTime": "2020-10-03T02:45:00.000000Z"
            },

            "status": "confirmed",
            'creator': {'email': 'donaldtrump@gmail.com', 'self': True},
            'created': '2020-10-09T04:10:47.000Z',
            'attendees': [{'email': 'trump@monash.edu', 'responseStatus': 'needsAction'},
                          {'email': 'donald@monash.edu', 'responseStatus': 'needsAction'}],
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 1},
                    {"method": "popup", "minutes": 10}
                ]
            }
        },
            {
                "summary": "test2",
                "id": "test12345",
                "start": {
                    "dateTime": "2020-10-03T02:00:00.000000Z"
                },
                "end": {
                    "dateTime": "2020-10-03T02:45:00.000000Z"
                },

                "status": "confirmed",
                'creator': {'email': 'donaldtrump@gmail.com', 'self': True},
                'created': '2020-10-09T04:10:47.000Z',
                'attendees': [{'email': 'trump@monash.edu', 'responseStatus': 'needsAction'},
                              {'email': 'donald@monash.edu', 'responseStatus': 'needsAction'}],
                "reminders": {
                    "useDefault": True,
                    "overrides": [
                        {"method": "email", "minutes": 1},
                        {"method": "popup", "minutes": 10}
                    ]
                }
            }
        ]

    # This is a function that may be called
    @patch.object(CalendarGUI, 'load_event_details')
    # These are UI elements taht require user inputs
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    def test_delete_reminder_no_selected_event(self, eventlist, reminderlist, load_event_details):
        eventlist.curselection.return_value = []  # No event selected form the event list
        reminderlist.curselection.return_value = []
        CalendarGUI.api = Mock()
        CalendarGUI.delete_reminder()

        # constant
        self.assertEqual(eventlist.curselection.call_count, 1)
        self.assertEqual(reminderlist.curselection.call_count, 1)
        # changes
        self.assertFalse(CalendarGUI.events[0]['reminders']['useDefault'])
        self.assertEqual(len(CalendarGUI.events[0]['reminders']['overrides']), 2)
        reminder_selected = 0
        self.assertEqual(CalendarGUI.api.events.return_value.update.return_value.execute.call_count, reminder_selected)
        self.assertEqual(load_event_details.call_count, reminder_selected)

    # This is a function that may be called
    @patch.object(CalendarGUI, 'load_event_details')
    # These are UI elements taht require user inputs
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    def test_delete_reminder_no_selected_reminder(self, eventlist, reminderlist, load_event_details):
        eventlist.curselection.return_value = ["0"]  # An event was selected form the event list
        reminderlist.curselection.return_value = []  # But no reminder selected from reminder list
        CalendarGUI.api = Mock()
        CalendarGUI.delete_reminder()

        # constant
        self.assertEqual(eventlist.curselection.call_count, 1)
        self.assertEqual(reminderlist.curselection.call_count, 1)
        # changes
        self.assertFalse(CalendarGUI.events[0]['reminders']['useDefault'])
        self.assertEqual(len(CalendarGUI.events[0]['reminders']['overrides']), 2)
        reminder_selected = 0
        self.assertEqual(CalendarGUI.api.events.return_value.update.return_value.execute.call_count, reminder_selected)
        self.assertEqual(load_event_details.call_count, reminder_selected)

    # This is a function that may be called
    @patch.object(CalendarGUI, 'load_event_details')
    # These are UI elements taht require user inputs
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    def test_delete_reminder_has_selected_event_and_reminder(self, eventlist, reminderlist,load_event_details):
        eventlist.curselection.return_value = ["0"]  # Event was selected from event list
        reminderlist.curselection.return_value = ["0"]  # And a reminder was selected from reminder list
        CalendarGUI.api = Mock()
        CalendarGUI.delete_reminder()

        # constant
        self.assertEqual(eventlist.curselection.call_count, 1)
        self.assertEqual(reminderlist.curselection.call_count, 1)
        # changes
        self.assertFalse(CalendarGUI.events[0]['reminders']['useDefault'])
        self.assertEqual(len(CalendarGUI.events[0]['reminders']['overrides']), 1)
        reminder_selected = 1
        self.assertEqual(CalendarGUI.api.events.return_value.update.return_value.execute.call_count, reminder_selected)
        self.assertEqual(load_event_details.call_count, reminder_selected)

    # This is a function that may be called
    @patch.object(CalendarGUI, 'load_event_details')
    # These are UI elements taht require user inputs
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    def test_delete_reminder_has_selected_event_and_uses_default_reminder(self, eventlist, reminderlist,load_event_details):
        eventlist.curselection.return_value = ["1"]  # Event 1 was selected, which has a default reminder
        reminderlist.curselection.return_value = ["0"]
        CalendarGUI.api = Mock()
        CalendarGUI.delete_reminder()

        # constant
        self.assertEqual(eventlist.curselection.call_count, 1)
        self.assertEqual(reminderlist.curselection.call_count, 1)
        # changes
        self.assertFalse(CalendarGUI.events[1]['reminders']['useDefault'])
        self.assertEqual(len(CalendarGUI.events[1]['reminders']['overrides']), 0)
        reminder_selected = 1
        self.assertEqual(CalendarGUI.api.events.return_value.update.return_value.execute.call_count, reminder_selected)
        self.assertEqual(load_event_details.call_count, reminder_selected)


class CalendarGUITestEnableDateTextbox(unittest.TestCase):

    # METHOD UNDER TEST: enable_date_textbox
    # Strategy: Branch Coverage

    # These are UI Elements that need user inputs
    @patch.object(CalendarGUI, 'navigate_checked')
    @patch.object(CalendarGUI, 'past_checked')
    @patch.object(CalendarGUI, 'dateIn')
    # This is a function that needs to be called
    @patch.object(CalendarGUI, 'enable_periods')
    def test_enable_date_textbox_show_past_events_checked(self, enable_periods, dateIn, past_checked, navigate_checked):
        past_checked.get.return_value = 1  # Show past events checkbox checked
        CalendarGUI.enable_date_textbox()

        # constant
        self.assertEqual(dateIn.configure.call_count, 1)

        # changes
        self.assertEqual(navigate_checked.set.call_count, 1)  # "Show events from" checkbox must not be checked
        self.assertEqual(enable_periods.call_count, 1)   # Navigation period dropdown options must be disabled

    # These are UI Elements that need user inputs
    @patch.object(CalendarGUI, 'past_checked')
    @patch.object(CalendarGUI, 'dateIn')
    # This is a function that needs to be called
    @patch.object(CalendarGUI, 'enable_periods')
    def test_enable_date_textbox_show_past_events_not_checked(self, enable_periods, dateIn, past_checked):
        past_checked.get.return_value = 0  # Show past events checkbox not checked
        CalendarGUI.enable_date_textbox()

        # constant
        self.assertEqual(dateIn.configure.call_count, 1)
        # changes
        self.assertEqual(enable_periods.call_count, 0)  # Navigation period dropdown options MAY be enabled


class CalendarGUITestEnablePeriods(unittest.TestCase):

    # These are UI Elements that need user inputs
    @patch.object(CalendarGUI, 'past_checked')
    @patch.object(CalendarGUI, 'navigate_checked')
    @patch.object(CalendarGUI, 'enable_date_textbox')  # This is a function that needs to be called
    @patch.object(CalendarGUI, 'nav_year_input')
    @patch.object(CalendarGUI, 'nav_month_input')
    @patch.object(CalendarGUI, 'nav_date_input')
    def test_enable_date_textbox_show_specific_events_checked(self, nav_date_input, nav_month_input, nav_year_input,
                                                              enable_date, navigate_checked, past_checked):
        navigate_checked.get.return_value = 1    # "Show events from" checkbox checked
        CalendarGUI.enable_periods()

        # constant
        self.assertEqual(nav_date_input.configure.call_count, 1)
        self.assertEqual(nav_month_input.configure.call_count, 1)
        self.assertEqual(nav_year_input.configure.call_count, 1)

        # changes
        self.assertEqual(past_checked.set.call_count, 1)    # Show past events checkbox must not be checked
        self.assertEqual(enable_date.call_count, 1)     # Past date textbox must be disabled

    # These are UI Elements that need user inputs
    @patch.object(CalendarGUI, 'navigate_checked')
    @patch.object(CalendarGUI, 'enable_date_textbox')  # This is a function that needs to be called
    @patch.object(CalendarGUI, 'nav_year_input')
    @patch.object(CalendarGUI, 'nav_month_input')
    @patch.object(CalendarGUI, 'nav_date_input')
    def test_enable_date_textbox_show_specific_events_not_checked(self, nav_date_input, nav_month_input, nav_year_input,
                                                                  enable_date, navigate_checked):
        navigate_checked.get.return_value = 0  # "Show events from" checkbox unchecked
        CalendarGUI.enable_periods()

        # constant
        self.assertEqual(nav_date_input.configure.call_count, 1)
        self.assertEqual(nav_month_input.configure.call_count, 1)
        self.assertEqual(nav_year_input.configure.call_count, 1)

        # changes
        self.assertEqual(enable_date.call_count, 0)  # Past date textbox MAY be enabled


class CalendarGUITestGetPeriods(unittest.TestCase):

    # METHOD UNDER TEST: get_periods
    # Strategy: Category partitioning

    def test_get_periods_specified_day_specified_month_specified_year(self):
        d = "12"
        m = "10"
        y = "2019"
        result = CalendarGUI.get_periods(d, m, y)
        start = "2019-10-12"  # There are the same as we wanted events for that day
        end = "2019-10-12"
        self.assertIn(start, result[0])
        self.assertIn(end, result[1])

    def test_get_periods_all_days_specified_month_and_year(self):
        d = "All"
        m = "10"
        y = "2020"
        result = CalendarGUI.get_periods(d, m, y)
        start = "2020-10-01"
        end = "2020-10-31"
        self.assertIn(start, result[0])
        self.assertIn(end, result[1])

    def test_get_periods_all_months_specified_year(self):

        # Day is All
        d = "All"
        m = "All"
        y = "2020"
        result = CalendarGUI.get_periods(d, m, y)
        start = "2020-01-01"
        end = "2020-12-31"
        self.assertIn(start, result[0])
        self.assertIn(end, result[1])

        # Day is not All but its value is not important (useless)
        d = "12"  # Day 12 is useless here as we wanted all months for 2020
        m = "All"
        y = "2020"
        result = CalendarGUI.get_periods(d, m, y)
        start = "2020-01-01"
        end = "2020-12-31"
        self.assertIn(start, result[0])
        self.assertIn(end, result[1])

    def test_get_periods_all_years(self):

        # All events in All years
        d = "All"
        m = "All"
        y = "All"
        result = CalendarGUI.get_periods(d, m, y)
        self.assertIsNone(result[0])
        self.assertIsNone(result[1])

        # Specified day and month, but they are useless as we wanted all years
        d = "12"  # Day 12 and month 12 is useless here as we wanted all years
        m = "12"  # Day 12 and month 12 is useless here as we wanted all years
        y = "All"
        result = CalendarGUI.get_periods(d, m, y)
        self.assertIsNone(result[0])
        self.assertIsNone(result[1])

        # Specified day, but it is useless as we wanted all years
        d = "12"  # Day 12 is useless here as we wanted all months and year
        m = "All"
        y = "All"
        result = CalendarGUI.get_periods(d, m, y)
        self.assertIsNone(result[0])
        self.assertIsNone(result[1])

        # Specified month, but it is useless as we wanted all years
        d = "All"
        m = "10"  # Month 10 is useless here as we wanted all years
        y = "All"
        result = CalendarGUI.get_periods(d, m, y)
        self.assertIsNone(result[0])
        self.assertIsNone(result[1])

    def test_get_periods_invalid_date_value_error(self):
        d = "31"  # 31st September doesnt exist
        m = "9"
        y = "2020"
        result = CalendarGUI.get_periods(d, m, y)
        self.assertIn(str(datetime.utcnow().isoformat())[:10], result[0])
        self.assertIsNone(result[1])

        d = "30"  # 30th February doesnt exist
        m = "2"
        y = "2020"
        result = CalendarGUI.get_periods(d, m, y)
        self.assertIn(str(datetime.utcnow().isoformat())[:10], result[0])
        self.assertIsNone(result[1])


class CalendarGUITestVerifyDate(unittest.TestCase):

    # METHOD UNDER TEST: verify_date
    # Strategy: Path Coverage & MC/DC for the decision (valid_data && valid_month && valid_year)

    def test_verify_date_invalid_length(self):
        datestr = "10/10"
        self.assertFalse(CalendarGUI.verify_date(datestr))
        datestr = "10/2020"
        self.assertFalse(CalendarGUI.verify_date(datestr))
        datestr = "10-2020"
        self.assertFalse(CalendarGUI.verify_date(datestr))
        datestr = "10.2020"
        self.assertFalse(CalendarGUI.verify_date(datestr))

    def test_verify_date_invalid_characters_value_error_raised(self):
        datestr = "10/AB/2020"
        self.assertFalse(CalendarGUI.verify_date(datestr))
        datestr = "10/10/ABCD"
        self.assertFalse(CalendarGUI.verify_date(datestr))
        datestr = "AB/9/2019"
        self.assertFalse(CalendarGUI.verify_date(datestr))
        datestr = "10/CD/ABCD"
        self.assertFalse(CalendarGUI.verify_date(datestr))
        datestr = "AB/CD/2020"
        self.assertFalse(CalendarGUI.verify_date(datestr))
        datestr = "AB/12/ABCD"
        self.assertFalse(CalendarGUI.verify_date(datestr))
        datestr = "AB/AB/ABCD"
        self.assertFalse(CalendarGUI.verify_date(datestr))

    # Path coverage paused, START OF MC/DC TEST for (valid_date && valid_month && valid_year)
    def test_verify_date_valid_date_valid_month_invalid_year(self):
        datestr = "10/10/-8000"
        self.assertFalse(CalendarGUI.verify_date(datestr))

    def test_verify_date_valid_date_valid_year_invalid_month(self):
        datestr = "10/96/2020"
        self.assertFalse(CalendarGUI.verify_date(datestr))

    def test_verify_date_valid_month_valid_year_invalid_date(self):
        datestr = "69/10/2020"
        self.assertFalse(CalendarGUI.verify_date(datestr))

    def test_verify_date_valid_date_valid_month_valid_year(self):
        datestr = "12/12/2020"
        self.assertTrue(CalendarGUI.verify_date(datestr))
        self.assertEqual("12", CalendarGUI.verify_date(datestr)[0])
        self.assertEqual("12", CalendarGUI.verify_date(datestr)[1])
        self.assertEqual("2020", CalendarGUI.verify_date(datestr)[2])
        datestr = "30-12-2019"
        self.assertTrue(CalendarGUI.verify_date(datestr))
        self.assertEqual("30", CalendarGUI.verify_date(datestr)[0])
        self.assertEqual("12", CalendarGUI.verify_date(datestr)[1])
        self.assertEqual("2019", CalendarGUI.verify_date(datestr)[2])
    # END OF MC/DC Test, back to path coverage

    def test_verify_date_valid_date_but_out_of_bounds(self):
        datestr = "12/1/1998"
        self.assertFalse(CalendarGUI.verify_date(datestr))
        datestr = "12/1/2066"
        self.assertFalse(CalendarGUI.verify_date(datestr))


class CalendarGUITestEnableDeleteReminder(unittest.TestCase):

    # METHOD UNDER TEST: enable_delete_reminder
    # Strategy: Branch Coverage

    # These are UI Elements that need user inputs
    @patch.object(CalendarGUI, 'delete_reminder_btn')
    @patch.object(CalendarGUI, 'reminderlist')
    def test_enable_delete_reminder_no_selection(self, reminderlist, delete_reminder_btn):
        reminderlist.curselection.return_value = [] # No reminder was selected from the remider list
        CalendarGUI.enable_delete_reminder()

        # constant
        self.assertEqual(reminderlist.curselection.call_count, 1)

        # changes
        event_selected = 0
        self.assertEqual(delete_reminder_btn.configure.call_count, event_selected) # Delete reminder button should be disabled

    # These are UI Elements that need user inputs
    @patch.object(CalendarGUI, 'delete_reminder_btn')
    @patch.object(CalendarGUI, 'reminderlist')
    def test_enable_delete_reminder_has_selection(self, reminderlist, delete_reminder_btn):
        reminderlist.curselection.return_value = ["9"]  # A reminder was selected from the remider list
        CalendarGUI.enable_delete_reminder()

        # constant
        self.assertEqual(reminderlist.curselection.call_count, 1)

        # changes
        event_selected = 1
        self.assertEqual(delete_reminder_btn.configure.call_count, event_selected) # Delete reminder button should be enabled


class CalendarGUIUIElementsTest(unittest.TestCase):

    # METHOD UNDER TEST: assign_elements_to_grid and bind_elements_command

    # These are all the UI Elements that need to be displayed
    @patch.object(CalendarGUI, 'c')
    @patch.object(CalendarGUI, 'sch')
    @patch.object(CalendarGUI, 'searchIn')
    @patch.object(CalendarGUI, 'searchBtn')
    @patch.object(CalendarGUI, 'eventlist')
    @patch.object(CalendarGUI, 'refreshBtn')
    @patch.object(CalendarGUI, 'delete_event_btn')
    @patch.object(CalendarGUI, 'dateIn')
    @patch.object(CalendarGUI, 'past_checkbox')
    @patch.object(CalendarGUI, 'updateBtn')
    @patch.object(CalendarGUI, 'nv')
    @patch.object(CalendarGUI, 'navigate_checkbox')
    @patch.object(CalendarGUI, 'nav_date_input')
    @patch.object(CalendarGUI, 'nav_month_input')
    @patch.object(CalendarGUI, 'nav_year_input')
    @patch.object(CalendarGUI, 'eventdetails')
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'delete_reminder_btn')
    @patch.object(CalendarGUI, 'lbl1')
    @patch.object(CalendarGUI, 'lbl2')
    @patch.object(CalendarGUI, 'lbl3')
    @patch.object(CalendarGUI, 'lbl4')
    @patch.object(CalendarGUI, 'lbl5')
    @patch.object(CalendarGUI, 'lbl6')
    @patch.object(CalendarGUI, 'lbl7')
    def test_assign_elements_to_grid(self, c, sch, searchIn, searchBtn, eventlist, refreshBtn, delete_event_btn,
                                     past_checkbox, dateIn, updateBtn, nv, \
                                     navigate_checkbox, nav_date_input, nav_month_input, nav_year_input, eventdetails,
                                     reminderlist, delete_reminder_btn, lbl1, lbl2, lbl3, lbl4, lbl5, lbl6, lbl7):
        CalendarGUI.assign_elements_to_grid()
        elements = locals()
        for i in elements:
            if i != 'self':
                self.assertEqual(elements[i].grid.call_count, 1)  # Ensure all elements are added to their respective grid

    # These are UI Elements that need user inputs
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    @patch.object(CalendarGUI, 'delete_reminder_btn')
    @patch.object(CalendarGUI, 'delete_event_btn')
    @patch.object(CalendarGUI, 'navigate_checkbox')
    @patch.object(CalendarGUI, 'past_checkbox')
    @patch.object(CalendarGUI, 'updateBtn')
    @patch.object(CalendarGUI, 'refreshBtn')
    @patch.object(CalendarGUI, 'searchBtn')
    @patch.object(CalendarGUI, 'nav_year_input')
    @patch.object(CalendarGUI, 'nav_month_input')
    @patch.object(CalendarGUI, 'nav_date_input')
    def test_bind_elements_command(self, nav_date_input, nav_month_input, nav_year_input, searchBtn, refreshBtn,
                                   updateBtn, past_checkbox, navigate_checkbox, delete_event_btn,
                                   delete_reminder_btn, eventlist, reminderlist):

        CalendarGUI.bind_elements_command()

        # Ensure all relevant elements are binded with their respective commands
        self.assertEqual(nav_date_input.configure.call_count, 1)
        self.assertEqual(nav_month_input.configure.call_count, 1)
        self.assertEqual(nav_year_input.configure.call_count, 1)
        self.assertEqual(searchBtn.configure.call_count, 1)
        self.assertEqual(refreshBtn.configure.call_count, 1)
        self.assertEqual(updateBtn.configure.call_count, 1)
        self.assertEqual(past_checkbox.configure.call_count, 1)
        self.assertEqual(navigate_checkbox.configure.call_count, 1)
        self.assertEqual(delete_event_btn.configure.call_count, 1)
        self.assertEqual(delete_reminder_btn.configure.call_count, 1)
        self.assertEqual(eventlist.bind.call_count, 1)
        self.assertEqual(reminderlist.bind.call_count, 1)


def main():
    # Create the test suite from the cases above.
    test_classes = [CalendarGUITestGetDetailedEvent, CalendarGUITestReloadEventList, CalendarGUITestLoadEventDetails,
                    CalendarGUITestDeleteEvent,
                    CalendarGUITestDeleteReminder, CalendarGUITestEnableDateTextbox, CalendarGUITestEnablePeriods,
                    CalendarGUITestGetPeriods,
                    CalendarGUITestVerifyDate, CalendarGUITestEnableDeleteReminder,
                    CalendarGUIUIElementsTest]  # Test Classes
    for classes in test_classes:
        suite = unittest.TestLoader().loadTestsFromTestCase(classes)
        # This will run the test suite.
        unittest.TextTestRunner(verbosity=2).run(suite)


main()
