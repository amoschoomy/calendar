# Test Strategy for Functionalties of Calendar.py

**Strategy for Viewing Upcoming Events**

This functionality is done through the get_upcoming_events method therefore we will test that method.

The whitebox technique we will use is branch coverage. There are two visible branch in the method, first is the if statement to check for possible parsing errors in date format and the second is the for loop. From there, we can derive test cases to achieve 100% branch coverage and therefore 100 statement coverage. Branches covered will be true/false conditions therefore 4 test cases will be present. For this method there are only two possible paths which is exception error which will immediately stop program execution and normal execution. Therefore branch coverage in this method implies full path coverage

**Strategy for Viewing Past Events**

This functionality is done through get_past_events method therefore we will test that method.

We will use the same technique which is branch coverage except now in this method which there is 3 branches. Values(date) selected in the test cases will be according to equivalence partitioning where every values in their respective partitions that follows the 3 conditions which is < , = , > will get the same result in blackbox testing. 

**Strategy for Viewing Upcoming Reminders, Viewing Past Reminders**

This functionalities is done through get_upcoming_reminders method and get_past_reminders, therefore we will test that methods. We will use path coverage for testing this method as this method have a few paths that is possible in the program flow due to nested loops and multiple if statements. This is to ensure that all possibles paths of the program are tested unlike branch coverage/condition coverage.

**Strategy for User Navigation (Feature 3)**

This functionality is done through two methods, the first being navigate_calendar where the user chooses which navigation type to view and reminders and events will be displayed. To test this method, path coverage is used to cover all possible paths in this method, there are 6 possible path in this method 2^1+2^1+1+1.

The second method is get_detailed_event where it returns a string of detailed event selected.To test this method, MC/DC coverage is used to reduce the number of redundant test cases.

2 test cases are needed to check for errors raised, that will change(stop) the program flow
Then, there are 3 seperate if statements to check, so there are 4 seperate conditions that will change the program output

Test case A: 1st if statement passes, 2nd and 3rd fails
Test case B: 2nd if statement passes, 1st and 3rd fails
Test case C: 3rd if statement passes, 2nd and 1st fails
Test Case D: All if statement passes

Overall there are 6 test cases for the method get_detailed_event


**Miscalleanous**

To test date_formatter method, just use branch coverage, there are 4 seperate branches to test, with hidden branch is when date given is wrong format.

