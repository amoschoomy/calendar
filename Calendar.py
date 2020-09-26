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
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


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
    
    # Add your methods here.

def get_past_events(api,starting_time,end_time=datetime.datetime.utcnow().isoformat() + 'Z'):
    """
    Shows past events given the time from today's date if date not specified
    """
    if end_time<=starting_time:
        raise ValueError("End time provided is less than the starting time")
    events_result=api.events().list(calendarId='primary',timeMin=starting_time,timeMax=end_time,singleEvents=True,orderBy='startTime').execute()
    return events_result.get('items',[])

def get_past_reminders(api,starting_time,end_time=datetime.datetime.utcnow().isoformat() + 'Z'):
    """
    Shows past reminders given a start date and/if end time specified
    
    """
    # Block of code below adapted from: https://stackoverflow.com/a/48750522/
    if len(starting_time.split('-')) != 3: # check if the len is 3. 
        raise ValueError("starting time provided is not of format")

    if len(end_time.split('-')) != 3: # check if the len is 3. 
        raise ValueError("starting time provided is not of format")
    
    reminder_list=[]
    if end_time<=starting_time:
        raise ValueError("End time provided is less than the starting time")
    events_result=api.events().list(calendarId='primary',timeMin=starting_time,timeMax=end_time,singleEvents=True,orderBy='startTime').execute()
    events=events_result.get('items',[])
    for event in events:
        if event['reminders'].get("useDefault")==True:
            reminder_list.append(event["summary"]+","+"Reminder through popup 10 minutes before event starts")
        else:
           for i in event["reminders"].get("overrides"):
                reminder_list.append(event["summary"]+","+"Reminder through "+i.get("method")+" "+str(i.get("minutes"))+
                " minutes before event starts")
    return reminder_list

def get_upcoming_reminders(api,starting_time=datetime.datetime.utcnow().isoformat() + 'Z'):
    """
    Shows upcoming reminders from todays date and time if starting date is not specified

    """
    # Block of code below adapted from: https://stackoverflow.com/a/48750522/

    if len(starting_time.split('-')) != 3: # check if the len is 3. 
        raise ValueError("starting time provided is not of format")

    reminder_list=[]
    events_result=api.events().list(calendarId='primary',timeMin=starting_time,singleEvents=True,orderBy='startTime').execute()
    events=events_result.get('items',[])
    for event in events:
        if event['reminders'].get("useDefault")==True:
            reminder_list.append(event["summary"]+","+"Reminder through popup 10 minutes before event starts")
        else:
            for i in event["reminders"].get("overrides"):
                reminder_list.append(event["summary"]+","+"Reminder through "+i.get("method")+" "+str(i.get("minutes"))+
                " minutes before event starts")
    return reminder_list
    
def main():
    api = get_calendar_api()
    time_now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    past_time="2019-09-25T09:59:04.501209Z"
    events = get_upcoming_events(api, time_now, 10)
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

if __name__ == "__main__":  # Prevents the main() function from being called by the test suite runner
    main()
