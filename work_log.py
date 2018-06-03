# As of 10:47pm on 06/02/2018
# Thanks to Chris Howell on the review-my-project slack for looking over the previous version.
# Still to do: Prevent New Entry or Edit entry from saving invalid strings in dates/minutes sections.
# Maybe recreate the way that main menu and search menu currently catch invalid options?
# Do keyword or REGEX search sections need anything else?

import datetime
import csv
import os
import re


def clear_screen():
    """Clear the screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def edit_entry(log):
    """Edit log entry."""
    with open('log.csv', 'r') as logfile:
        log_contents = list(csv.DictReader(logfile, delimiter=','))
    row_iter = 0

    for entry in log_contents:
        if entry == log:
            condemned = row_iter

            nd_loop = 1
            date_fmt = r'(\d{2}/\d{2}/\d{4})?'
            while nd_loop:
                clear_screen()
                new_date = input('''
{} is the date for this entry.
Type new date 'MM/DD/YYYY' to change, or just press enter.
'''.format(log['Date']))
                if re.match(date_fmt, new_date):
                    nd_loop -= 1
                else:
                    input('Invalid date. Press enter to try again.')

            new_task = input('''
{} is the task name for this entry.
Type new task name to change, or just press enter.
'''.format(log['Task']))

            nm_loop = 1
            nm_fmt = r'\d*'
            while nm_loop:
                new_minutes = input('''
{} is the number of minutes spent on this task.
Type a new integer to edit, or just press enter to skip.
'''.format(log['Time Spent']))
                if re.match(nm_fmt, new_minutes):
                    nm_loop -= 1
                else:
                    input('Invalid integer. Press enter to try again.')

            new_notes = input('''
"{}"
These are the task notes for this entry.
Type new notes to replace, or press enter to skip.
'''.format(log['Notes']))
            new_row = {'Date': new_date,
                       'Task': new_task,
                       'Time Spent': new_minutes,
                       'Notes': new_notes}
        else:
            row_iter += 1

    if new_row['Date'] == '':
        new_row['Date'] = log_contents[condemned]['Date']
    if new_row['Task'] == '':
        new_row['Task'] = log_contents[condemned]['Task']
    if new_row['Time Spent'] == '':
        new_row['Time Spent'] = log_contents[condemned]['Time Spent']
    if new_row['Notes'] == '':
        new_row['Notes'] = log_contents[condemned]['Notes']

    log_contents.pop(condemned)
    log_contents.append(new_row)

    with open('log.csv', 'w') as logfile:
        fieldnames = ['Date', 'Task', 'Time Spent', 'Notes']
        logwriter = csv.DictWriter(logfile, fieldnames=fieldnames)
        logwriter.writeheader()
        for row in log_contents:
            logwriter.writerow(row)
    input('Entry edited. Press enter to return to search menu.')
    return


def delete_entry(log):
    """Delete an entry."""
    with open('log.csv', 'r') as logfile:
        log_contents = list(csv.DictReader(logfile, delimiter=','))
    row_iter = 0
    for entry in log_contents:
        if entry == log:
            condemned = row_iter
        else:
            row_iter += 1

    log_contents.pop(condemned)

    with open('log.csv', 'w') as logfile:
        fieldnames = ['Date', 'Task', 'Time Spent', 'Notes']
        logwriter = csv.DictWriter(logfile, fieldnames=fieldnames)
        logwriter.writeheader()
        for row in log_contents:
            logwriter.writerow(row)
    input('Entry deleted.  Press enter to return to search menu.')
    return


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

        if entry == 0 and entry < (len(results) - 1):
            review_action = input('''
[N]ext Item,
[E]dit Item, [D]elete Item, [R]eturn to Search Menu
> ''')
        elif entry == (len(results) - 1) and entry > 0:
            review_action = input('''
[P]revious Item,
[E]dit Item, [D]elete Item, [R]eturn to Search Menu
> ''')
        elif entry == (len(results) - 1) and entry == 0:
            review_action = input('''
[E]dit Item, [D]elete Item, [R]eturn to Search Menu
> ''')
        else:
            review_action = input('''
[N]ext Item, [P]revious Item,
[E]dit Item, [D]elete Item, [R]eturn to Search Menu
> ''')

        if review_action.upper() == "N" and entry < len(results) - 1:
            entry += 1
        elif review_action.upper() == "P" and entry > 0:
            entry -= 1
        elif review_action.upper() == "E":
            edit_entry(results[entry])
            results_loop -= 1
        elif review_action.upper() == "D":
            delete_entry(results[entry])
            results_loop -= 1
        elif review_action.upper() == "R":
            results_loop -= 1
        else:
            input("Error: Invalid selection. Press enter to try again.")


def check_for_results(results):
    """Check if any search results are caught."""
    if results == []:
        input("No matches. Press enter to return to search menu.")
        return
    else:
        display_results(results)
        return


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
            check_for_results(results)
            search_loop -= 1

        else:
            print("Error: Invalid date. \n Please enter valid date.")
            input("Press 'enter' to retry.")


def search_date_range(log_contents):
    """Search by date range."""
    results = []
    search_loop = 1
    range_fmt = r'\d{2}/\d{2}/\d{4}-\d{2}/\d{2}/\d{4}'

    while search_loop:
        clear_screen()
        target_range = input('''
Please enter date range in following format:
MM/DD/YYYY-MM/DD/YYYY
> ''')

        if re.match(range_fmt, target_range):
            targets = target_range.split(sep='-')
            date_first = datetime.datetime.strptime(targets[0], "%m/%d/%Y")
            date_last = datetime.datetime.strptime(targets[1], "%m/%d/%Y")
            for entry in log_contents:
                dtlog = datetime.datetime.strptime(entry['Date'], "%m/%d/%Y")
                if dtlog >= date_first and dtlog <= date_last:
                    results.append(entry)
            check_for_results(results)
            search_loop -= 1

        else:
            print("Error: Invalid dates. \n Please enter valid date.")
            input("Press 'enter' to retry.")


def search_term(log_contents):
    """Search by keyword(s)."""
    results = []
    search_loop = 1

    while search_loop:
        clear_screen()
        target_term = input("Please enter search terms. > ")
        for entry in log_contents:
            if re.search(
                target_term.lower(),
                entry['Task'].lower()) or re.search(target_term.lower(),
                                                    entry['Notes'].lower()):
                results.append(entry)
        check_for_results(results)
        search_loop -= 1


def search_regex(log_contents):
    """Search by regex strings?"""
    results = []
    search_loop = 1

    while search_loop:
        clear_screen()
        target_term = input("Please enter a valid REGEX pattern. > ")
        for entry in log_contents:
            if re.search(target_term,
                         entry['Task']) or re.search(target_term,
                                                     entry['Notes']):
                results.append(entry)
        check_for_results(results)
        search_loop -= 1


def new_entry():
    """Add new entry to work log."""
    try:
        with open('log.csv', 'r') as logfile:
            demostring = logfile.read()
    except FileNotFoundError:
        demostring = ''

    with open('log.csv', 'a') as logfile:
        fieldnames = ['Date', 'Task', 'Time Spent', 'Notes']
        logwriter = csv.DictWriter(logfile, fieldnames=fieldnames)
        task_date = input("Please enter date in MM/DD/YYYY format. > ")
        task_title = input("Please enter a title for this task. > ")
        task_time = input("Please enter number of minutes spent on task. > ")
        task_notes = input("Any additional notes? (Press enter to skip). > ")

        if demostring == '':
            logwriter.writeheader()
        logwriter.writerow({
            'Date': task_date,
            'Task': task_title,
            'Time Spent': task_time,
            'Notes': task_notes
            })

    input("{} saved.  Press enter to return to menu.".format(task_title))
    return


def search_entries():
    """Confirm log.csv exists and select a search method."""
    se_loop = 1
    while se_loop:

        try:
            with open('log.csv', 'r') as logfile:
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
            return
        else:
            print(
                "Invalid entry.  Please select either option A, B, C, D, or E"
            )


def main_menu():
    """Start the app."""
    while True:
        clear_screen()
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
            clear_screen()
            print('Farewell!')
            quit()
        elif start.upper() == "A":
            print(new_entry())
        elif start.upper() == "B":
            print(search_entries())
        else:
            print("Invalid entry.  Please select either option A, B, or C.")
            input('Press enter to start again.')

if __name__ == '__main__':
    main_menu()
