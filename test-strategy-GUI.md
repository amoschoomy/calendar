Note #1: This test suite assumes that the Google Calendar API is thoroughly tested and does not contain any bugs/errors.

Note #2: Mocking is used whenever we require any calls to the Google Calendar API and when requiring user inputs

Note #3: We have both a CLI (Calendar.py) and a GUI (CalendarGUI.py), this test suite is for the GUI, to see test strategies for the GUI see test-strategy.md

Note #4: All tests for the GUI are in the file CalendarGUITestAll.py, with each class in the file reperesenting a method under test.

#**Strategies for Viewing a List Of Events**

This functionality is done using the **reload_event_list** method.-

Since the method relies heavily on user input, we use **path coverage** to test this function to cover all possible paths of user input given by the user.

This method also calls the google calendar api, hence **mocking** will be used to simulate the return value of the google api and all user inputs.

There are certain parameters (user inputs) that that dictates what is displayed on the event list. the parameters are:-

**Parameter 1:** Include **past** events

In order to add past events to the event list, the user has to check the "Show past events" checkbox.

They also have to input a valid past date in an adjacent textbox from which, all the events after the inputted date will be loaded in the event list.

The past date validation is done by the **verify_date** method which we will test using **path coverage**.

Path coverage is used because we expect user input and by using path coverage we can test all the possible user input paths


**Parameter 2:**  **Navigate** and show events of a specific period

In order to show and navigate to events of a specific period in the event list, the user has to check the "Show events from" textbox.

They also have to input a valid date period in an adjacent options dropdown lists from which, all the events in the said period will be loaded in the event list.

The period validation is done using the **get_periods** method, which we will test using **category partitioning**, a blackbox testing technique.

The categories are as follows :-

a) All years - Returns startdate = None, enddate = None

b) All months of a specific year - Returns startdate = 1 JAN of selected year, enddate = 31 DEC of selected year

c) All dates of a specific month and year - Returns startdate = 1st of selected month and year, enddate = 30th/31st of selected month and year

d) Specific date, month and year - Returns startdate = enddate = selected date, month and year

e) Invalid date - returns startdate = today, enddate = None

**Parameter 3:** Filter events with **search** keywords

In order to show only events containing specific keywords, the user have to input the keyword in the search textbox above the event list and only events containing the said keyword will be added to the event list


#**Strategies for Viewing an event details and reminders**

When the user decides to view an event, they would click on the event in the event list and the details and reminders of the event will be displayed below the event list.

This is by 2 methods get_detailed_events and load_event_details 

**get_detailed_events** decodes the event object retrieved from the API and converts it to a paragraph of legible texts

To test get_detailed_events, we use **path coverage** because some events may contain certain attributes that some events don't. (eg. guests and location)

**load_event_details** then displays the details of the event on the main GUI and enables the delete buton to delete the event. It also inserts all the reminders that the event has into a reminder list as well

To test load_event_details, we use **path coverage** because there are 3 possible paths in the function

Depending on whether an event is selected or not, and also some events may contain default reminders while others don't and we want to test both cases.

#**Strategies for Deleting an event and its reminders**

**Deleting event**

When the user selects an event, the "Delete" button will be enabled and he/she can delete the event by clicking on it

This functionality is handled by the **delete_event** method which calls the google calendar api.

To test this functionality we used **path coverage**, and **mocking** will be used to simulate the google api's return value and all user inputs

There are only 2 paths this method could take, depending whether the user has selected the event or not, therefore we test all the paths in the test cases

**Deleting reminders of event**

When the user selects an event, the reminder list will be populated with reminders of that event.

When the user selects a specific reminder, the "Delete" button will be enabled and he/she can delete the reminder by clicking on it

This functionality is handled by the **delete_reminder** method which calls the google calendar api to inform it of the delete command

To test this functionality we used **path coverage**, and **mocking** will be used to simulate the google api's return value and all user inputs

There are 4 paths this method could take, depending whether the event user has selected the event and reminder or not. It also depends whether the selected event has a default reminder or not.
Therefore we test all the paths in the test cases

#**Strategies for Testing UI Elements and Behaviours**

These methods below exists to make the GUI interactive and user friendly

Since user input is required to test these methods, **mocking** will be sued to simulate all user inputs

**enable_date_textbox** is used to enable the date textbox input when the user checks the "Show past event" checkbox

To test this function we will use **branch coverage** because there are 2 visible branches. One for when the checkbox is checked and the other for otherwise.

**enable_periods** is used to enable the date period drop-down option lists when the user checks the "Show events from"

To test this function we will use **branch coverage** because there are 2 visible branches. One for when the checkbox is checked and the other for otherwise.

**enable_delete_reminder** enables the delete button whenever a reminder is selected from the reminder list

To test this functionality we used **path coverage** because there are 2 paths this method could take, depending whether the event user has selected the reminder or not.

**assign_elements_to_grid** ensures that the UI elements are positioned properly in the UI

To test this functionality we used **mocking** to ensure that all relevant UI elements are positioned properly

**bind_elements_command** ensures that UI elements are binded with the necassary methods to execute upon activation

To test this functionality we used **mocking** to ensure that all relevant UI elements are binded with the correct commands 
