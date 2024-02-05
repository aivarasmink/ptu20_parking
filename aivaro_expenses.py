import PySimpleGUI as sg
import sqlite3
from datetime import datetime

# Connect the database to SQLite
connector = sqlite3.connect("expenses_tracker.db")
cursor = connector.cursor()

connector.execute(
    'CREATE TABLE IF NOT EXISTS ExpenseTracker (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Date DATETIME, Description TEXT, Amount FLOAT)'
)
connector.commit()

# To list all the expenses
def list_all_expenses(table):
    table.delete(*table.get_children())

    all_data = connector.execute('SELECT * FROM ExpenseTracker')
    data = all_data.fetchall()

    for values in data:
        table.insert('', sg.TableData(values=values))

# To clear all the fields
def clear_fields(date, desc, amnt, table):
    today_date = datetime.now().date()
    date.update(value=today_date)
    desc.update(value='')
    amnt.update(value=0.0)
    table.update(values=[])

# To add an expense
def add_expense(values, date, desc, amnt, table):
    if not values['date'] or not values['desc'] or not values['amnt']:
        sg.popup_error('Field empty. Please fill out all missing fields before adding expense.')
    else:
        connector.execute(
            'INSERT INTO ExpenseTracker (Date, Description, Amount) VALUES (?,?,?)',
            (values['date'], values['desc'], values['amnt'])
        )
        connector.commit()

        clear_fields(date, desc, amnt, table)
        list_all_expenses(table)

# To remove an expense
def remove_expense(table):
    if not table.SelectedRows:
        sg.popup_error('No expense selected.')
        return
    
    current_selection = table.SelectedRows[0]
    values_selected = current_selection
    surety = sg.popup_yes_no('Are you sure?', f'Are you sure that you want to delete the expense of {values_selected[2]}')

    if surety == 'Yes':
        connector.execute('DELETE FROM ExpenseTracker WHERE ID=%d' % values_selected[0])
        connector.commit()
        list_all_expenses(table)

# PySimpleGUI window
sg.theme('Dark Blue 3')

layout = [
    [sg.Text('Expense Tracker', font=('broadway', 20), justification='center', size=(20, 1))],
    [sg.Text('Date (DD/M/YY):'), sg.InputText(key='date', size=(10, 1)), sg.Button('Enter date', key='enter date')],
    [sg.Text('Description:'), sg.InputText(key='desc', size=(15, 1))],
    [sg.Text('Amount:'), sg.InputText(key='amnt', size=(10, 1))],
    [sg.Button('Add Expense', key='add_expense'), sg.Button('Delete Expense', key='remove_expense')],
    [sg.Table(values=[], headings=['ID', 'Date', 'Description', 'Amount'],
              auto_size_columns=True, justification='right', key='table', display_row_numbers=False,
              num_rows=15, col_widths=[10, 20, 60, 15])]
]

window = sg.Window('Expense Tracker', layout, finalize=True)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == 'pick_date':
        date_value = sg.popup_get_date('Enter date', default_date=values['date'])
        window['date'].update(value=date_value)
    elif event == 'add_expense':
        add_expense(values, window['date'], window['desc'], window['amnt'], window['table'])
    elif event == 'remove_expense':
        remove_expense(window['table'])

window.close()
