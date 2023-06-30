import csv
from flask import session
from flaskr.db import get_db
from datetime import datetime

# Add the data returned by the CSV parser to database
def format_output(data: list):
    db = get_db()
    # input each row of data into transactions table
    for row in data:
        db.execute(
            'INSERT INTO transactions (transacted, uploaded, bank, amount, description, category, user_id)'
            'VALUES (?, ?, ?, ?, ?, ?, ?)',
            (row[0], datetime.now(), row[1], row[2], row[3], row[4], session['user_id'])
            )
        db.commit()


def category_totals(cat_list: list | str) -> list:
    db = get_db()
    totals = []
    # If user is redirected to summary page
    if type(cat_list) == list:
        # Iterates throught users list of categories
        for item in cat_list:
            # Sums all expenses with the current category name
            total = db.execute('SELECT category, ROUND(SUM(amount), 2) FROM transactions \
                                WHERE category = ? AND user_id = ?',
                                (item['category'], session['user_id'])
                                )
            # Retrieve the budgeted amount for the current category
            budget = db.execute('SELECT ROUND(budget, 2) FROM categories WHERE category = ? AND user_id = ?',
                                (item['category'], session['user_id'])
                                ).fetchone()
            # Format the returned values          
            for row in total:
                # If the entry does not have a category name
                if row['category'] == None:
                    totals.append({'category' : item['category'], 'budget' : budget['ROUND(budget, 2)'] or None,'amount' : None})
                else:
                    totals.append({'category' : row['category'], 'budget' : budget['ROUND(budget, 2)'] or None, 'amount' : row['ROUND(SUM(amount), 2)'] or None})
        return totals
    # Else user added a new category
    else:
        total = db.execute('SELECT category, ROUND(SUM(amount), 2) FROM transactions WHERE category = ? AND user_id = ?', (cat_list['category'], session['user_id'])).fetchall()
        for row in total:
            totals.append({'category' : row['category'], 'amount' : row['ROUND(SUM(amount), 2)']})
        return totals


# Format category names to begin with a capital letter
def is_capital(CategoryDict: str | list | dict):
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


# Check if a category is in users categoyr in database
def has_category(category: str) -> bool:
    db = get_db()
    HasCategory = db.execute('SELECT * FROM categories WHERE category = ? AND user_id= ?', (category, session['user_id'])).fetchone()
    if HasCategory:
        return True
    else:
        return False
