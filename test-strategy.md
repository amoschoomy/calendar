# Test Strategy for Functionality of Calendar.py

Note #1: This test suite assumes that the Google Calendar API is thoroughly tested and does not contain any bugs/errors.

Note #2: Mocking is used whenever we require any calls to the Google Calendar API and when requiring user inputs

Note #3: We have both a CLI (Calendar.py) and a GUI (CalendarGUI.py), this test suite is for the CLI, to see test strategies for the GUI see test-strategy-GUI.md

Note #4: Each file with the filename CalendarTest<method_name> contains the tests for each method in the CLI

**Strategy for Viewing Upcoming Events**

This functionality is done through the get_upcoming_events method therefore we will test that method.

We will use is **branch coverage**. There are two visible branch in the method, first is the if statement to check for possible parsing errors in date format and the second is the for loop. From there, we can derive test cases to achieve 100% branch coverage and therefore 100 statement coverage. Branches covered will be true/false conditions therefore 4 test cases will be present. For this method there are only two possible paths which is exception error which will immediately stop program execution and normal execution. Therefore branch coverage in this method implies full path coverage

**Strategy for Viewing Past Events**

This functionality is done through get_past_events method therefore we will test that method.

We will use the same technique which is **branch coverage** except now in this method which there is 3 branches. Values(date) selected in the test cases will be according to equivalence partitioning where every values in their respective partitions that follows the 3 conditions which is < , = , > will get the same result in blackbox testing.

**Strategy for Viewing Upcoming Reminders, Viewing Past Reminders**

This functionalities is done through get_upcoming_reminders method and get_past_reminders, therefore we will test that methods. 

We will use **path coverage** for testing this method as this method have a few paths that is possible in the program flow due to nested loops and multiple if statements. This is to ensure that all possibles paths of the program are tested unlike branch coverage/condition coverage.

**Strategy for User Navigation (Feature 3)**

This functionality is done through two methods, the first being navigate_calendar where the user chooses which navigation type to view and reminders and events will be displayed. 

To test this method, **path coverage** is used to cover all possible paths in this method, there are 6 possible path in this method 2^1+2^1+1+1.

Test for get_detailed_reminder will be similar to get_upcoming_reminders but only for one specific event

The second method is get_detailed_event where it returns a string of detailed event selected.To test this method, MC/DC coverage is used to reduce the number of redundant test cases.

2 test cases are needed to check for errors raised, that will change(stop) the program flow
Then, there are 3 seperate if statements to check, so there are 4 seperate conditions that will change the program output

Test case A: 1st if statement passes, 2nd and 3rd fails
Test case B: 2nd if statement passes, 1st and 3rd fails
Test case C: 3rd if statement passes, 2nd and 1st fails
Test Case D: All if statement passes

Overall there are 6 test cases for the method get_detailed_event


**Strategy for Searching Events, Reminders**

This functionality is done through two methods, namely get_searched_events() and get_searched_reminders() methods, we will test these methods.

To test get_searched_events(), we will use **path coverage** to test this method since they are 3 visible branches and a for loop. the first 2 branches checks for invalid queries and the last branch is the for loop which may not run. We derived 4 test cases from here that can test all possible paths, implying 100% branch and statement coverage.

To test get_searched_reminders(), we wil use **path coverage** as well. There are 4 visible branches, 2 of which are nested inside a for loop. The first 2 branch checks for invalid queries, and the last 2 branch are in the for loop which may not run. We derived 5 test cases so that that can test all possible paths, implying 100% branch and statement coverage.

**Strategy for Deleting Events, Reminders**

This functionality is done through two methods, namely delete_events() and delete_reminders() methods, we will test these methods.

To test delete_events(), we will use **branch coverage** to test these methods since they are 3 visible branches, the first two checks for invalid queries and the last branch calls the api delete() function. We derived 3 test cases from here that helps use achieve 100% branch and statement coverage.

To test delete_reminders(), we will use **branch coverage** to test these methods since they are 3 visible branches, the first two checks for invalid queries and the last branch calls the api get() and update() function. We derived 3 test cases from here that helps use achieve 100% branch and statement coverage.


**Test Strategy for Running the Calendar CLI**

This functionality requires the run_calendar method which requires user input, so mocked input are used. 

We will use **branch coverage** to cover all possible user input branches and therefore implying 100% statement coverage

**Miscalleanous**

To test date_formatter method, we used **branch coverage**, there are 4 seperate branches to test, with hidden branch is when date given is wrong format.

The get_selected_event method requires user input, so mocked inputs are used. We used **path coverage** to test this function, there are 3 seperate paths, 2 of are paths are exception handlers for invalid inputs

The get_selected_reminders method requires user input, so mocked inputs are used. We used **path coverage** to test this function, there are 4 seperate paths, 2 of are paths are exception handlers for invalid inputs

