import datetime
import csv
import os


def clear_screen():
    """Clear the screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def new_entry():
    # Have user specify date. MM/DD/YYYY Format their entry into a datetime object.
    # next ask user to title their task.
    # Ask for Time spent in minutes.
    # Ask for optional notes.  If they enter nothing, it's fine.
    # Let user know the entry is saved.  Wait for input to return to main menu.
    with open('log.csv', 'a') as logfile:
        fieldnames = ['entry_date', 'entry_title', 'time_spent', 'notes']
        logwriter = csv.DictWriter(logfile, fieldnames=fieldnames)

        task_date = input("Please enter date in MM/DD/YYYY format. > ")
        task_title = input("Please enter a title for this task. > ")
        task_time = input("Please enter number of minutes spent on task. > ")
        task_notes = input("Any additional notes? (Press enter to skip). > ")

        logwriter.writeheader()
        logwriter.writerrow({
            'entry_date': task_date,
            'entry_title': task_title,
            'time_spent': task_time,
            'notes': task_notes
        })
        # add log entry
    pass


def search_entries():
    # if 2. display submenu to allow different ways to search.
    # a. exact date b. range of dates c. exact search
    # d. regex pattern e. find by time spent f. range of times spent g. return to main menu
    # if an inappropriate date or search term is given, the exception should be caught ina  way that prevents app from crashing.
    # if search matches items, include options to proceed forward and backwards through each task, edit or delete individual tasks, and of course, return to main menu
    pass


def main_menu():
    """Start the app."""
    start = input("""
WORK LOG.
Please select from the following options:
A) New Entry
B) Search Existing Entries
C) Exit Program
> """)
    if start.upper() == "C":
        quit()
    elif start.upper() == "A":
        new_entry()
    elif start.upper() == "B":
        search_entries()
    else:
        print("Invalid entry.  Please select either option A, B, or C.")
        continue
        # User is given options to:
        # 1. Add new entry. 2. Search entries. 3. Exit program.

    # Follow PEP8