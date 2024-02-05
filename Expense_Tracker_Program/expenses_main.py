import PySimpleGUI as sg
from datetime import datetime
from expenses_add_summary import add_expense, get_summary

sg.theme("Dark Blue 3")
sg.set_options(font="broadway 20")

def register_expense():
    layout = [
        [sg.Text("Description:"), sg.Input(key="-DESCRIPTION-", size=(15, 1))],
        [sg.Text("Amount:"), sg.Input(key="-AMOUNT-", size=(15, 1))],
        [sg.Button("Register", key="-REGISTER-"), sg.Button("Return", key="-RETURN-")],
    ]

    window = sg.Window("Register Expense", layout, element_padding=(10, 10))

    while True:
        event, values = window.read()

        if event in [sg.WIN_CLOSED, "-RETURN-"]:
            break

        if event == "-REGISTER-":
            description = values["-DESCRIPTION-"]
            amount = values["-AMOUNT-"]

            # Add logic to handle the registration of the expense
            # For simplicity, just printing the values for now
            add_expense(datetime.now(), "Category", description, float(amount))
            sg.Popup("Expense registered successfully", title = "Success")

                        

    window.close()

main_layout = [
    [sg.Button('Add Expense', key="-ADD EXPENSE-"), sg.Button('Show Summary', key="-SHOW SUMMARY-"), sg.Button('Exit', key="-EXIT-")],
]

main_window = sg.Window(
    "Expense Tracker Program",
    main_layout,
    element_justification="center",
    element_padding=(10, 10),
    finalize=True,
)

while True:
    event, values = main_window.read()

    if event in [sg.WIN_CLOSED, "-EXIT-"]:
        break

    if event == "-ADD EXPENSE-":
        register_expense()

    # Add logic for other events here

main_window.close()
        
        
   

        