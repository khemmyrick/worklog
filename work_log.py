# I've been stuck on the project forever.
# Took longer than I'd like to admit to realize I could loop through the csv.DictReader list the same way I did in project 1.
# New Entry works.
# Search by single date works.
# Next to be implemented:
# 1. edit/delete search entry.
# 2. Search by date range.
# 3. Search by keyword.
# 4. Search by REGEX.

import datetime
import csv
import os
import re


def clear_screen():
    """Clear the screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_results(results):
    """Display search results."""
    clear_screen()
    results_loop = 1
    entry = 0
    while results_loop:
        clear_screen()
        print(str(len(results)) + " results match your search.")
        print("Date: " + results[entry]['Date'])
        print("Task: " + results[entry]['Task'])
        print("Time Spent: " + results[entry]['Time Spent'])
        print("Notes: " + results[entry]['Notes'] + "\n")
        print("Entry {} of {}.".format((entry + 1), len(results)))
        if entry == 0 & entry < (len(results) - 1):
            review_action = input('''
[N]ext Item,
[E]dit Item, [D]elete Item, [R]eturn to Search Menu
> ''')
        elif entry == (len(results) - 1) & entry > 0:
            review_action = input('''
[P]revious Item,
[E]dit Item, [D]elete Item, [R]eturn to Search Menu
> ''')
        elif entry == (len(results) - 1) & entry == 0:
            review_action = input('''
[E]dit Item, [D]elete Item, [R]eturn to Search Menu
> ''')
        else:
            review_action = input('''
[N]ext Item, [P]revious Item,
[E]dit Item, [D]elete Item, [R]eturn to Search Menu
> ''')
        if review_action.upper() == "N":
            entry += 1
        elif review_action.upper() == "P":
            entry -= 1
        elif review_action.upper() == "E":
            edit_entry()
            pass
        elif review_action.upper() == "D":
            delete_entry()
            pass
        elif review_action.upper() == "R":
            results_loop -= 1
            return "Search complete."
        else:
            print("Error: Please select a valid option.")


def search_date(log_contents):
    """Search by date."""
    results = []
    search_loop = 1
    while search_loop:
        clear_screen()
        target_date = input('''
    Please enter date in following format:
    MM/DD/YYYY
    > ''')
        date_fmt = r'\d{2}/\d{2}/\d{4}'
        if re.match(date_fmt, target_date):
            for entry in log_contents:
                if entry['Date'] == target_date:
                    results.append(entry)
            display_results(results)
            search_loop -= 1
        else:
            print("Error: Invalid date. \n Please enter valid date.")
            input("Press 'enter' to retry.")


def search_date_range(log_contents):
    range_fmt = r'\d{2}/\d{2}/\d{4}(-\d{2}/\d{2}/\d{4})?'
    target_range = input('''
Please enter date range in following format:
MM/DD/YYYY-MM/DD/YYYY
''')
    pass


def search_term(log_contents):
    """Search by keyword(s)."""
    pass
    target_term = input("Please enter search terms.")


def search_regex(log_contents):
    """Search by regex codes?"""
    # ?
    pass


def new_entry():
    """Add new entry to work log."""
    # Format their entry into a date object?
    try:
        with open('log.csv', 'r') as logfile:
            demostring = logfile.read()
    except FileNotFoundError:
        demostring = ''
        # Check if log.csv exists.
    with open('log.csv', 'a') as logfile:
        fieldnames = ['Date', 'Task', 'Time Spent', 'Notes']
        logwriter = csv.DictWriter(logfile, fieldnames=fieldnames)
        task_date = input("Please enter date in MM/DD/YYYY format. > ")
        task_title = input("Please enter a title for this task. > ")
        task_time = input("Please enter number of minutes spent on task. > ")
        task_notes = input("Any additional notes? (Press enter to skip). > ")
        if demostring == '':
            logwriter.writeheader()
            # If log.csv doesn't exist, create it and add header row.
        logwriter.writerow({
            'Date': task_date,
            'Task': task_title,
            'Time Spent': task_time,
            'Notes': task_notes
            })

    input("Entry saved.  Press enter to return to menu.")
    return task_title + " saved."


def search_entries():
    """Confirm log.csv exists and select a search method."""
    se_loop = 1
    while se_loop:

        try:
            with open('log.csv', 'r') as logfile:
                # Reopen csv file and check contents every time.
                # Reason being: We may have made edits!
                log_contents = list(csv.DictReader(logfile, delimiter=','))

        except FileNotFoundError:
            input("This work log is empty. Press 'enter' to return to menu.")
            return "Returning to menu."

        else:
            clear_screen()
            search_type = input("""
    How would you like to search? Type a letter to select your choice.
    ----------------------------
    A) By Date
    B) By Range of Dates
    C) By Search Keyword
    D) By REGEX Pattern
    E) Return to Main Menu
    > """)

        if search_type.upper() == 'A':
            search_date(log_contents)
        elif search_type.upper() == 'B':
            search_date_range(log_contents)
        elif search_type.upper() == 'C':
            search_term(log_contents)
        elif search_type.upper() == 'D':
            search_regex(log_contents)
        elif search_type.upper() == 'E':
            clear_screen()
            return "Return to Main Menu. \n ------------------------"
        else:
            print("Invalid entry.  Please select either option A, B, C, or D.")


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


main_menu()

# Follow PEP8