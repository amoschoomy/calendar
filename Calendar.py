# Make sure you are logged into your Monash student account.
# Go to: https://developers.google.com/calendar/quickstart/python
# Click on "Enable the Google Calendar API"
# Configure your OAuth client - select "Desktop app", then proceed
# Click on "Download Client Configuration" to obtain a credential.json file
# Do not share your credential.json file with anybody else, and do not commit it to your A2 git repository.
# When app is run for the first time, you will need to sign in using your Monash student account.
# Allow the "View your calendars" permission request.


# Students must have their own api key
# No test cases needed for authentication, but authentication may required for running the app very first time.
# http://googleapis.github.io/google-api-python-client/docs/dyn/calendar_v3.html


# Code adapted from https://developers.google.com/calendar/quickstart/python
from __future__ import print_function
import datetime
import pickle
import os.path
from time import strptime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def get_calendar_api():
    """
    Get an object which allows you to consume the Google Calendar API.
    You do not need to worry about what this function exactly does, nor create test cases for it.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)


def get_upcoming_events(api, starting_time=datetime.datetime.utcnow().isoformat() + 'Z'):
    """
    Get all upcoming events

    """
    results = ""
    # Block of code below adapted from: https://stackoverflow.com/a/48750522/
    if len(starting_time.split('-')) != 3:  # check if the len is 3.
        raise ValueError("starting time provided is not of format")

    events_result = api.events().list(calendarId='primary', timeMin=starting_time,
                                      singleEvents=True,
                                      orderBy='startTime').execute()
    result = events_result.get('items', [])

    for event in result:
        start = event['start'].get('dateTime', event['start'].get('date'))
        results += event.get('summary', "No title") + "," + start + "\n"
    return results


def get_past_events(api, starting_time, end_time=datetime.datetime.utcnow().isoformat() + 'Z'):
    """
    Shows past events given the time from today's date if date not specified
    """
    results = ""
    # Block of code below adapted from: https://stackoverflow.com/a/48750522/
    if len(starting_time.split('-')) != 3:  # check if the len is 3.
        raise ValueError("starting time provided is not of format")

    # Block of code below adapted from: https://stackoverflow.com/a/48750522/
    if len(end_time.split('-')) != 3:  # check if the len is 3.
        raise ValueError("starting time provided is not of format")

    if end_time < starting_time:
        raise ValueError("End time provided is less than the starting time")

    events_result = api.events().list(calendarId='primary', timeMin=starting_time, timeMax=end_time, singleEvents=True,
                                      orderBy='startTime').execute()
    result = events_result.get('items', [])

    for event in result:
        start = event['start'].get('dateTime', event['start'].get('date'))
        results += event.get('summary', "No title") + "," + start + "\n"
    return results


def get_past_reminders(api, starting_time, end_time=datetime.datetime.utcnow().isoformat() + 'Z'):
    """
    Shows past reminders given a start date and/if end time specified

    """
    # Block of code below adapted from: https://stackoverflow.com/a/48750522/
    if len(starting_time.split('-')) != 3:  # check if the len is 3.
        raise ValueError("starting time provided is not of format")

    if len(end_time.split('-')) != 3:  # check if the len is 3.
        raise ValueError("starting time provided is not of format")

    reminders = ""
    if end_time < starting_time:
        raise ValueError("End time provided is less than the starting time")
    events_result = api.events().list(calendarId='primary', timeMin=starting_time, timeMax=end_time, singleEvents=True,
                                      orderBy='startTime').execute()
    events = events_result.get('items', [])
    for event in events:
        if event['reminders'].get("useDefault") == True:
            reminders += event.get('summary',
                                   "No title") + "," + "Reminder through popup 10 minutes before event starts"
        else:
            for i in event["reminders"].get("overrides", []):
                reminders += event.get('summary', "No title") + "," + "Reminder through " + i.get("method") + " " + str(
                    i.get("minutes")) + " minutes before event starts"
        reminders += "\n"
    return reminders


def get_upcoming_reminders(api, starting_time=datetime.datetime.utcnow().isoformat() + 'Z'):
    """
    Shows upcoming reminders from todays date and time if starting date is not specified

    """
    # Block of code below adapted from: https://stackoverflow.com/a/48750522/

    if len(starting_time.split('-')) != 3:  # check if the len is 3.
        raise ValueError("starting time provided is not of format")

    reminders = ""
    events_result = api.events().list(calendarId='primary', timeMin=starting_time, singleEvents=True,
                                      orderBy='startTime').execute()
    events = events_result.get('items', [])
    for event in events:
        if event['reminders'].get("useDefault") == True:
            reminders += event.get('summary',
                                   "No title") + "," + "Reminder through popup 10 minutes before event starts"
        else:
            for i in event["reminders"].get("overrides", []):
                reminders += event.get('summary', "No title") + "," + "Reminder through " + i.get("method") + " " + str(
                    i.get("minutes")) + " minutes before event starts"
        reminders += "\n"
    return reminders


def navigate_calendar(api, date, navigation_type):
    result = ""
    month = str(date.month)
    year = str(date.year)
    day = str(date.day)

    if navigation_type == "MONTH" and month == "2":
        try:
            dates = datetime.datetime.strptime(year + "-" + month + "-" + "28" + " 23:59:59", '%Y-%m-%d %H:%M:%S')
            result += "EVENTS: \n"
            result += get_past_events(api, date.isoformat() + "Z", dates.isoformat() + "Z")
            result += "\n"
            result += "REMINDERS: \n"
            result += get_past_reminders(api, date.isoformat() + "Z", dates.isoformat() + "Z")
        except ValueError:
            dates = datetime.datetime.strptime(year + "-" + month + "-" + "29" + " 23:59:59", '%Y-%m-%d %H:%M:%S')
            result += "EVENTS: \n"
            result += get_past_events(api, date.isoformat() + "Z", dates.isoformat() + "Z")
            result += "\n"
            result += "REMINDERS: \n"
            result += get_past_reminders(api, date.isoformat() + "Z", dates.isoformat() + "Z")
            result += "\n"
    elif navigation_type == "MONTH":
        try:
            dates = datetime.datetime.strptime(year + "-" + month + "-" + "31" + " 23:59:59", '%Y-%m-%d %H:%M:%S')
            result += "EVENTS: \n"
            result += get_past_events(api, date.isoformat() + "Z", dates.isoformat() + "Z")
            result += "\n"
            result += "REMINDERS: \n"
            result += get_past_reminders(api, date.isoformat() + "Z", dates.isoformat() + "Z")
        except ValueError:
            dates = datetime.datetime.strptime(year + "-" + month + "-" + "30" + " 23:59:59", '%Y-%m-%d %H:%M:%S')
            result += "EVENTS: \n"
            result += get_past_events(api, date.isoformat() + "Z", dates.isoformat() + "Z")
            result += "\n"
            result += "REMINDERS: \n"
            result += get_past_reminders(api, date.isoformat() + "Z", dates.isoformat() + "Z")
            result += "\n"

    elif navigation_type == "YEAR":
        dates = datetime.datetime.strptime(year + "-" + "12" + "-" + "31" + " 23:59:59", '%Y-%m-%d %H:%M:%S')
        result += "EVENTS: \n"
        result += get_past_events(api, date.isoformat() + "Z", dates.isoformat() + "Z")
        result += "\n"
        result += get_past_reminders(api, date.isoformat() + "Z", dates.isoformat() + "Z")
        result += "REMINDERS: \n"

    elif navigation_type == "DAY":
        dates = datetime.datetime.strptime(year + "-" + month + "-" + day + " 23:59:59", '%Y-%m-%d %H:%M:%S')
        result += "EVENTS: \n"
        result += get_past_events(api, date.isoformat() + "Z", dates.isoformat() + "Z")
        result += "\n"
        result += "REMINDERS: \n"
        result += get_past_reminders(api, date.isoformat() + "Z", dates.isoformat() + "Z")
    else:
        raise ValueError("Navigation type is wrong")
    return result


def get_detailed_event(event):
    detailed_description = ""
    if event.get("summary") == None:  # None means no key for event title, subsequent event data cannnot be retrieved
        raise ValueError("Wrong argument passed into")
    # NOTE:
    # if parameter passed in is of other type, Attribute Errors will be raised
    detailed_description += "Title: " + event.get('summary', "No title") + "\n"

    if event.get("visibility") is not None:
        detailed_description += "Visibility: " + event.get("visibility") + "\n"
    detailed_description += "Status: " + event["status"] + "\n"
    detailed_description += "Created: " + event["created"] + "\n"
    detailed_description += "Creator: " + event["creator"].get("email") + "\n"
    detailed_description += "Start: " + event['start'].get('dateTime', event['start'].get('date')) + "\n"
    detailed_description += "End: " + event['end'].get('dateTime', event['end'].get('date')) + "\n"
    if event.get("location") is not None:
        detailed_description += "Location: " + event.get("location") + "\n"
    if event.get("attendees") is not None:
        detailed_description += "Attendees: "
        for attendees in event["attendees"]:
            detailed_description += attendees.get("email") + ", "
    detailed_description = detailed_description[:-2]  # strip commas at the end
    detailed_description += "\n"
    return detailed_description


def get_searched_events(api, query):
    if query is None:
        raise TypeError
    elif query.strip() == "":
        raise ValueError
    else:
        events = api.events().list(calendarId='primary', singleEvents=True, orderBy='startTime', q=query).execute()
        results = ""
        result = events.get('items', [])

        for event in result:
            start = event['start'].get('dateTime', event['start'].get('date'))
            results += event.get("summary", "No title") + "," + start
            results += "\n"
        return results


def get_searched_reminders(api, query):
    if query is None:
        raise TypeError
    elif query.strip() == "":
        raise ValueError

    else:
        reminders = ""
        events = api.events().list(calendarId='primary', singleEvents=True, orderBy='startTime', q=query).execute()
        result = events.get('items', [])
        for event in result:

            if event['reminders'].get("useDefault") == True:
                reminders += event.get("summary",
                                       "No title") + "," + "Reminder through popup 10 minutes before event starts"
            else:
                for i in event["reminders"].get("overrides", []):
                    reminders += event.get("summary", "No title") + "," + "Reminder through " + i.get(
                        "method") + " " + str(
                        i.get("minutes")) + " minutes before event starts"
            reminders += "\n"

        return reminders


def delete_events(api, event):
    if event is None:
        raise TypeError
    elif not event.get("id", False):
        raise ValueError
    else:
        api.events().delete(calendarId='primary', eventId=event["id"]).execute()


def delete_reminders(api, event, reminder_index=-1):
    if event is None:
        raise TypeError
    elif reminder_index is None:
        raise TypeError

    reminders = event["reminders"].get("overrides", [])
    if event['reminders'].get("useDefault", False):
        event['reminders'] = {"useDefault": False, "overrides": []}
        retval = api.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
        return retval.get('updated', None)
    elif reminder_index >= len(reminders):
        raise IndexError
    else:
        event["reminders"]["overrides"].pop(reminder_index)
        retval = api.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
        return retval.get('updated', None)


def get_detailed_reminders(event):
    detailed_description = ""
    if event.get("start") == None:  # None means no key for event start time, subsequent event data cannnot be retrieved
        raise ValueError("Wrong argument passed into")
    # NOTE:
    # if parameter passed in is of other type, Attribute Errors will be raised
    if event['reminders'].get("useDefault") == True:
        detailed_description += event["summary"] + "," + "Reminder through popup 10 minutes before event starts"
    else:
        for i in event["reminders"].get("overrides", []):
            detailed_description += event.get('summary', 'No title') + "," + "Reminder through " + i.get(
                "method") + " " + str(
                i.get("minutes")) + " minutes before event starts"
    detailed_description += "\n"
    return detailed_description


def run_calendar(api):
    print("Welcome to MLLMAOTEAM Google Calendar Viewer v1.0")
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    print("Todays date(YY-MM-DD): " + today)
    print("Commands available:")
    directives = ['upcoming -e', 'past -e', 'search -e', "upcoming -r", "past -r", "search -r",
                  "help", "navigate", "exit"]
    for directive in directives:
        print(directive)
    print("-e is for events, while -r is for reminders")
    while True:
        command = input("command>")
        if command not in directives:
            print("Invalid command. Please try again!")
            continue
        if command == "upcoming -e":
            print(get_upcoming_events(api))
        elif command == "upcoming -r":
            print(get_upcoming_reminders(api))
        elif command == "past -e":
            while True:
                try:
                    past_date = input("Enter the date how long in the past in YYYY-MM-DD format only: ")
                    date = datetime.datetime.strptime(past_date, "%Y-%m-%d").isoformat() + ".000000Z"
                    print(get_past_events(api, date))
                    break
                except ValueError:
                    print("Wrong format please try again")
        elif command == "past -r":
            while True:
                try:
                    past_date = input("Enter the date how long in the past in YYYY-MM-DD format only: ")
                    date = datetime.datetime.strptime(past_date, "%Y-%m-%d").isoformat() + ".000000Z"
                    print(get_past_reminders(api, date))
                    break
                except ValueError:
                    print("Wrong format please try again")
        elif command == "search -e":
            query = input("Enter search query: ")
            print(get_searched_events(api, query))
        elif command == "search -r":
            query = input("Enter search query: ")
            print(get_searched_reminders(api, query))
        elif command == "navigate":
            nav_type = ["MONTH", "DAY", "YEAR"]
            while True:
                print("Navigate calender by : ")
                for i in range(len(nav_type)):
                    print(str(i) + ": " + nav_type[i])
                try:
                    nav = int(input())
                    if not (nav in [0,1,2]):
                        raise ValueError
                    nav_date = input("Enter date of navigation exactly in DD Month YYYY format(eg. 21 January 2020): ")
                    date_inputted = datetime.datetime.strptime(nav_date, '%d %B %Y')
                    date = date_formatter(date_inputted, nav_type[nav])
                    print(navigate_calendar(api, date, nav_type[nav]))
                    decision = input("View Event? y/n \n")
                    if decision == "y":
                        event = input("Input full name of the event: ")
                        events = api.events().list(calendarId='primary', singleEvents=True, orderBy='startTime',
                                                   q=event).execute()
                        try:
                            sole_event = get_selected_event(events.get('items', []))
                            print(get_detailed_event(sole_event))
                            print(get_detailed_reminders(sole_event))
                            des = input("Enter 'del' to delete event, 'del -r' to delete reminders.").strip().lower()
                            if des == "del":
                                delete_events(api, sole_event)
                                print("Deleted event successfully")
                                break
                            elif des == "del -r":
                                reminder_index = get_selected_reminders(sole_event)
                                if reminder_index is not None:
                                    delete_reminders(api, sole_event, reminder_index)
                                    print("Deleted reminder succesfully")
                                break
                            else:
                                print("No delete instruction, returning to calendar...")
                                break
                        except AttributeError:
                            print("Failure. No event/reminder selected")
                    else:
                        print("Exiting Navigation")
                        break
                except ValueError:
                    print("Wrong input. Try again")
                    continue
        elif command == "help":
            print("Commands available:")
            for directive in directives:
                print(directive)
            print("-e is for events, while -r is for reminders")
            print("\n")
            print("Contact devs at acho0057@student.monash.edu and apan0027@student.monash.edu for further help")
        elif command == "exit":
            break


def get_selected_event(results):
    dict = {}
    prompt = ""

    for event in range(len(results)):
        dict[event] = results[event]

        start = results[event]['start'].get('dateTime', results[event]['start'].get('date'))
        prompt += str(event) + ": " + results[event].get('summary', "No title") + "," + start + "\n"
    # if dict
    print(prompt)

    userselect = None
    try:
        index = int(input("Select an event: "))
        userselect = dict[index]
    except ValueError:
        pass
    except KeyError:
        pass

    return userselect


def get_selected_reminders(event):
    dict = {}
    prompt = ""
    reminderobj = event.get("reminders", {})

    if reminderobj.get("useDefault", False):
        return -1

    overrides = reminderobj.get("overrides", [])

    for i in range(len(overrides)):
        prompt += str(i) + ". Reminder through " + overrides[i].get("method") + " " + str(
            overrides[i].get("minutes")) + " minutes before event starts\n"
        dict[i] = overrides[i]

    print(prompt)
    selected = None
    try:
        index = int(input("Select a reminder to delete: "))
        print("Selected reminder: Reminder through " + dict[index]['method'] + " " + str(dict[index]['minutes']) + " minutes before event starts\n")
        selected = index
    except ValueError:
        pass
    except KeyError:
        pass

    return selected


def date_formatter(date_inputted, nav_type):
    if nav_type == "MONTH":
        return datetime.datetime.strptime("01" + str(date_inputted.month) + str(date_inputted.year), '%d%m%Y')
    elif nav_type == "YEAR":
        return datetime.datetime.strptime("01" + "01" + str(date_inputted.year), '%d%m%Y')
    else:
        return date_inputted


def main():
    api = get_calendar_api()
    run_calendar(api)


if __name__ == "__main__":  # Prevents the main() function from being called by the test suite runner
    try:main()
    except KeyboardInterrupt:
        pass
