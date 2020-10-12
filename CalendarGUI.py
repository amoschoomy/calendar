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
import sys
import os
from tkinter import *
from tkinter import ttk
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

if os.environ.get('DISPLAY', '') == '':
    os.environ.__setitem__('DISPLAY', ':99')

events = None
api = None


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


def reload_event_list():
    global events

    query = None
    starting_time = datetime.datetime.utcnow().isoformat() + 'Z'
    end_time = None

    if searchIn.get().lower() != "":
        query = searchIn.get()

    past_date_tokens = verify_date(dateIn.get())
    if past_only.get() and past_date_tokens:
        starting_time = datetime.datetime.strptime(
            past_date_tokens[2] + "-" + past_date_tokens[1] + "-" + past_date_tokens[0],
            "%Y-%m-%d").isoformat() + ".000000Z"
    elif specific_only.get():
        period = get_periods(nav_date.get(), nav_month.get(), nav_year.get())
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


def load_event_details(*args):
    idxs = eventlist.curselection()
    if len(idxs) == 1:
        idx = int(idxs[0])
        text = get_detailed_event(events[idx])
        eventdetails.delete(1.0, END)
        eventdetails.insert(END, text)
        reminderlist.delete(0, END)

        if events[idx]["reminders"].get("useDefault", False):
            print(events[idx]["reminders"].get("useDefault", False))
            reminderlist.insert(END, "Popup 10 minutes before event starts")
        else:
            overrides = events[idx]["reminders"].get("overrides", [])
            for each in overrides:
                reminderlist.insert(END, each.get("method") + " " + str(
                    each.get("minutes")) + " minutes before event starts")

        delete_event_btn.configure(state="normal")
        delete_reminder_btn.configure(state="disable")


def delete_event():
    idxs = eventlist.curselection()
    if len(idxs) == 1:
        idx = int(idxs[0])
        api.events().delete(calendarId='primary', eventId=events[idx]["id"]).execute()
        reload_event_list()


def delete_reminder():
    idxs = eventlist.curselection()
    selected_event = None
    if len(idxs) == 1:
        selected_event = int(idxs[0])
    idxs = reminderlist.curselection()
    if len(idxs) == 1 and selected_event is not None:
        idx = int(idxs[0])
        if events[selected_event]["reminders"].get("useDefault", False):
            events[selected_event]['reminders'] = {"useDefault": False, "overrides": []}
        else:
            events[selected_event]['reminders']["overrides"].pop(idx)
        api.events().update(calendarId='primary', eventId=events[selected_event]['id'],
                            body=events[selected_event]).execute()
        load_event_details()


def enable_date_textbox():
    if past_only.get():
        dateIn.configure(state="normal")
        specific_only.set(0)
        enable_periods()
    else:
        dateIn.configure(state="disable")


def enable_periods():
    if specific_only.get():
        nv_date.configure(state="normal")
        nv_month.configure(state="normal")
        nv_year.configure(state="normal")
        past_only.set(0)
        enable_date_textbox()
    else:
        nv_date.configure(state="disable")
        nv_month.configure(state="disable")
        nv_year.configure(state="disable")


dates_in_month = {"1": 31, "2": 28, "3": 31, "4": 30, "5": 31, "6": 30, "7": 31, "8": 31, "9": 30, "10": 31, "11": 30,
                  "12": 31, "All": 31}


def get_periods(date, month, year):
    if month == "All":
        month = "1"
        date = "1"
        endmonth = "12"
        endday = "31"
    else:
        endmonth = month
        if date == "All":
            date = "1"
            endday = str(dates_in_month[endmonth])
        else:
            endday = date

    if year != "All":
        try:
            startdate = datetime.datetime.strptime(year + "-" + month + "-" + date + " 23:59:59",
                                                   '%Y-%m-%d %H:%M:%S').isoformat() + "Z"
            enddate = datetime.datetime.strptime(year + "-" + endmonth + "-" + endday + " 23:59:59",
                                                 '%Y-%m-%d %H:%M:%S').isoformat() + "Z"
        except ValueError:
            startdate = datetime.datetime.utcnow().isoformat() + 'Z'
            enddate = None
    else:
        startdate = None
        enddate = None

    return startdate, enddate


def verify_date(string):
    string = string.replace("/", "-")
    string = string.replace(".", "-")
    tokens = string.split("-")

    if len(tokens) != 3:
        return False
    try:
        if int(tokens[0]) in list(range(1, 32)) and int(tokens[1]) in list(range(1, 13)) and int(tokens[2]) > 1900:
            return tokens
        else:
            return False
    except ValueError:
        return False


def enable_delete_reminder(*args):
    idxs = reminderlist.curselection()
    if len(idxs) == 1:
        delete_reminder_btn.configure(state="normal")


root = c = sch = searchIn = searchBtn = eventlist = refreshBtn = delete_event_btn = past_only = checkbtn = dateIn = updateBtn = nv \
    = specific_only = navigate_checkbtn = nav_date = nv_date = nav_month = nv_month = nav_year = nv_year = eventdetails = reminderlist = \
    delete_reminder_btn = None
lbl1 = lbl2 = lbl3 = lbl4 = lbl5 = lbl6 = lbl7 = None

dates = ["All"] + [str(i) for i in range(1, 32)]
months = ["All"] + [str(i) for i in range(1, 13)]
years = ["All"] + [str(i) for i in range(int(datetime.datetime.now().year) - 5, int(datetime.datetime.now().year) + 2)]


def assign_elements_to_grid():

    c.grid(column=0, row=0, sticky=(N, W, E, S))
    sch.grid(row=0, columnspan=2, sticky=(W, E))
    searchIn.grid(row=0, column=1, padx=5, sticky=(W, E))
    searchBtn.grid(row=0, column=2, padx=5, sticky=E)
    eventlist.grid(row=2, columnspan=2, rowspan=8, sticky=(W, E))
    refreshBtn.grid(row=2, column=2, padx=5, sticky=(N, E))
    delete_event_btn.grid(row=3, column=2, padx=5, sticky=(N, E))
    dateIn.grid(row=10, column=1, pady=5, padx=5, sticky=(W, E))
    checkbtn.grid(row=10, sticky=W)
    updateBtn.grid(row=10, rowspan=2, column=2, padx=5, sticky=(N, S, E))
    nv.grid(row=11, columnspan=2, sticky=(W, E))
    navigate_checkbtn.grid(column=0, row=0, sticky=W)
    nv_date.grid(column=2, row=0, sticky=E)
    nv_month.grid(column=4, row=0, sticky=E)
    nv_year.grid(column=6, row=0, sticky=E)
    eventdetails.grid(row=13, columnspan=3, rowspan=10, sticky=(W, E))
    reminderlist.grid(row=25, columnspan=2, rowspan=8, sticky=(W, E), pady=5)
    delete_reminder_btn.grid(row=25, column=2, padx=5, sticky=(N, E))

    lbl1.grid(row=0, column=0, sticky=E)
    lbl2.grid(row=1, sticky=W)
    lbl3.grid(column=1, row=0, sticky=E)
    lbl4.grid(column=3, row=0, sticky=E)
    lbl5.grid(column=5, row=0, sticky=E)
    lbl6.grid(row=12, sticky=W)
    lbl7.grid(row=24, sticky=W)


def bind_elements_command():
    searchBtn.configure(command=reload_event_list)
    refreshBtn.configure(command=reload_event_list)
    updateBtn.configure(command=reload_event_list)
    checkbtn.configure(command=enable_date_textbox)
    navigate_checkbtn.configure(command=enable_periods)
    delete_event_btn.configure(command=delete_event)
    delete_reminder_btn.configure(command=delete_reminder)
    # Bind element actions to their respective functions
    eventlist.bind('<<ListboxSelect>>', load_event_details)
    reminderlist.bind('<<ListboxSelect>>', enable_delete_reminder)


def main():
    global api, c, sch, searchIn, searchBtn, eventlist, refreshBtn, delete_event_btn, past_only, checkbtn, dateIn, updateBtn, nv, specific_only, \
        navigate_checkbtn, nav_date, nv_date, nav_month, nv_month, nav_year, nv_year, eventdetails, reminderlist, \
        delete_reminder_btn, root, lbl1, lbl2, lbl3, lbl4, lbl5, lbl6, lbl7

    api = get_calendar_api()
    # Init and configure eleements
    # Create and grid the outer content frame
    root = Tk()
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    c = ttk.Frame(padding=(5, 5, 12, 0))
    # Search Elements
    sch = ttk.Frame(c)
    lbl1 = Label(sch, text="Search events: ")
    searchIn = ttk.Entry(sch, width=50)
    searchBtn = ttk.Button(c, text="Search")
    # Events List Elements
    lbl2 = Label(c, text="Events")
    eventlist = Listbox(c, height=8, exportselection=False)
    refreshBtn = ttk.Button(c, text="Refresh")
    delete_event_btn = ttk.Button(c, text="Delete", state="disable")
    # Show past events elements
    past_only = IntVar()
    checkbtn = Checkbutton(c, text="Show past events since: (DD/MM/YYYY)",variable=past_only)
    dateIn = ttk.Entry(c, state="disabled")
    updateBtn = ttk.Button(c, text="Update")
    # Navigate events elements
    nv = ttk.Frame(c)
    specific_only = IntVar()
    navigate_checkbtn = Checkbutton(nv, variable=specific_only, text="Show only events on: ")
    lbl3 = Label(nv, text="Date")
    nav_date = StringVar()
    nav_date.set(dates[0])
    nv_date = OptionMenu(nv, nav_date, *dates)
    lbl4 = Label(nv, text="Month")
    nav_month = StringVar()
    nav_month.set(months[0])
    nv_month = OptionMenu(nv, nav_month, *months)
    lbl5 = Label(nv, text="Year")
    nav_year = StringVar()
    nav_year.set(years[0])
    nv_year = OptionMenu(nv, nav_year, *years)
    nv_date.configure(state="disable")
    nv_month.configure(state="disable")
    nv_year.configure(state="disable")
    # Event details elements
    lbl6 = Label(c, text="Event Details:")
    eventdetails = Text(c, height=10, width=30)
    # Reminders elements
    lbl7 = Label(c, text="Reminders:")
    reminderlist = Listbox(c, height=8)
    delete_reminder_btn = ttk.Button(c, text="Delete", state="disable")
    assign_elements_to_grid()
    bind_elements_command()
    reload_event_list()
    root.mainloop()


if __name__ == "__main__":  # Prevents the main() function from being called by the test suite runner
    try:
        main()

    except KeyboardInterrupt:
        pass
