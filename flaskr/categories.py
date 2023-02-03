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
            total = db.execute('SELECT transactions.category, ROUND(SUM(amount)), categories.budget \
                                FROM transactions \
                                JOIN categories ON transactions.category = categories.category \
                                WHERE transactions.category = ? AND transactions.user_id = ?',
                                (item['category'], session['user_id'])
                                ).fetchall()
                                
            for row in total:
                if row['category'] == None:
                    totals.append({'category' : item['category'], 'amount' : None})
                if row['budget'] == None:
                    totals.append({'category' : row['category'], 'amount' : row['ROUND(SUM(amount))']})
                else:
                    totals.append({'category' : row['category'], 'budget' : row['budget'], 'amount' : row['ROUND(SUM(amount))']})
        return totals
    # else input is not a list
    else:
        total = db.execute('SELECT category, ROUND(SUM(amount)) FROM transactions WHERE category = ? AND user_id = ?', (cat_list['category'], session['user_id'])).fetchall()
        for row in total:
            totals.append({'category' : row['category'], 'amount' : row['ROUND(SUM(amount))']})
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
    HasCategory = db.execute('SELECT * FROM categories WHERE category = ? AND user_id= ?', (category,session['user_id'])).fetchone()
    if HasCategory:
        return True
    else:
        return False


    """
        SELECT transactions.amount, categories.budget, categories.category
        FROM transactions 
        LEFT JOIN transactions
        ON transactions.category = categories.category
        WHERE category = "Gasoline" AND user_id = 1

        SELECT transactions.category, ROUND(SUM(transactions.amount)), categories.budget
        FROM transactions
        JOIN categories ON transactions.category = categories.category
        WHERE transactions.category = "Gasoline" AND transactions.user_id = 1
        GROUP BY transactions.category;
    """
