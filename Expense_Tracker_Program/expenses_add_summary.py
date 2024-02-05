import sqlite3
import PySimpleGUI as sg
from datetime import datetime
from typing import Any
from expenses_db import connection, cursor

def add_expense(date: datetime, category: str, amount: float, description: str) -> bool:
    query = "INSERT INTO expanses (date, category, amount, description) VALUES (?,?,?,?)"
    
    try:
        with connection:
            cursor.execute(query, (date, category, amount, description))
    except Exception as error:
        sg.PopupOK(f"DB Error {error.__class__.__name__}: {error}", title="DB Error")
        return False
    else:
        sg.PopupOK(f"Expense added successfully.", title="Success")
        return True
    
def get_summary(period_from: datetime, period_to: datetime) -> list[Any]:
    query = '''
        SELECT strftime(?, date) as period_start,
        SUM(amount) as total_amout
        FROM category
        GROUP BY strftime(?, date)
        HAVING strftime(?, date) >=? AND strftime(?, date) <=?
        ORDER BY strftime(?, date)
    '''
    if period_from == 'weekly':
        result = cursor.execute(query, ('%Y-%m-%d', '%Y-%m-%d', '%Y-%m-%d', period_from, period_to, '%Y-%m-%d')).fetchall()
    elif period_from == 'monthly':
        result = cursor.execute(query, ('%Y-%m', '%Y-%m', '%Y-%m', period_from, period_to, '%Y-%m')).fetchall()
    elif period_from == 'yearly':
        result = cursor.execute(query, ('%Y', '%Y', '%Y', period_from, period_to, '%Y-%m-%d')).fetchall()


    return result