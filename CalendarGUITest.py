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

    @patch.object(CalendarGUI, 'delete_event_btn')
    @patch.object(CalendarGUI, 'eventdetails')
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    @patch.object(CalendarGUI, 'api')
    @patch.object(CalendarGUI, 'nav_year')
    @patch.object(CalendarGUI, 'nav_month')
    @patch.object(CalendarGUI, 'nav_date')
    @patch.object(CalendarGUI, 'specific_only')
    @patch.object(CalendarGUI, 'dateIn')
    @patch.object(CalendarGUI, 'past_only')
    @patch.object(CalendarGUI, 'searchIn')
    def test_reload_event_list_normal_upcoming_events(self, searchIn, past, dateIn, specific,
                                                      ndate, nmonth, nyear, api, eventlist, reminderlist, details,
                                                      deleteBtn):
        searchIn.get.return_value = ""
        past.get.return_value = 0
        dateIn.return_value = ""
        specific.get.return_value = 0
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
        self.assertEqual(specific.get.call_count, 1)
        self.assertEqual(ndate.call_count, 0)
        self.assertEqual(nmonth.call_count, 0)
        self.assertEqual(nyear.call_count, 0)
        self.assertEqual(eventlist.insert.call_count, 2)

        # constant
        self.assertEqual(past.get.call_count, 1)
        self.assertEqual(dateIn.get.call_count, 1)
        self.assertEqual(api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(eventlist.delete.call_count, 1)
        self.assertEqual(reminderlist.delete.call_count, 1)
        self.assertEqual(details.delete.call_count, 1)
        self.assertEqual(deleteBtn.configure.call_count, 1)

    @patch.object(CalendarGUI, 'delete_event_btn')
    @patch.object(CalendarGUI, 'eventdetails')
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    @patch.object(CalendarGUI, 'api')
    @patch.object(CalendarGUI, 'nav_year')
    @patch.object(CalendarGUI, 'nav_month')
    @patch.object(CalendarGUI, 'nav_date')
    @patch.object(CalendarGUI, 'specific_only')
    @patch.object(CalendarGUI, 'dateIn')
    @patch.object(CalendarGUI, 'past_only')
    @patch.object(CalendarGUI, 'searchIn')
    def test_reload_event_list_include_past_events(self, searchIn, past, dateIn, specific, ndate, nmonth, nyear, api,
                                                   eventlist, reminderlist, details,
                                                   deleteBtn):
        searchIn.get.return_value = ""
        past.get.return_value = 1
        dateIn.get.return_value = "10/10/2018"
        specific.get.return_value = 0
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
        self.assertEqual(specific.get.call_count, 0)
        self.assertEqual(ndate.get.call_count, 0)
        self.assertEqual(nmonth.get.call_count, 0)
        self.assertEqual(nyear.get.call_count, 0)
        self.assertEqual(eventlist.insert.call_count, 3)

        # constants
        self.assertEqual(past.get.call_count, 1)
        self.assertEqual(dateIn.get.call_count, 1)
        self.assertEqual(api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(eventlist.delete.call_count, 1)
        self.assertEqual(reminderlist.delete.call_count, 1)
        self.assertEqual(details.delete.call_count, 1)
        self.assertEqual(deleteBtn.configure.call_count, 1)

    @patch.object(CalendarGUI, 'delete_event_btn')
    @patch.object(CalendarGUI, 'eventdetails')
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    @patch.object(CalendarGUI, 'api')
    @patch.object(CalendarGUI, 'nav_year')
    @patch.object(CalendarGUI, 'nav_month')
    @patch.object(CalendarGUI, 'nav_date')
    @patch.object(CalendarGUI, 'specific_only')
    @patch.object(CalendarGUI, 'dateIn')
    @patch.object(CalendarGUI, 'past_only')
    @patch.object(CalendarGUI, 'searchIn')
    def test_reload_event_list_include_past_events_invalid_past_date(self, searchIn, past, dateIn, specific, ndate,
                                                                     nmonth, nyear, api,
                                                                     eventlist, reminderlist, details,
                                                                     deleteBtn):
        searchIn.get.return_value = ""
        past.get.return_value = 1
        dateIn.get.return_value = "39/15/2980"
        specific.get.return_value = 0
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
        self.assertEqual(specific.get.call_count, 1)
        self.assertEqual(ndate.get.call_count, 0)
        self.assertEqual(nmonth.get.call_count, 0)
        self.assertEqual(nyear.get.call_count, 0)
        self.assertEqual(eventlist.insert.call_count, 2)

        # constants
        self.assertEqual(past.get.call_count, 1)
        self.assertEqual(dateIn.get.call_count, 1)
        self.assertEqual(api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(eventlist.delete.call_count, 1)
        self.assertEqual(reminderlist.delete.call_count, 1)
        self.assertEqual(details.delete.call_count, 1)
        self.assertEqual(deleteBtn.configure.call_count, 1)

    @patch.object(CalendarGUI, 'delete_event_btn')
    @patch.object(CalendarGUI, 'eventdetails')
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    @patch.object(CalendarGUI, 'api')
    @patch.object(CalendarGUI, 'nav_year')
    @patch.object(CalendarGUI, 'nav_month')
    @patch.object(CalendarGUI, 'nav_date')
    @patch.object(CalendarGUI, 'specific_only')
    @patch.object(CalendarGUI, 'dateIn')
    @patch.object(CalendarGUI, 'past_only')
    @patch.object(CalendarGUI, 'searchIn')
    def test_reload_event_list_navigate_specific_events(self, searchIn, past, dateIn, specific, ndate, nmonth, nyear,
                                                        api,
                                                        eventlist, reminderlist, details,
                                                        deleteBtn):
        searchIn.get.return_value = ""
        past.get.return_value = 0
        dateIn.get.return_value = ""
        specific.get.return_value = 1
        ndate.get.return_value = "All"
        nmonth.get.return_value = "10"
        nyear.get.return_value = "2020"
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
        self.assertEqual(specific.get.call_count, 1)
        self.assertEqual(ndate.get.call_count, 1)
        self.assertEqual(nmonth.get.call_count, 1)
        self.assertEqual(nyear.get.call_count, 1)
        self.assertEqual(eventlist.insert.call_count, 2)

        # constants
        self.assertEqual(past.get.call_count, 1)
        self.assertEqual(dateIn.get.call_count, 1)
        self.assertEqual(api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(eventlist.delete.call_count, 1)
        self.assertEqual(reminderlist.delete.call_count, 1)
        self.assertEqual(details.delete.call_count, 1)
        self.assertEqual(deleteBtn.configure.call_count, 1)

    @patch.object(CalendarGUI, 'delete_event_btn')
    @patch.object(CalendarGUI, 'eventdetails')
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    @patch.object(CalendarGUI, 'api')
    @patch.object(CalendarGUI, 'nav_year')
    @patch.object(CalendarGUI, 'nav_month')
    @patch.object(CalendarGUI, 'nav_date')
    @patch.object(CalendarGUI, 'specific_only')
    @patch.object(CalendarGUI, 'dateIn')
    @patch.object(CalendarGUI, 'past_only')
    @patch.object(CalendarGUI, 'searchIn')
    def test_reload_event_list_search_upcoming_events(self, searchIn, past, dateIn, specific,
                                                      ndate, nmonth, nyear, api, eventlist, reminderlist, details,
                                                      deleteBtn):
        searchIn.get.return_value = "test"
        past.get.return_value = 0
        dateIn.return_value = ""
        specific.get.return_value = 0
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
        self.assertEqual(specific.get.call_count, 1)
        self.assertEqual(ndate.get.call_count, 0)
        self.assertEqual(nmonth.get.call_count, 0)
        self.assertEqual(nyear.get.call_count, 0)
        self.assertEqual(eventlist.insert.call_count, 2)

        # constants
        self.assertEqual(past.get.call_count, 1)
        self.assertEqual(dateIn.get.call_count, 1)
        self.assertEqual(api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(eventlist.delete.call_count, 1)
        self.assertEqual(reminderlist.delete.call_count, 1)
        self.assertEqual(details.delete.call_count, 1)
        self.assertEqual(deleteBtn.configure.call_count, 1)

    @patch.object(CalendarGUI, 'delete_event_btn')
    @patch.object(CalendarGUI, 'eventdetails')
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    @patch.object(CalendarGUI, 'api')
    @patch.object(CalendarGUI, 'nav_year')
    @patch.object(CalendarGUI, 'nav_month')
    @patch.object(CalendarGUI, 'nav_date')
    @patch.object(CalendarGUI, 'specific_only')
    @patch.object(CalendarGUI, 'dateIn')
    @patch.object(CalendarGUI, 'past_only')
    @patch.object(CalendarGUI, 'searchIn')
    def test_reload_event_list_search_past_events(self, searchIn, past, dateIn, specific, ndate, nmonth, nyear, api,
                                                  eventlist, reminderlist, details,
                                                  deleteBtn):
        searchIn.get.return_value = "test3"
        past.get.return_value = 1
        dateIn.get.return_value = "10/10/2018"
        specific.get.return_value = 0
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
        self.assertEqual(specific.get.call_count, 0)
        self.assertEqual(ndate.get.call_count, 0)
        self.assertEqual(nmonth.get.call_count, 0)
        self.assertEqual(nyear.get.call_count, 0)
        self.assertEqual(eventlist.insert.call_count, 1)

        # constants
        self.assertEqual(past.get.call_count, 1)
        self.assertEqual(dateIn.get.call_count, 1)
        self.assertEqual(api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(eventlist.delete.call_count, 1)
        self.assertEqual(reminderlist.delete.call_count, 1)
        self.assertEqual(details.delete.call_count, 1)
        self.assertEqual(deleteBtn.configure.call_count, 1)

    @patch.object(CalendarGUI, 'delete_event_btn')
    @patch.object(CalendarGUI, 'eventdetails')
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    @patch.object(CalendarGUI, 'api')
    @patch.object(CalendarGUI, 'nav_year')
    @patch.object(CalendarGUI, 'nav_month')
    @patch.object(CalendarGUI, 'nav_date')
    @patch.object(CalendarGUI, 'specific_only')
    @patch.object(CalendarGUI, 'dateIn')
    @patch.object(CalendarGUI, 'past_only')
    @patch.object(CalendarGUI, 'searchIn')
    def test_reload_event_list_search_in_navigated_events(self, searchIn, past, dateIn, specific, ndate, nmonth, nyear,
                                                          api,
                                                          eventlist, reminderlist, details, deleteBtn):
        searchIn.get.return_value = "test2"
        past.get.return_value = 0
        dateIn.get.return_value = ""
        specific.get.return_value = 1
        ndate.get.return_value = "All"
        nmonth.get.return_value = "10"
        nyear.get.return_value = "2020"
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
        self.assertEqual(specific.get.call_count, 1)
        self.assertEqual(ndate.get.call_count, 1)
        self.assertEqual(nmonth.get.call_count, 1)
        self.assertEqual(nyear.get.call_count, 1)
        self.assertEqual(eventlist.insert.call_count, 1)

        # constants
        self.assertEqual(past.get.call_count, 1)
        self.assertEqual(dateIn.get.call_count, 1)
        self.assertEqual(api.events.return_value.list.return_value.execute.call_count, 1)
        self.assertEqual(eventlist.delete.call_count, 1)
        self.assertEqual(reminderlist.delete.call_count, 1)
        self.assertEqual(details.delete.call_count, 1)
        self.assertEqual(deleteBtn.configure.call_count, 1)


class CalendarGUITestLoadEventDetails(unittest.TestCase):

    @patch.object(CalendarGUI, 'delete_reminder_btn')
    @patch.object(CalendarGUI, 'delete_event_btn')
    @patch.object(CalendarGUI, 'eventdetails')
    @patch.object(CalendarGUI, 'reminderlist')
    @patch.object(CalendarGUI, 'eventlist')
    @patch.object(CalendarGUI, 'events')
    def test_load_event_details_no_selection(self, events, eventlist, reminderlist, details, deleteBtn,
                                             deleteReminderBtn):
        eventlist.curselection.return_value = []
        events.get.return_value = [{
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
        ]
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
        eventlist.curselection.return_value = ["0"]
        CalendarGUI.events = [{
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
        }
        ]
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
        eventlist.curselection.return_value = ["0"]
        CalendarGUI.events = [{
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

    @patch.object(CalendarGUI, 'past_only')
    @patch.object(CalendarGUI, 'dateIn')
    @patch.object(CalendarGUI, 'enable_periods')
    def test_enable_date_textbox_show_past_events_checked(self, periods, dateIn, past):
        past.get.return_value = 1
        CalendarGUI.enable_date_textbox()

        # constant
        self.assertEqual(dateIn.configure.call_count, 1)

        # changes
        self.assertFalse(CalendarGUI.specific_only.get())
        self.assertEqual(periods.call_count, 1)

    @patch.object(CalendarGUI, 'past_only')
    @patch.object(CalendarGUI, 'dateIn')
    @patch.object(CalendarGUI, 'enable_periods')
    def test_enable_date_textbox_show_past_events_not_checked(self, periods, dateIn, past):
        past.get.return_value = 0
        CalendarGUI.enable_date_textbox()

        # constant
        self.assertEqual(dateIn.configure.call_count, 1)
        # changes
        self.assertEqual(periods.call_count, 0)


class CalendarGUITestEnablePeriods(unittest.TestCase):

    @patch.object(CalendarGUI, 'specific_only')
    @patch.object(CalendarGUI, 'enable_date_textbox')
    @patch.object(CalendarGUI, 'nv_year')
    @patch.object(CalendarGUI, 'nv_month')
    @patch.object(CalendarGUI, 'nv_date')
    def test_enable_date_textbox_show_specific_events_checked(self, ndate, nmonth, nyear, enable_date, specific):
        specific.get.return_value = 1
        CalendarGUI.enable_periods()

        # constant
        self.assertEqual(ndate.configure.call_count, 1)
        self.assertEqual(nmonth.configure.call_count, 1)
        self.assertEqual(nyear.configure.call_count, 1)

        # changes
        self.assertFalse(CalendarGUI.past_only.get())
        self.assertEqual(enable_date.call_count, 1)

    @patch.object(CalendarGUI, 'specific_only')
    @patch.object(CalendarGUI, 'enable_date_textbox')
    @patch.object(CalendarGUI, 'nv_year')
    @patch.object(CalendarGUI, 'nv_month')
    @patch.object(CalendarGUI, 'nv_date')
    def test_enable_date_textbox_show_specific_events_not_checked(self, ndate, nmonth, nyear, enable_date, specific):
        specific.get.return_value = 0
        CalendarGUI.enable_periods()

        # constant
        self.assertEqual(ndate.configure.call_count, 1)
        self.assertEqual(nmonth.configure.call_count, 1)
        self.assertEqual(nyear.configure.call_count, 1)

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
        datestr = "12.1.1998"
        self.assertTrue(CalendarGUI.verify_date(datestr))
        self.assertEqual("12", CalendarGUI.verify_date(datestr)[0])
        self.assertEqual("1", CalendarGUI.verify_date(datestr)[1])
        self.assertEqual("1998", CalendarGUI.verify_date(datestr)[2])


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



class CalendarGUITestMain(unittest.TestCase):

    def test_main_function(self):
        CalendarGUI.main()


def main():
    # Create the test suite from the cases above.
    test_classes = [CalendarGUITestGetDetailedEvent, CalendarGUITestReloadEventList, CalendarGUITestLoadEventDetails, CalendarGUITestDeleteEvent,
                    CalendarGUITestDeleteReminder, CalendarGUITestEnableDateTextbox, CalendarGUITestEnablePeriods, CalendarGUITestGetPeriods,
                    CalendarGUITestVerifyDate, CalendarGUITestEnableDeleteReminder]  # Test Classes
    for classes in test_classes:
        suite = unittest.TestLoader().loadTestsFromTestCase(classes)
        # This will run the test suite.
        unittest.TextTestRunner(verbosity=2).run(suite)

main()
