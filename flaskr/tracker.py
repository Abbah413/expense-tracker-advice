import os
from datetime import datetime

from werkzeug.utils import secure_filename

from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.parse_csv import parse_csv
from flaskr.categories import format_output, category_totals, is_capital,has_category
from flask import (
    Blueprint, redirect, render_template, request, url_for, session,
)


ALLOWED_EXTENSIONS = set(['csv'])

bp = Blueprint('tracker', __name__)

# Check if imported file is csv
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
@login_required
def index():
    db = get_db()
    totals = []
    # Get the users categories from the table
    categories = db.execute('SELECT category FROM categories WHERE user_id = ?', (session['user_id'],)).fetchall()
    # Returns the totals for each category
    totals = category_totals(categories)
    return render_template('tracker/index.html', categories=totals)

@bp.route('/', methods=['POST'])
@login_required
def append_summary():
    db = get_db()
    json_data = request.get_json() # Returns {category : 'value'}
    if json_data['action'] == 'add':
        json_data = is_capital(json_data)        
        # If the category is not in category table add it
        if not has_category(json_data['category']):
            # Add the new category to the table
            db.execute('INSERT INTO categories (category, user_id) VALUES (?, ?)', (json_data['category'], session['user_id']))
            db.commit()
            total = category_totals(json_data) # Returns the category totals
            # Sets the format to return the totals then returns them
            send_json = {'category' : json_data['category'], 'amount' : total[0]['amount']}
            return send_json
        else:
            return {'response' : None}
    # Removes a category from the users list
    if json_data['action'] == 'remove':
        db.execute('DELETE FROM categories WHERE category = ? AND user_id = ?', (json_data['category'], session['user_id']))
        db.commit()
        if not has_category(json_data['category']):
            return {'response' : 'removed'}
        else:
            return {'response' : None}
    # Add budget value for the specified category to the categories table
    if json_data['action'] == 'budget' and has_category(json_data['category']):
        db.execute('UPDATE categories SET budget = ? WHERE category = ? AND user_id = ?', ((json_data['budget']), json_data['category'], session['user_id']))
        db.commit()
        return {'response' : 'added'}
    else:
        return {'response' : None}



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
            # Send the csv to the parser
            parsed_data = parse_csv(FileLocation)
            # Delete the csv
            os.remove(FileLocation)
            # Append the transactions table with the parsed data
            format_output(parsed_data)

            return redirect(url_for('tracker.transactions'))
    else:
        return render_template('tracker/import.html')

@bp.route('/transactions', methods=['GET', 'POST'])
@login_required
def transactions():
    # Access the database
    db = get_db()
    # Select all the users transactions
    output = db.execute('SELECT * FROM transactions WHERE user_id= ?', (session['user_id'],)).fetchall()

    if request.method == 'POST':
        # Get the category from users input in transaction form
        json_data = request.get_json()
        json_data = is_capital(json_data)

        if json_data['action'] == 'Type':
            # Add users category to corrisponding transaction
            db.execute('UPDATE transactions SET category = ? WHERE id = ?', (json_data['category'], json_data['transid']))
            db.commit()
            # Check for user category in categories table
            # If users category in categories
            if has_category(json_data['category']):
                return {'response': 'received'}
            # Else return category not in table
            else:
                return {'response': None}
        # Clear the users transactions from the transactions table
        if json_data['action'] == 'Delete':
            db.execute('DELETE FROM transactions WHERE user_id = ?', (session['user_id'],))
            db.commit()
            return {'response': 'deleted'}
    else:
        # output users transactions to the transaction form
        return render_template('tracker/transactions.html', output=output)
