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


def category_totals(cat_list):
    db = get_db()
    totals = []
    if type(cat_list) == list:
        # iterates throught the list of categories
        for item in cat_list:
            total = db.execute('SELECT category, ROUND(SUM(amount), 2) FROM transactions \
                                WHERE category = ? AND user_id = ?',
                                (item['category'], session['user_id'])
                                )
            budget = db.execute('SELECT ROUND(budget, 2) FROM categories WHERE category = ? AND user_id = ?',
                                (item['category'], session['user_id'])
                                ).fetchone()
                
                               
            for row in total:
                if row['category'] == None:
                    totals.append({'category' : item['category'], 'budget' : budget['ROUND(budget, 2)'] or None,'amount' : None})
                    print('1')
                else:
                    totals.append({'category' : row['category'], 'budget' : budget['ROUND(budget, 2)'] or None, 'amount' : row['ROUND(SUM(amount), 2)'] or None})
                    print('2')
        return totals
    # else input is not a list
    else:
        total = db.execute('SELECT category, ROUND(SUM(amount), 2) FROM transactions WHERE category = ? AND user_id = ?', (cat_list['category'], session['user_id'])).fetchall()
        for row in total:
            totals.append({'category' : row['category'], 'amount' : row['ROUND(SUM(amount), 2)']})
        return totals


def is_capital(CategoryDict):
    if type(CategoryDict) == dict:
        for key, word in CategoryDict.items():
            if word[0].islower():
                CategoryDict[key] = word.capitalize()
        return CategoryDict 
    elif type(CategoryDict) == str:
        CategoryDict = CategoryDict.capitalize()
        return CategoryDict
    elif type(CategoryDict) == list:
        for i, word in CategoryDict:
            CategoryDict[i] = word.capitalize
        return CategoryDict
    else:
        return CategoryDict


def has_category(category):
    db = get_db()
    HasCategory = db.execute('SELECT * FROM categories WHERE category = ? AND user_id= ?', (category, session['user_id'])).fetchone()
    if HasCategory:
        return True
    else:
        return False

