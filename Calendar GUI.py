from tkinter import *
from tkinter import ttk
from Calendar import *

root = Tk()
api = get_calendar_api()

events = None
event_ids = None
event_names = None
fromdate = None

def showEvent(*args,selected=None):

    global selected_event
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


def updateEvents():
    global events
    global event_ids
    global event_names

    past_date_tokens = verify_date(dateIn.get())

    if searchIn.get().lower() != "":
        events = get_searched_events(api, searchIn.get())
    elif past_only.get() and past_date_tokens:
        date = datetime.datetime.strptime(past_date_tokens[2] + "-" + past_date_tokens[1] + "-" + past_date_tokens[0],
                                          "%Y-%m-%d").isoformat() + ".000000Z"
        events = get_past_events(api, date)
    else:
        events = get_upcoming_events(api)

    event_ids = [events[i]["id"] for i in range(len(events))]
    event_names = [events[i]["summary"] for i in range(len(events))]
    eventlist.delete(0, END)
    for i in event_names:
        eventlist.insert(END, i)

    reminderlist.delete(0, END)
    eventdetails.delete(1.0, END)
    delete_event_btn.configure(state="disable")


def deleteEvent(reminders=None):
    idxs = eventlist.curselection()
    if len(idxs) == 1:
        idx = int(idxs[0])
        print(events[idx])
        delete_events(api, events[idx])
        updateEvents()



def enableTextbox():
    if past_only.get():
        dateIn.configure(state="normal")
        updateBtn.configure(state="normal")
    else:
        dateIn.configure(state="disabled")
        updateBtn.configure(state="disabled")


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
        if selected_event["reminders"].get("useDefault",False):
            idx = -1
        delete_reminders(api,selected_event,idx)
        showEvent()


print(verify_date("10-10-2010"))
# Create and grid the outer content frame
c = ttk.Frame(root, padding=(5, 5, 12, 0))
c.grid(column=0, row=0, sticky=(N, W, E, S))
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

Label(c, text="Search all events: ").grid(row=0, sticky=(E))

searchIn = ttk.Entry(c)
searchIn.grid(row=0, column=1, padx=5, sticky=(W, E))

searchBtn = ttk.Button(c, text="Search", command=updateEvents)
searchBtn.grid(row=0, column=2, padx=5, sticky=E)

Label(c, text="Events").grid(row=1, sticky=W)
eventlist = Listbox(c, height=8, exportselection=False)
eventlist.grid(row=2, columnspan=2, rowspan=8, sticky=(W, E))
ttk.Button(c, text="Refresh", command=updateEvents).grid(row=2, column=2, padx=5, sticky=(N, E))

delete_event_btn = ttk.Button(c, text="Delete", command=deleteEvent, state="disable")
delete_event_btn.grid(row=3, column=2, padx=5, sticky=(N, E))

past_only = IntVar()
checkbtn = Checkbutton(c, text="Show only past events since: ", variable=past_only, command=enableTextbox).grid(row=10,
                                                                                                                sticky=W)

dateIn = ttk.Entry(c, state="disabled")
dateIn.grid(row=10, column=1, pady=5, padx=5, sticky=(W, E))

updateBtn = ttk.Button(c, text="Update", state="disable", command=updateEvents)
updateBtn.grid(row=10, column=2, padx=5, sticky=E)

Label(c, text="Event Details:").grid(row=11, sticky=W)
eventdetails = Text(c, height=10, width=30)
eventdetails.grid(row=12, columnspan=3, rowspan=10, sticky=(W, E))

Label(c, text="Reminders:").grid(row=23, sticky=W)
reminderlist = Listbox(c, listvariable=event_names, height=8)
reminderlist.grid(row=24, columnspan=2, rowspan=8, sticky=(W, E))

delete_reminder_btn = ttk.Button(c, text="Delete", command=deleteReminder,state="disable")
delete_reminder_btn.grid(row=24, column=2, padx=5, sticky=(N, E))

eventlist.bind('<<ListboxSelect>>', showEvent)
reminderlist.bind('<<ListboxSelect>>', showReminder)

updateEvents()
root.mainloop()
