import csv
from flask import session
from flaskr.db import get_db
from datetime import datetime

# list of fields for the reader to use
fieldnames = ['date', 'bank', 'amount', 'description', 'type', 'id']

def format_output(filename):
    db = get_db()

    # open parsed csv then read from csv
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        # inputeach row of csv into transactions table
        for row in reader:
            db.execute(
                'INSERT INTO transactions (transacted, uploaded, bank, amount, description, category, user_id)'
                'VALUES (?, ?, ?, ?, ?, ?, ?)',
                (row['date'], datetime.now(), row['bank'], row['amount'], row['description'], row['type'], session['user_id'])
                )
            db.commit()

def category_totals(cat_list = []):
    db = get_db()
    totals = []
    print(cat_list)
    # iterates throught the list of categories
    for item in cat_list:
        print('Item: ', item)
        total = db.execute('SELECT category, SUM(amount) FROM transactions WHERE category = ? AND user_id = ?', (item, session['user_id'])).fetchall()
        for row in total:
            print(row['category'], ' cat')
            print(row['SUM(amount)'], 'sum')
        return total
            


