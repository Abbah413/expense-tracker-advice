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
from flaskr.categories import format_output


ALLOWED_EXTENSIONS = set(['csv'])

bp = Blueprint('tracker', __name__)

# check if imported file is csv
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
@login_required
def index():

    return render_template('tracker/index.html')


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

            return redirect(url_for('tracker.categories'))


    else:
        return render_template('tracker/import.html')

@bp.route('/categories', methods=['GET', 'POST'])
@login_required
def categories():
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
        db.execute('UPDATE transactions SET category = ? WHERE id = ?', (JsonData['category'], JsonData['transid'])).commit()

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
        return render_template('tracker/categories.html', output=output)
