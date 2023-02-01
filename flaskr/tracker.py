import os
import json
import csv

from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, session,
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from datetime import datetime

from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.parse_csv import import_file
from flaskr.categories import format_output, category_totals


ALLOWED_EXTENSIONS = set(['csv'])

bp = Blueprint('tracker', __name__)

# check if imported file is csv
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    db = get_db()
    CategoryTotals = []
    cat_list = []
    # get the users categories from the table
    categories = db.execute('SELECT category FROM categories WHERE user_id = ?', (session['user_id'],)).fetchall()
    # returns the totals for each category
    for row in categories:
        i = 0
        cat_list[i] = row['category']
        print(cat_list[i])
        i+=1
    CategoryTotals = category_totals(cat_list)
    """
    for row in categories:
        CategoryTotals = category_totals(row['category'])
    """
    
    if request.method == "POST":
        # returns {category : 'value'}
        JsonData = request.get_json()
        print(JsonData)
        # check if the category exists in the table for current user
        HasCategory = db.execute('SELECT category_id FROM categories Where category = ? AND user_id = ?',
                                     (JsonData['category'], session['user_id'])).fetchall()
        # if the category is not in category table add it
        if not HasCategory:
            # add the new category to the table
            db.execute('INSERT INTO categories (category, user_id) VALUES (?, ?)', (JsonData['category'], session['user_id']))
            db.commit()
            """CurrentCategory = db.execute('SELECT category_id FROM categories Where category = ? AND user_id = ?',
                                        (JsonData['category'], session['user_id'])).fetchone()
            """
            total = category_totals(JsonData)

            return {'category' : JsonData['category'], 'amount' : total['SUM(amount)']}
        
        else:
            return {'response' : 'none'}

    return render_template('tracker/index.html', categories=CategoryTotals)


@bp.route('/import', methods=['GET', 'POST'])
@login_required
def import_csv():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            new_filename = f'{filename.split(".")[0]}_{str(datetime.now())}.csv'
            FileLocation = os.path.join('flaskr/UPLOAD_FOLDER', new_filename)
            file.save(FileLocation)

            # send the csv to the parser
            import_file(FileLocation)
            # input parsed csv into transactions table
            format_output(FileLocation)
            # delete the csv
            os.remove(FileLocation)

            return redirect(url_for('tracker.transactions'))


    else:
        return render_template('tracker/import.html')

@bp.route('/transactions', methods=['GET', 'POST'])
@login_required
def transactions():
    # access the database
    db = get_db()
    # select all the users transactions
    output = db.execute('SELECT * FROM transactions WHERE user_id= ?', (session['user_id'],)).fetchall()

    if request.method == 'POST':
        # get the category from users input in transaction form
        JsonData = request.get_json()
        # test variable
        print(JsonData)
        # add users category to corrisponding transaction
        db.execute('UPDATE transactions SET category = ? WHERE id = ?', (JsonData['category'], JsonData['transid']))
        db.commit()
        # check for user category in categories table
        HasCategory = db.execute('SELECT * FROM categories WHERE category = ? AND user_id= ?', (JsonData['category'],session['user_id'])).fetchone()
        # if users category in categories
        if HasCategory:
            return {'response': 'received'}
        # else return category not in table
        else:
            return {'response': 'none'}
    else:
        # output users transactions to the transaction form
        return render_template('tracker/transactions.html', output=output)
