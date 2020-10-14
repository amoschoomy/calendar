@echo off
coverage run -m --branch CalendarTestDateFormatter
coverage run -a -m --branch CalendarTestGetDetailedEvent
coverage run -a -m --branch CalendarTestGetPastEvents
coverage run -a -m --branch CalendarTestGetUpcomingEvents
coverage run -a -m --branch CalendarTestGetPastReminders
coverage run -a -m --branch CalendarTestGetUpcomingReminders
coverage run -a -m --branch CalendarTestNavigateCalendar
coverage run -a -m --branch CalendarTestGetDetailedReminder
coverage run -a -m --branch CalendarTestSearchEvents
coverage run -a -m --branch CalendarTestSearchReminders
coverage run -a -m --branch CalendarTestDeleteEvents
coverage run -a -m --branch CalendarTestDeleteReminders
coverage run -a -m --branch CalendarTestRunCalendar
coverage run -a -m --branch CalendarTestGetSelectedEvents
coverage run -a -m --branch CalendarTestGetSelectedReminders
coverage run -a -m --branch CalendarGUITestAll
coverage report 
coverage html
ECHO Opening html file.
PAUSE
"%~dp0htmlcov\index.html"