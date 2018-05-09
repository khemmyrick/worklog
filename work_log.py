import datetime
# use datetime for date-based searches.
# check date strings from csv file with a pre-stored format against user entered datestrings
import csv
import os
import re


def clear_screen():
    """Clear the screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def search_date():
    pass


def search_term():
    pass


def search_regex():
    pass


def new_entry():
    """Add new entry to work log."""
    # Format their entry into a date object.
    try:
        with open('log.csv', 'r') as logfile:
            demostring = logfile.read()
    except FileNotFoundError:
        demostring = ''
    with open('log.csv', 'a') as logfile:
        fieldnames = ['Date', 'Task', 'Time Spent', 'Notes']
        # replace these with 'Date', 'Task', 'Time Spent' and 'Notes'
        logwriter = csv.DictWriter(logfile, fieldnames=fieldnames)

        task_date = input("Please enter date in MM/DD/YYYY format. > ")
        task_title = input("Please enter a title for this task. > ")
        task_time = input("Please enter number of minutes spent on task. > ")
        task_notes = input("Any additional notes? (Press enter to skip). > ")
        # if re.match('Date,Task', demostring) == False:
        if demostring == '':
            logwriter.writeheader()
        logwriter.writerow({
            'Date': task_date,
            'Task': task_title,
            'Time Spent': task_time,
            'Notes': task_notes
            })
        # replace these strings after replacing row headers

    input("Entry saved.  Press enter to retrun to menu.")
    return task_title + " saved."
    # add log entry


def search_entries():
    search_type = input("""
How would you like to search?
----------------------------
A) By Date
B) By Search Keyword
C) By REGEX Pattern
D) Main Menu
""")
    if search_type.upper() == 'A':
        search_date()
    elif search_type.upper() == 'B':
        search_term()
    elif search_type.upper() == 'C':
        search_regex()
    elif search_type.upper() == 'D':
        return "Returning to main menu."
    else:
        print("Invalid entry.  Please select either option A, B, C, or D.")
    # if 2. display submenu to allow different ways to search.
    # a. exact date b. range of dates c. exact search
    # d. regex pattern e. find by time spent f. range of times spent g. return to main menu
    # if an inappropriate date or search term is given, the exception should be caught ina  way that prevents app from crashing.
    # if search matches items, include options to proceed forward and backwards through each task, edit or delete individual tasks, and of course, return to main menu
    pass


def main_menu():
    """Start the app."""
    while True:
        start = input("""
WORK LOG
Please select from the following options:
----------------------------
A) New Entry
----------------------------
B) Search Existing Entries
----------------------------
C) Exit Program
----------------------------
> """)
        if start.upper() == "C":
            quit()
        elif start.upper() == "A":
            print(new_entry())
        elif start.upper() == "B":
            print(search_entries())
        else:
            print("Invalid entry.  Please select either option A, B, or C.")
            print('*' * 50)
    #        continue
            # User is given options to:
            # 1. Add new entry. 2. Search entries. 3. Exit program.

main_menu()

# Follow PEP8