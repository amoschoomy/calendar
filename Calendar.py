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


def get_upcoming_events(api, starting_time, number_of_events):
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next n events on the user's calendar.
    """
    if (number_of_events <= 0):
        raise ValueError("Number of events must be at least 1.")

    events_result = api.events().list(calendarId='primary', timeMin=starting_time,
                                      maxResults=number_of_events, singleEvents=True,
                                      orderBy='startTime').execute()
    return events_result.get('items', [])


def get_upcoming_events_2(api, starting_time=datetime.datetime.utcnow().isoformat() + 'Z'):
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
        results += event['summary'] + "," + start+"\n"
    return results

    # Add your methods here.


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
        results += event['summary'] + "," + start +"\n"
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
            reminders += event["summary"] + "," + "Reminder through popup 10 minutes before event starts"
        else:
            for i in event["reminders"].get("overrides", []):
                reminders += event["summary"] + "," + "Reminder through " + i.get("method") + " " + str(
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
            reminders += event["summary"] + "," + "Reminder through popup 10 minutes before event starts"
        else:
            for i in event["reminders"].get("overrides", []):
                reminders += event["summary"] + "," + "Reminder through " + i.get("method") + " " + str(
                    i.get("minutes")) + " minutes before event starts"
        reminders += "\n"
    return reminders

def navigate_calendar(api,date,navigation_type):
    result=""
    month=str(date.month)
    year=str(date.year)
    day=str(date.day)

    if navigation_type == "MONTH":
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
        try:
            dates = datetime.datetime.strptime(year + "-" + "12" + "-" + "31" + " 23:59:59", '%Y-%m-%d %H:%M:%S')
            result += "EVENTS: \n"
            result += get_past_events(api, date.isoformat() + "Z", dates.isoformat() + "Z")
            result += "\n"
            result += get_past_reminders(api, date.isoformat() + "Z", dates.isoformat() + "Z")
            result += "REMINDERS: \n"
        except ValueError:
            dates = datetime.datetime.strptime(year + "-" + "12" + "-" + "30" + " 23:59:59", '%Y-%m-%d %H:%M:%S')
            result += "EVENTS: \n"
            result += get_past_events(api, date.isoformat() + "Z", dates.isoformat() + "Z")
            result += "\n"
            result += "REMINDERS: \n"
            result += get_past_reminders(api, date.isoformat() + "Z", dates.isoformat() + "Z")
            result += "\n"

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


def get_detailed_event(api, query):
    events_result = api.events().list(calendarId='primary', singleEvents=True, orderBy='startTime', q=query).execute()
    event = events_result.get("items", [])
    detailed_description = ""
    detailed_description += "Title: " + event['summary'] + "\n"
    detailed_description += "Visibility:" + event["visibility"] + "\n"
    detailed_description += "Status: " + event["status"] + "\n"
    detailed_description += "Start:" + event['start'].get('dateTime', event['start'].get('date')) + "\n"
    detailed_description += "End:" + event['end'].get('dateTime', event['end'].get('date')) + "\n"
    detailed_description += "Location" + event["location"] + "\n"
    for attendees in event["attendees"]:
        detailed_description += attendees.email + "\n"
    return detailed_description


def get_searched_events(api, query):
    results = ""
    events = api.events().list(calendarId='primary', singleEvents=True, orderBy='startTime', q=query).execute()
    result = events.get('items', [])

    return result


def get_searched_reminders(api, query):
    reminders = ""
    events = api.events().list(calendarId='primary', singleEvents=True, orderBy='startTime', q=query).execute()
    result = events.get('items', [])
    for event in result:

        if event['reminders'].get("useDefault") == True:
            reminders += event["summary"] + "," + "Reminder through popup 10 minutes before event starts"
        else:
            for i in event["reminders"].get("overrides", []):
                reminders += event["summary"] + "," + "Reminder through " + i.get("method") + " " + str(
                    i.get("minutes")) + " minutes before event starts"
        reminders += "\n"

    return reminders


def delete_events(api, eventID):
    api.events().delete(calendarId='primary', eventId=eventID).execute()


def delete_reminders(api, eventID):
    event = api.events().get(calendarId='primary', eventId=eventID).execute()

    event['reminders'] = {"useDefault": False,
                          "overrides": []}

    return api.events().update(calendarId='primary', eventId=event['id'], body=event).execute()


def run_calendar(api):
    print("Welcome to MLLMAOTEAM Google Calendar Viewer v1.0")
    directives = ['upcoming', 'past', 'search', 'delete', 'date', 'month', 'year']
    selected = None

    while True:
        command = input("command>").split(" ")
        n = len(command)
        results = ""

        if not n:
            continue

        directive = command[0]

        if directive == 'upcoming':

            if n > 1 and command[1] == '-r':
                results = get_upcoming_reminders(api)
            else:
                results = get_upcoming_events_2(api)

        elif directive == 'past':

            if n > 1 and command[1] == '-r':
                results = get_past_reminders(api)
            else:
                results = get_past_events(api)

        elif directive == 'search':

            if n > 2 and command[1] == '-r':
                results = get_searched_reminders(api, command[2])
            elif n > 1:
                results = get_searched_events(api, command[1])
            else:
                print("No search keyword.")
                continue

        elif directive == 'delete':

            if selected is None:
                print("No events selected")
            elif n > 1 and command[1] == '-r':
                if input("Delete reminders for selected event: " + selected['summary'] + "?").lower() == "y":
                    delete_reminders(api, selected['id'])
                    selected = None
                    print("Deleted reminders sucessfully")
            else:
                if input("Delete selected event: " + selected['summary'] + "?").lower() == "y":
                    delete_events(api, selected['id'])
                    selected = None
                    print("Deleted event sucessfully")
            continue

        else:
            print("Invalid directive")
            continue

        selected = get_selected_event(results)


def get_selected_event(results):
    dict = {}
    prompt = ""
    for event in range(len(results)):
        dict[event] = results[event]

        start = results[event]['start'].get('dateTime', results[event]['start'].get('date'))
        prompt += str(event) + ": " + results[event]['summary'] + "," + start + "\n"

    print(prompt)

    userselect = None
    try:
        index = int(input("Select an event: "))
        userselect = dict[index]
        print("Selected event: " + dict[index]['summary'])

    except ValueError:
        print("No event selected")
    except KeyError:
        print("No event selected")

    return userselect


def main():
    api = get_calendar_api()
    time_now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    past_time = "2019-09-25T09:59:04.501209Z"
    events = get_upcoming_events(api, time_now, 10)
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

    run_calendar(api)
    # print("SEARCH EVENTS")
    # print(get_searched_events(api, "hydrogen"))
    # print("SEARCH REMINDERS")
    # print(get_searched_reminders(api, "hydrogen"))

    # print(delete_reminders(api,
    #                        "_60q30c1g60o30e1i60o4ac1g60rj8gpl88rj2c1h84s34h9g60s30c1g60o30c1g8h1k2g9j6d1jegi275148dhg64o30c1g60o30c1g60o30c1g60o32c1g60o30c1g8ksjie1h6gr42ghm74o3ce9k8gsjch246ks4ch9m68s3igph8p10")[
    #           'reminders'])


if __name__ == "__main__":  # Prevents the main() function from being called by the test suite runner
    main()
