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
from tkinter import *
from tkinter import ttk
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

root = Tk()
events = None

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


def get_detailed_event(event):
    detailed_description = ""
    if event.get("summary") == None:  # None means no key for event title, subsequent event data cannnot be retrieved
        raise ValueError("Wrong argument passed into")
    # NOTE:
    # if parameter passed in is of other type, Attribute Errors will be raised
    detailed_description += "Title: " + event['summary'] + "\n"

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


def updateEvents():
    global events

    past_date_tokens = verify_date(dateIn.get())

    query = None
    starting_time = datetime.datetime.utcnow().isoformat() + 'Z'
    end_time = None

    if searchIn.get().lower() != "":
        query = searchIn.get()

    if past_only.get() and past_date_tokens:
        starting_time = datetime.datetime.strptime(
            past_date_tokens[2] + "-" + past_date_tokens[1] + "-" + past_date_tokens[0],
            "%Y-%m-%d").isoformat() + ".000000Z"
    elif specific_only.get():
        period = get_periods()
        starting_time = period[0]
        end_time = period[1]

    events = api.events().list(calendarId='primary', timeMin=starting_time, timeMax=end_time, singleEvents=True,
                               orderBy='startTime', q=query).execute().get("items", [])

    eventlist.delete(0, END)
    for i in events:
        eventlist.insert(END, i["summary"])

    reminderlist.delete(0, END)
    eventdetails.delete(1.0, END)
    delete_event_btn.configure(state="disable")


def showEvent(*args):

    idxs = eventlist.curselection()
    if len(idxs) == 1:
        idx = int(idxs[0])
        text = get_detailed_event(events[idx])
        eventdetails.delete(1.0, END)
        eventdetails.insert(END, text)

        if events[idx]["reminders"].get("useDefault", False):
            reminders = ["Popup 10 minutes before event starts"]
        else:
            overrides = events[idx]["reminders"].get("overrides", [])
            reminders = []
            for each in overrides:
                reminders += each.get("method") + " " + str(each.get("minutes")) + " minutes before event starts"

        reminderlist.delete(0, END)
        for each in reminders:
            reminderlist.insert(END, each)
        delete_event_btn.configure(state="normal")
        delete_reminder_btn.configure(state="disable")


def deleteEvent():
    idxs = eventlist.curselection()
    if len(idxs) == 1:
        idx = int(idxs[0])
        api.events().delete(calendarId='primary', eventId=events[idx]["id"]).execute()
        updateEvents()


def deleteReminder():
    idxs = eventlist.curselection()
    print(idxs)
    if len(idxs) == 1:
        print("Entered")
        idx = int(idxs[0])
        selected_event = events[idx]

    idxs = reminderlist.curselection()
    if len(idxs) == 1:
        idx = int(idxs[0])
        if selected_event["reminders"].get("useDefault", False):
            selected_event['reminders'] = {"useDefault": False, "overrides": []}
        else:
            selected_event['reminders']["overrides"].pop(idx)
        api.events().update(calendarId='primary', eventId=selected_event['id'], body=selected_event).execute()
        # delete_reminders(api, selected_event, idx)
        showEvent()


def enableTextbox():
    if past_only.get():
        dateIn.configure(state="normal")
        specific_only.set(0)
        enablePeriods()
    else:
        dateIn.configure(state="disable")



def enablePeriods():
    if specific_only.get():
        nv_date.configure(state="normal")
        nv_month.configure(state="normal")
        nv_year.configure(state="normal")
        past_only.set(0)
        enableTextbox()
    else:
        nv_date.configure(state="disable")
        nv_month.configure(state="disable")
        nv_year.configure(state="disable")

def get_periods():
    date = nav_date.get()
    month = nav_month.get()
    year = nav_year.get()

    if month == "All":
        month = "1"
        endmonth = "12"
    else:
        endmonth = month

    if date == "All":
        date = "1"
        if endmonth in ["1","3","5","7","8","10","12"]:
            endday = "31"
        elif endmonth == "2":
            endday = "28"
        else:
            endday = "30"
    else:
        endday = date

    if year == "All":
        startdate = None
        enddate = None
    else:
        startdate = datetime.datetime.strptime(year + "-" + month + "-" + date + " 23:59:59", '%Y-%m-%d %H:%M:%S').isoformat() + "Z"
        enddate = datetime.datetime.strptime(year + "-" + endmonth + "-" + endday + " 23:59:59", '%Y-%m-%d %H:%M:%S').isoformat() + "Z"
    return startdate, enddate


def verify_date(string):
    tokens = string.split("-")
    if len(tokens) != 3:
        tokens = string.split("/")
    if len(tokens) != 3:
        tokens = string.split(".")
    if len(tokens) != 3:
        return False
    if len(tokens[0]) == 2 and len(tokens[1]) == 2 and len(tokens[2]) == 4:
        return tokens
    return False


def showReminder(*args):
    idxs = reminderlist.curselection()
    if len(idxs) == 1:
        delete_reminder_btn.configure(state="normal")


# Create and grid the outer content frame
c = ttk.Frame(root, padding=(5, 5, 12, 0))
c.grid(column=0, row=0, sticky=(N, W, E, S))
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

# Search Elements
sch = ttk.Frame(c)
sch.grid(row=0,columnspan=2,sticky=(W, E))

Label(sch, text="Search events: ").grid(row=0,column=0, sticky=E)
searchIn = ttk.Entry(sch,width=50)
searchIn.grid(row=0, column=1, padx=5, sticky=(W,E))
searchBtn = ttk.Button(c, text="Search", command=updateEvents)
searchBtn.grid(row=0, column=2, padx=5, sticky=E)

# Events List Elements
Label(c, text="Events").grid(row=1, sticky=W)
eventlist = Listbox(c, height=8, exportselection=False)
eventlist.grid(row=2, columnspan=2, rowspan=8, sticky=(W, E))
ttk.Button(c, text="Refresh", command=updateEvents).grid(row=2, column=2, padx=5, sticky=(N, E))
delete_event_btn = ttk.Button(c, text="Delete", command=deleteEvent, state="disable")
delete_event_btn.grid(row=3, column=2, padx=5, sticky=(N, E))

# Show past events elements
past_only = IntVar()
checkbtn = Checkbutton(c, text="Show past events since: (DD/MM/YYYY)", variable=past_only, command=enableTextbox).grid(row=10,
                                                                                                                sticky=W)
dateIn = ttk.Entry(c, state="disabled")
dateIn.grid(row=10, column=1, pady=5, padx=5, sticky=(W, E))
updateBtn = ttk.Button(c, text="Update", command=updateEvents)
updateBtn.grid(row=10, rowspan=2,column=2, padx=5, sticky=(N,S,E))

# Navigate events elements
nv = ttk.Frame(c)
nv.grid(row =11,columnspan=2,sticky=(W, E))
specific_only = IntVar()
navigate_checkbtn = Checkbutton(nv, text="Show only events on: ", variable=specific_only, command=enablePeriods).grid(column=0,row=0,sticky=W)

Label(nv, text="Date").grid(column=1,row=0, sticky=E)
dates = ["All"] + [str(i) for i in range(1,32)]
nav_date = StringVar()
nav_date.set(dates[0])
nv_date = OptionMenu(nv,nav_date,*dates)
nv_date.grid(column=2,row=0, sticky=E)

Label(nv, text="Month").grid(column=3,row=0, sticky=E)
months = ["All"] + [str(i) for i in range(1,13)]
nav_month = StringVar()
nav_month.set(months[0])
nv_month = OptionMenu(nv,nav_month,*months)
nv_month.grid(column=4,row=0, sticky=E)

Label(nv, text="Year").grid(column=5,row=0, sticky=E)
years = ["All"] + [str(i) for i in range(int(datetime.datetime.now().year) - 5, int(datetime.datetime.now().year) + 2)]
nav_year = StringVar()
nav_year.set(years[0])
nv_year = OptionMenu(nv,nav_year,*years)
nv_year.grid(column=6,row=0, sticky=E)

nv_date.configure(state="disable")
nv_month.configure(state="disable")
nv_year.configure(state="disable")


# Event details elements
Label(c, text="Event Details:").grid(row=12, sticky=W)
eventdetails = Text(c, height=10, width=30)
eventdetails.grid(row=13, columnspan=3, rowspan=10, sticky=(W, E))

# Reminders elements
Label(c, text="Reminders:").grid(row=24, sticky=W)
reminderlist = Listbox(c, height=8)
reminderlist.grid(row=25, columnspan=2, rowspan=8, sticky=(W, E),pady=5)
delete_reminder_btn = ttk.Button(c, text="Delete", command=deleteReminder, state="disable")
delete_reminder_btn.grid(row=25, column=2, padx=5, sticky=(N, E))

# Bind element actions to their respective functions
eventlist.bind('<<ListboxSelect>>', showEvent)
reminderlist.bind('<<ListboxSelect>>', showReminder)

# Get teh api and update the page
api = get_calendar_api()
updateEvents()
root.mainloop()
