from datetime import datetime
import unittest
from unittest.mock import Mock, patch
import CalendarGUI

class CalendarGUITestGetDetailedEvent(unittest.TestCase):

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


    # These are each of the UI elements
    @patch.object(CalendarGUI, 'delete_event_btn')
    @patch.object(CalendarGUI, 'eventdetails')
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    @patch.object(CalendarGUI, 'api')
    @patch.object(CalendarGUI, 'nav_year')
    @patch.object(CalendarGUI, 'nav_month')
    @patch.object(CalendarGUI, 'nav_date')
    @patch.object(CalendarGUI, 'navigate_checked')
    @patch.object(CalendarGUI, 'dateIn')
    @patch.object(CalendarGUI, 'past_checked')
    @patch.object(CalendarGUI, 'searchIn')
    def test_reload_event_list_normal_upcoming_events(self, searchIn, past_checked, dateIn, navigate_checked,
                                                      nav_date, nav_month, nav_year, api, eventlist, reminderlist, details,
                                                      deleteBtn):
        searchIn.get.return_value = ""
        past_checked.get.return_value = 0
        dateIn.return_value = ""
        navigate_checked.get.return_value = 0
        api.events.return_value.list.return_value.execute.return_value = {
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
        self.assertEqual(api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(eventlist.delete.call_count, 1)
        self.assertEqual(reminderlist.delete.call_count, 1)
        self.assertEqual(details.delete.call_count, 1)
        self.assertEqual(deleteBtn.configure.call_count, 1)

    # These are each of the UI elements
    @patch.object(CalendarGUI, 'delete_event_btn')
    @patch.object(CalendarGUI, 'eventdetails')
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    @patch.object(CalendarGUI, 'api')
    @patch.object(CalendarGUI, 'nav_year')
    @patch.object(CalendarGUI, 'nav_month')
    @patch.object(CalendarGUI, 'nav_date')
    @patch.object(CalendarGUI, 'navigate_checked')
    @patch.object(CalendarGUI, 'dateIn')
    @patch.object(CalendarGUI, 'past_checked')
    @patch.object(CalendarGUI, 'searchIn')
    def test_reload_event_list_include_past_events(self, searchIn, past_checked, dateIn, navigate_checked, nav_date_input, nav_month_input, nav_year_input, api,
                                                   eventlist, reminderlist, details, deleteBtn):

        searchIn.get.return_value = ""
        past_checked.get.return_value = 1
        dateIn.get.return_value = "1/10/2019"
        navigate_checked.get.return_value = 0
        api.events.return_value.list.return_value.execute.return_value = {
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
        self.assertEqual(api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(eventlist.delete.call_count, 1)
        self.assertEqual(reminderlist.delete.call_count, 1)
        self.assertEqual(details.delete.call_count, 1)
        self.assertEqual(deleteBtn.configure.call_count, 1)

    # These are each of the UI elements
    @patch.object(CalendarGUI, 'delete_event_btn')
    @patch.object(CalendarGUI, 'eventdetails')
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    @patch.object(CalendarGUI, 'api')
    @patch.object(CalendarGUI, 'nav_year')
    @patch.object(CalendarGUI, 'nav_month')
    @patch.object(CalendarGUI, 'nav_date')
    @patch.object(CalendarGUI, 'navigate_checked')
    @patch.object(CalendarGUI, 'dateIn')
    @patch.object(CalendarGUI, 'past_checked')
    @patch.object(CalendarGUI, 'searchIn')
    def test_reload_event_list_include_past_events_invalid_past_date(self, searchIn, past_checked, dateIn, navigate_checked, nav_date_input,
                                                                     nav_month_input, nav_year_input, api,
                                                                     eventlist, reminderlist, details,
                                                                     deleteBtn):
        searchIn.get.return_value = ""
        past_checked.get.return_value = 1
        dateIn.get.return_value = "39/15/2980"
        navigate_checked.get.return_value = 0
        api.events.return_value.list.return_value.execute.return_value = {
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
        self.assertEqual(api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(eventlist.delete.call_count, 1)
        self.assertEqual(reminderlist.delete.call_count, 1)
        self.assertEqual(details.delete.call_count, 1)
        self.assertEqual(deleteBtn.configure.call_count, 1)

    # These are each of the UI elements
    @patch.object(CalendarGUI, 'delete_event_btn')
    @patch.object(CalendarGUI, 'eventdetails')
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    @patch.object(CalendarGUI, 'api')
    @patch.object(CalendarGUI, 'nav_year')
    @patch.object(CalendarGUI, 'nav_month')
    @patch.object(CalendarGUI, 'nav_date')
    @patch.object(CalendarGUI, 'navigate_checked')
    @patch.object(CalendarGUI, 'dateIn')
    @patch.object(CalendarGUI, 'past_checked')
    @patch.object(CalendarGUI, 'searchIn')
    def test_reload_event_list_navigate_specific_events(self, searchIn, past_checked, dateIn, navigate_checked, nav_date_input, nav_month_input, nav_year_input,
                                                        api,
                                                        eventlist, reminderlist, details,
                                                        deleteBtn):
        searchIn.get.return_value = ""
        past_checked.get.return_value = 0
        dateIn.get.return_value = ""
        navigate_checked.get.return_value = 1
        nav_date_input.get.return_value = "All"
        nav_month_input.get.return_value = "10"
        nav_year_input.get.return_value = "2020"
        api.events.return_value.list.return_value.execute.return_value = {
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
        self.assertEqual(api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(eventlist.delete.call_count, 1)
        self.assertEqual(reminderlist.delete.call_count, 1)
        self.assertEqual(details.delete.call_count, 1)
        self.assertEqual(deleteBtn.configure.call_count, 1)

    # These are each of the UI elements
    @patch.object(CalendarGUI, 'delete_event_btn')
    @patch.object(CalendarGUI, 'eventdetails')
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    @patch.object(CalendarGUI, 'api')
    @patch.object(CalendarGUI, 'nav_year')
    @patch.object(CalendarGUI, 'nav_month')
    @patch.object(CalendarGUI, 'nav_date')
    @patch.object(CalendarGUI, 'navigate_checked')
    @patch.object(CalendarGUI, 'dateIn')
    @patch.object(CalendarGUI, 'past_checked')
    @patch.object(CalendarGUI, 'searchIn')
    def test_reload_event_list_search_upcoming_events(self, searchIn, past_checked, dateIn, navigate_checked,
                                                      nav_date_input, nav_month_input, nav_year_input, api, eventlist, reminderlist, details,
                                                      deleteBtn):
        searchIn.get.return_value = "test"
        past_checked.get.return_value = 0
        dateIn.return_value = ""
        navigate_checked.get.return_value = 0
        api.events.return_value.list.return_value.execute.return_value = {
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
        self.assertEqual(api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(eventlist.delete.call_count, 1)
        self.assertEqual(reminderlist.delete.call_count, 1)
        self.assertEqual(details.delete.call_count, 1)
        self.assertEqual(deleteBtn.configure.call_count, 1)

    # These are each of the UI elements
    @patch.object(CalendarGUI, 'delete_event_btn')
    @patch.object(CalendarGUI, 'eventdetails')
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    @patch.object(CalendarGUI, 'api')
    @patch.object(CalendarGUI, 'nav_year')
    @patch.object(CalendarGUI, 'nav_month')
    @patch.object(CalendarGUI, 'nav_date')
    @patch.object(CalendarGUI, 'navigate_checked')
    @patch.object(CalendarGUI, 'dateIn')
    @patch.object(CalendarGUI, 'past_checked')
    @patch.object(CalendarGUI, 'searchIn')
    def test_reload_event_list_search_past_events(self, searchIn, past_checked, dateIn, navigate_checked, nav_date_input, nav_month_input, nav_year_input, api,
                                                  eventlist, reminderlist, details,
                                                  deleteBtn):
        searchIn.get.return_value = "test3"
        past_checked.get.return_value = 1
        dateIn.get.return_value = "10/10/2018"
        navigate_checked.get.return_value = 0
        api.events.return_value.list.return_value.execute.return_value = {
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
        self.assertEqual(api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(eventlist.delete.call_count, 1)
        self.assertEqual(reminderlist.delete.call_count, 1)
        self.assertEqual(details.delete.call_count, 1)
        self.assertEqual(deleteBtn.configure.call_count, 1)

    # These are each of the UI elements
    @patch.object(CalendarGUI, 'delete_event_btn')
    @patch.object(CalendarGUI, 'eventdetails')
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    @patch.object(CalendarGUI, 'api')
    @patch.object(CalendarGUI, 'nav_year')
    @patch.object(CalendarGUI, 'nav_month')
    @patch.object(CalendarGUI, 'nav_date')
    @patch.object(CalendarGUI, 'navigate_checked')
    @patch.object(CalendarGUI, 'dateIn')
    @patch.object(CalendarGUI, 'past_checked')
    @patch.object(CalendarGUI, 'searchIn')
    def test_reload_event_list_search_in_navigated_events(self, searchIn, past_checked, dateIn, navigate_checked, nav_date_input, nav_month_input, nav_year_input,
                                                          api,
                                                          eventlist, reminderlist, details, deleteBtn):
        searchIn.get.return_value = "test2"
        past_checked.get.return_value = 0
        dateIn.get.return_value = ""
        navigate_checked.get.return_value = 1
        nav_date_input.get.return_value = "All"
        nav_month_input.get.return_value = "10"
        nav_year_input.get.return_value = "2020"
        api.events.return_value.list.return_value.execute.return_value = {
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
        self.assertEqual(api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(eventlist.delete.call_count, 1)
        self.assertEqual(reminderlist.delete.call_count, 1)
        self.assertEqual(details.delete.call_count, 1)
        self.assertEqual(deleteBtn.configure.call_count, 1)


class CalendarGUITestLoadEventDetails(unittest.TestCase):

    def set_up(self):
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

    @patch.object(CalendarGUI, 'delete_reminder_btn')
    @patch.object(CalendarGUI, 'delete_event_btn')
    @patch.object(CalendarGUI, 'eventdetails')
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    def test_load_event_details_no_selection(self, eventlist, reminderlist, details, deleteBtn, deleteReminderBtn):
        self.set_up()
        eventlist.curselection.return_value = []
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

    @patch.object(CalendarGUI, 'delete_reminder_btn')
    @patch.object(CalendarGUI, 'delete_event_btn')
    @patch.object(CalendarGUI, 'eventdetails')
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    def test_load_event_details_has_selection(self, eventlist, reminderlist, details, deleteBtn, deleteReminderBtn):
        self.set_up()
        eventlist.curselection.return_value = ["0"]
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

    @patch.object(CalendarGUI, 'delete_reminder_btn')
    @patch.object(CalendarGUI, 'delete_event_btn')
    @patch.object(CalendarGUI, 'eventdetails')
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    def test_load_event_details_has_selection_default_reminder(self, eventlist, reminderlist, details, deleteBtn,
                                                               deleteReminderBtn):
        self.set_up()
        eventlist.curselection.return_value = ["1"]
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

    @patch.object(CalendarGUI, 'reload_event_list')
    @patch.object(CalendarGUI, 'api')
    @patch.object(CalendarGUI, 'eventlist')
    def test_delete_event_no_selection(self, eventlist, api, reload_event_list):
        eventlist.curselection.return_value = []

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
        CalendarGUI.delete_event()

        # constant
        self.assertEqual(eventlist.curselection.call_count, 1)

        # changes
        event_selected = 0
        self.assertEqual(api.events.return_value.delete.return_value.execute.call_count, event_selected)
        self.assertEqual(reload_event_list.call_count, event_selected)

    @patch.object(CalendarGUI, 'reload_event_list')
    @patch.object(CalendarGUI, 'api')
    @patch.object(CalendarGUI, 'eventlist')
    def test_delete_event_has_selection(self, eventlist, api, reload_event_list):
        eventlist.curselection.return_value = ["0"]

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
        CalendarGUI.delete_event()

        # constant
        self.assertEqual(eventlist.curselection.call_count, 1)

        # changes
        event_selected = 1
        self.assertEqual(api.events.return_value.delete.return_value.execute.call_count, event_selected)
        self.assertEqual(reload_event_list.call_count, event_selected)


class CalendarGUITestDeleteReminder(unittest.TestCase):

    @patch.object(CalendarGUI, 'load_event_details')
    @patch.object(CalendarGUI, 'api')
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    def test_delete_reminder_no_selected_event(self, eventlist, reminderlist, api, load_event_details):
        eventlist.curselection.return_value = []
        reminderlist.curselection.return_value = []
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
        }
        ]
        CalendarGUI.delete_reminder()

        # constant
        self.assertEqual(eventlist.curselection.call_count, 1)
        self.assertEqual(reminderlist.curselection.call_count, 1)
        # changes
        self.assertFalse(CalendarGUI.events[0]['reminders']['useDefault'])
        self.assertEqual(len(CalendarGUI.events[0]['reminders']['overrides']), 2)
        reminder_selected = 0
        self.assertEqual(api.events.return_value.update.return_value.execute.call_count, reminder_selected)
        self.assertEqual(load_event_details.call_count, reminder_selected)

    @patch.object(CalendarGUI, 'load_event_details')
    @patch.object(CalendarGUI, 'api')
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    def test_delete_reminder_no_selected_reminder(self, eventlist, reminderlist, api, load_event_details):
        eventlist.curselection.return_value = ["0"]
        reminderlist.curselection.return_value = []
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
        }
        ]
        CalendarGUI.delete_reminder()

        # constant
        self.assertEqual(eventlist.curselection.call_count, 1)
        self.assertEqual(reminderlist.curselection.call_count, 1)
        # changes
        self.assertFalse(CalendarGUI.events[0]['reminders']['useDefault'])
        self.assertEqual(len(CalendarGUI.events[0]['reminders']['overrides']), 2)
        reminder_selected = 0
        self.assertEqual(api.events.return_value.update.return_value.execute.call_count, reminder_selected)
        self.assertEqual(load_event_details.call_count, reminder_selected)

    @patch.object(CalendarGUI, 'load_event_details')
    @patch.object(CalendarGUI, 'api')
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    def test_delete_reminder_has_selected_event_and_reminder(self, eventlist, reminderlist, api,
                                                             load_event_details):
        eventlist.curselection.return_value = ["0"]
        reminderlist.curselection.return_value = ["0"]
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
        }
        ]
        CalendarGUI.delete_reminder()

        # constant
        self.assertEqual(eventlist.curselection.call_count, 1)
        self.assertEqual(reminderlist.curselection.call_count, 1)
        # changes
        self.assertFalse(CalendarGUI.events[0]['reminders']['useDefault'])
        self.assertEqual(len(CalendarGUI.events[0]['reminders']['overrides']), 1)
        reminder_selected = 1
        self.assertEqual(api.events.return_value.update.return_value.execute.call_count, reminder_selected)
        self.assertEqual(load_event_details.call_count, reminder_selected)

    @patch.object(CalendarGUI, 'load_event_details')
    @patch.object(CalendarGUI, 'api')
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    def test_delete_reminder_has_selected_event_and_uses_default_reminder(self, eventlist, reminderlist, api,
                                                                          load_event_details):
        eventlist.curselection.return_value = ["0"]
        reminderlist.curselection.return_value = ["0"]
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
        CalendarGUI.delete_reminder()

        # constant
        self.assertEqual(eventlist.curselection.call_count, 1)
        self.assertEqual(reminderlist.curselection.call_count, 1)
        # changes
        self.assertFalse(CalendarGUI.events[0]['reminders']['useDefault'])
        self.assertEqual(len(CalendarGUI.events[0]['reminders']['overrides']), 0)
        reminder_selected = 1
        self.assertEqual(api.events.return_value.update.return_value.execute.call_count, reminder_selected)
        self.assertEqual(load_event_details.call_count, reminder_selected)


class CalendarGUITestEnableDateTextbox(unittest.TestCase):

    @patch.object(CalendarGUI, 'navigate_checked')
    @patch.object(CalendarGUI, 'past_checked')
    @patch.object(CalendarGUI, 'dateIn')
    @patch.object(CalendarGUI, 'enable_periods')
    def test_enable_date_textbox_show_past_events_checked(self, periods, dateIn, past_checked, navigate_checked):

        past_checked.get.return_value = 1
        CalendarGUI.enable_date_textbox()

        # constant
        self.assertEqual(dateIn.configure.call_count, 1)

        # changes
        self.assertEqual(navigate_checked.set.call_count, 1)
        self.assertEqual(periods.call_count, 1)

    @patch.object(CalendarGUI, 'past_checked')
    @patch.object(CalendarGUI, 'dateIn')
    @patch.object(CalendarGUI, 'enable_periods')
    def test_enable_date_textbox_show_past_events_not_checked(self, periods, dateIn, past_checked):
        past_checked.get.return_value = 0
        CalendarGUI.enable_date_textbox()

        # constant
        self.assertEqual(dateIn.configure.call_count, 1)
        # changes
        self.assertEqual(periods.call_count, 0)


class CalendarGUITestEnablePeriods(unittest.TestCase):

    @patch.object(CalendarGUI, 'past_checked')
    @patch.object(CalendarGUI, 'navigate_checked')
    @patch.object(CalendarGUI, 'enable_date_textbox')
    @patch.object(CalendarGUI, 'nav_year_input')
    @patch.object(CalendarGUI, 'nav_month_input')
    @patch.object(CalendarGUI, 'nav_date_input')
    def test_enable_date_textbox_show_specific_events_checked(self, nav_date_input, nav_month_input, nav_year_input, enable_date, navigate_checked, past_checked):
        navigate_checked.get.return_value = 1
        CalendarGUI.enable_periods()

        # constant
        self.assertEqual(nav_date_input.configure.call_count, 1)
        self.assertEqual(nav_month_input.configure.call_count, 1)
        self.assertEqual(nav_year_input.configure.call_count, 1)

        # changes
        self.assertEqual(past_checked.set.call_count, 1)
        self.assertEqual(enable_date.call_count, 1)

    @patch.object(CalendarGUI, 'navigate_checked')
    @patch.object(CalendarGUI, 'enable_date_textbox')
    @patch.object(CalendarGUI, 'nav_year_input')
    @patch.object(CalendarGUI, 'nav_month_input')
    @patch.object(CalendarGUI, 'nav_date_input')
    def test_enable_date_textbox_show_specific_events_not_checked(self, nav_date_input, nav_month_input, nav_year_input, enable_date, navigate_checked):
        navigate_checked.get.return_value = 0
        CalendarGUI.enable_periods()

        # constant
        self.assertEqual(nav_date_input.configure.call_count, 1)
        self.assertEqual(nav_month_input.configure.call_count, 1)
        self.assertEqual(nav_year_input.configure.call_count, 1)

        # changes
        self.assertEqual(enable_date.call_count, 0)


class CalendarGUITestGetPeriods(unittest.TestCase):

    def test_get_periods_specified_day_specified_month_specified_year(self):
        d = "12"
        m = "10"  # Month 10 is useless here as we wanted all years
        y = "2019"
        result = CalendarGUI.get_periods(d,m,y)
        start = "2019-10-12" # There are the same as we wanted events for that day
        end = "2019-10-12"
        self.assertIn(start, result[0])
        self.assertIn(end, result[1])

    def test_get_periods_all_day_specified_month_year(self):
        d = "All"
        m = "10"
        y = "2020"
        result = CalendarGUI.get_periods(d,m,y)
        start = "2020-10-01"
        end = "2020-10-31"
        self.assertIn(start,result[0])
        self.assertIn(end,result[1])

    def test_get_periods_all_day_all_month_specified_year(self):
        d = "All"
        m = "All"
        y = "2020"
        result = CalendarGUI.get_periods(d,m,y)
        start = "2020-01-01"
        end = "2020-12-31"
        self.assertIn(start,result[0])
        self.assertIn(end,result[1])

    def test_get_periods_specified_day_all_month_specified_year(self):
        d = "12"  # Day 12 is useless here as we wanted all months for 2020
        m = "All"
        y = "2020"
        result = CalendarGUI.get_periods(d,m,y)
        start = "2020-01-01"
        end = "2020-12-31"
        self.assertIn(start,result[0])
        self.assertIn(end,result[1])

    def test_get_periods_all_day_all_month_all_year(self):
        d = "All"
        m = "All"
        y = "All"
        result = CalendarGUI.get_periods(d,m,y)
        self.assertIsNone(result[0])
        self.assertIsNone(result[1])

    def test_get_periods_specified_day_specified_month__all_year(self):
        d = "12" # Day 12 and month 12 is useless here as we wanted all years
        m = "12" # Day 12 and month 12 is useless here as we wanted all years
        y = "All"
        result = CalendarGUI.get_periods(d, m, y)
        self.assertIsNone(result[0])
        self.assertIsNone(result[1])

    def test_get_periods_specified_day_all_month_all_year(self):
        d = "12" # Day 12 is useless here as we wanted all months and year
        m = "All"
        y = "All"
        result = CalendarGUI.get_periods(d,m,y)
        self.assertIsNone(result[0])
        self.assertIsNone(result[1])

    def test_get_periods_all_day_specified_month_all_year(self):
        d = "All"
        m = "10"  # Month 10 is useless here as we wanted all years
        y = "All"
        result = CalendarGUI.get_periods(d,m,y)
        self.assertIsNone(result[0])
        self.assertIsNone(result[1])

    def test_get_periods_invalid_date_value_error(self):
        d = "31" # 31st September doesnt exist
        m = "9"
        y = "2020"
        result = CalendarGUI.get_periods(d,m,y)
        self.assertIn(str(datetime.utcnow().isoformat())[:10], result[0])
        self.assertIsNone(result[1])

    def test_get_periods_invalid_date_value_error_2(self):
        d = "30" # 30th February doesnt exist
        m = "2"
        y = "2020"
        result = CalendarGUI.get_periods(d,m,y)
        self.assertIn(str(datetime.utcnow().isoformat())[:10], result[0])
        self.assertIsNone(result[1])

class CalendarGUITestVerifyDate(unittest.TestCase):

    def test_verify_date_invalid_length(self):
        datestr = "10/10"
        self.assertFalse(CalendarGUI.verify_date(datestr))
        datestr = "10/2020"
        self.assertFalse(CalendarGUI.verify_date(datestr))
        datestr = "10-2020"
        self.assertFalse(CalendarGUI.verify_date(datestr))
        datestr = "10.2020"
        self.assertFalse(CalendarGUI.verify_date(datestr))

    def test_verify_date_valid_date_invalid_month_year(self):
        datestr = "10/32/2020"
        self.assertFalse(CalendarGUI.verify_date(datestr))
        datestr = "10/10/1000"
        self.assertFalse(CalendarGUI.verify_date(datestr))

    def test_verify_date_valid_month_invalid_date_year(self):
        datestr = "10/10/1000"
        self.assertFalse(CalendarGUI.verify_date(datestr))
        datestr = "69/10/2020"
        self.assertFalse(CalendarGUI.verify_date(datestr))

    def test_verify_date_valid_year_invalid_date_month(self):
        datestr = "100/10/2000"
        self.assertFalse(CalendarGUI.verify_date(datestr))
        datestr = "10/96/2020"
        self.assertFalse(CalendarGUI.verify_date(datestr))

    def test_verify_date_value_error_raised(self):
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

    def test_verify_date_valid_date(self):
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

    def test_verify_date_date_out_of_bounds(self):
        datestr = "12.1.1998"
        self.assertFalse(CalendarGUI.verify_date(datestr))
        datestr = "12.1.2066"
        self.assertFalse(CalendarGUI.verify_date(datestr))


class CalendarGUITestEnableDeleteReminder(unittest.TestCase):

    @patch.object(CalendarGUI, 'delete_reminder_btn')
    @patch.object(CalendarGUI, 'reminderlist')
    def test_enable_delete_reminder_no_selection(self, reminderlist, delete_reminder_btn):
        reminderlist.curselection.return_value = []
        CalendarGUI.enable_delete_reminder()

        # constant
        self.assertEqual(reminderlist.curselection.call_count, 1)

        # changes
        event_selected = 0
        self.assertEqual(delete_reminder_btn.configure.call_count, event_selected)

    @patch.object(CalendarGUI, 'delete_reminder_btn')
    @patch.object(CalendarGUI, 'reminderlist')
    def test_enable_delete_reminder_has_selection(self, reminderlist, delete_reminder_btn):
        reminderlist.curselection.return_value = ["9"]
        CalendarGUI.enable_delete_reminder()

        # constant
        self.assertEqual(reminderlist.curselection.call_count, 1)

        # changes
        event_selected = 1
        self.assertEqual(delete_reminder_btn.configure.call_count, event_selected)


class CalendarGUIUIElementsTest(unittest.TestCase):

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
    def test_assign_elements_to_grid(self, c, sch, searchIn, searchBtn, eventlist, refreshBtn, delete_event_btn, past_checkbox, dateIn, updateBtn, nv, \
        navigate_checkbox, nav_date_input, nav_month_input,nav_year_input, eventdetails, reminderlist, delete_reminder_btn, lbl1, lbl2, lbl3, lbl4, lbl5, lbl6, lbl7):
        CalendarGUI.assign_elements_to_grid()
        elements = locals()
        for i in elements:
            if i != 'self':
                self.assertEqual(elements[i].grid.call_count,1)


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
    def test_bind_elements_command(self, nav_date_input, nav_month_input, nav_year_input, searchBtn, refreshBtn, updateBtn, past_checkbox, navigate_checkbox, delete_event_btn,
                                   delete_reminder_btn, eventlist, reminderlist):

        CalendarGUI.bind_elements_command()
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
    test_classes = [CalendarGUITestGetDetailedEvent, CalendarGUITestReloadEventList, CalendarGUITestLoadEventDetails, CalendarGUITestDeleteEvent,
                    CalendarGUITestDeleteReminder, CalendarGUITestEnableDateTextbox, CalendarGUITestEnablePeriods, CalendarGUITestGetPeriods,
                    CalendarGUITestVerifyDate, CalendarGUITestEnableDeleteReminder, CalendarGUIUIElementsTest]  # Test Classes
    for classes in test_classes:
        suite = unittest.TestLoader().loadTestsFromTestCase(classes)
        # This will run the test suite.
        unittest.TextTestRunner(verbosity=2).run(suite)

main()
