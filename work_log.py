import datetime
import csv
import os
import re


def clear_screen():
    """Clear the screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def minute_check(minutes):
    try:
        int(minutes)
    except ValueError:
        input('Invalid integer. Press enter to try again.')
        return False
    else:
        return True


def edit_entry(log):
    """Edit log entry."""
    with open('log.csv', 'r') as logfile:
        log_contents = list(csv.DictReader(logfile, delimiter=','))
    row_iter = 0

    for entry in log_contents:
        if entry == log:
            condemned = row_iter

            nd_loop = 1
            while nd_loop:
                clear_screen()
                new_date = input('''
{} is the date for this entry.
Type new date 'MM/DD/YYYY' to change, or just press enter.
'''.format(log['Date']))
                if new_date == '':
                    nd_loop -= 1
                else:
                    try:
                        datetime.datetime.strptime(new_date, "%m/%d/%Y")
                    except ValueError:
                        input('Invalid date. Press enter to try again.')
                    else:
                        nd_loop -= 1

            nt_loop = 1
            while nt_loop:
                new_task = input('''
{} is the task name for this entry.
Type new task name to change, or just press enter.
'''.format(log['Task']))
                if new_task == '' or re.match(r'\S+', new_task):
                    nt_loop -= 1
                else:
                    input('Invalid task name.  Press enter to try again.')

            nm_loop = 1
            while nm_loop:
                new_minutes = input('''
{} is the number of minutes spent on this task.
Type a new integer to edit, or just press enter to skip.
'''.format(log['Time Spent']))
                if new_minutes == '':
                    nm_loop -= 1
                else:
                    legit = minute_check(new_minutes)
                    if legit:
                        nm_loop -= 1
                    else:
                        continue

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


def search_datelist(log_contents):
    """Select date from list of available dates."""
    results = []
    search_loop = 1
    while search_loop:
        for entry in log_contents:
            if entry['Date'] not in results:
                results.append(entry['Date'])

        list_loop = 1
        list_dict = {}
        clear_screen()
        for day in results:
            list_dict[list_loop] = day
            print('{}: {}'.format(list_loop, day))
            list_loop += 1

        select_loop = 1
        while select_loop:
            try:
                selection = int(input('Please select a date from this list.'))
            except ValueError:
                input('Input must be number. Press enter to retry.')
            else:
                try:
                    list_dict[selection]
                except KeyError:
                    print('That number is not on the list.')
                    input('Press enter to retry.')
                else:
                    select_loop -= 1

        results = []
        for entry in log_contents:
            if entry['Date'] == list_dict[selection]:
                results.append(entry)
        check_for_results(results)
        search_loop -= 1


def search_date_range(log_contents):
    """Search by date range."""
    results = []
    search_loop = 1

    while search_loop:
        clear_screen()

        tr_loop = 1
        while tr_loop:
            target_range = input('''
Please enter date range in following format:
MM/DD/YYYY-MM/DD/YYYY
> ''')

            targets = target_range.split(sep='-')
            try:
                date_frst = datetime.datetime.strptime(targets[0], "%m/%d/%Y")
                date_last = datetime.datetime.strptime(targets[1], "%m/%d/%Y")
            except ValueError:
                input('Invalid date range. Press enter to retry.')
            else:
                if date_frst < date_last:
                    tr_loop -= 1
                else:
                    print('Invalid date range.')
                    print('Please enter two dates, earliest first.')
                    input('Press enter to retry.')

        for entry in log_contents:
            try:
                dtlog = datetime.datetime.strptime(entry['Date'],
                                                   "%m/%d/%Y")
            except ValueError:
                continue
            else:
                if dtlog >= date_frst and dtlog <= date_last:
                    results.append(entry)
        check_for_results(results)
        search_loop -= 1


def search_term(log_contents):
    """Search by keyword(s)."""
    results = []
    search_loop = 1

    while search_loop:
        clear_screen()

        tt_loop = 1
        while tt_loop:
            target_term = input("Please enter search keyword(s). > ")
            if re.match(r'\w+', target_term):
                tt_loop -= 1
            else:
                print('Enter a non-REGEX search term.')
                print('Term should begin with an alphanumeric character.')
                input('Press enter to retry.')

        for entry in log_contents:
            if re.search(
                target_term.lower(),
                entry['Task'].lower()) or re.search(target_term.lower(),
                                                    entry['Notes'].lower()):
                results.append(entry)
        check_for_results(results)
        search_loop -= 1


def search_regex(log_contents):
    """Search by regex strings."""
    results = []
    search_loop = 1

    while search_loop:
        clear_screen()

        tt_loop = 1
        while tt_loop:
            target_term = input("Please enter a valid REGEX pattern. > ")
            try:
                re.match(target_term, log_contents[0]['Task'])
            except re.error:
                clear_screen()
                print('"{}" is not a valid REGEX pattern.'.format(target_term))
                print('''
For more information on REGEX patterns in python, please visit:
https://docs.python.org/3/library/re.html
''')
                input('Press enter to retry.')
            else:
                tt_loop -= 1

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

        td_loop = 1
        while td_loop:
            task_date = input("Please enter date in MM/DD/YYYY format. > ")
            try:
                datetime.datetime.strptime(task_date, "%m/%d/%Y")
            except ValueError:
                input('Invalid date. Press enter to try again.')
            else:
                td_loop -= 1

        tt_loop = 1
        while tt_loop:
            task_title = input("Please enter a title for this task. > ")
            if re.match(r'\S+', task_title):
                tt_loop -= 1
            else:
                input('Invalid task name.  Press enter to try again.')

        tm_loop = 1
        while tm_loop:
            task_min = input("Enter number of minutes spent on task. > ")
            legit = minute_check(task_min)
            if legit:
                tm_loop -= 1
            else:
                continue

        task_notes = input("Any additional notes? (Press enter to skip). > ")

        if demostring == '':
            logwriter.writeheader()
        logwriter.writerow({
            'Date': task_date,
            'Task': task_title,
            'Time Spent': task_min,
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
            search_datelist(log_contents)
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
            print('''
Invalid entry.  Please select either option A, B, C, D, or E.
''')


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
