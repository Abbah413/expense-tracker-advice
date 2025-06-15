import os
from datetime import datetime
from werkzeug.utils import secure_filename

from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.parse_csv import parse_csv
from flaskr.categories import format_output, category_totals, is_capital, has_category
from flask import (
    Blueprint, redirect, render_template, request, url_for, session, jsonify
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
        if not has_category(json_data['category']):
            db.execute('INSERT INTO categories (category, user_id) VALUES (?, ?)', (json_data['category'], session['user_id']))
            db.commit()
            total = category_totals(json_data)
            send_json = {'category': json_data['category'], 'amount': total[0]['amount']}
            return send_json
        else:
            return {'response': None}
    if json_data['action'] == 'remove':
        db.execute('DELETE FROM categories WHERE category = ? AND user_id = ?', (json_data['category'], session['user_id']))
        db.commit()
        if not has_category(json_data['category']):
            return {'response': 'removed'}
        else:
            return {'response': None}
    if json_data['action'] == 'budget' and has_category(json_data['category']):
        db.execute('UPDATE categories SET budget = ? WHERE category = ? AND user_id = ?', (json_data['budget'], json_data['category'], session['user_id']))
        db.commit()
        return {'response': 'added'}
    else:
        return {'response': None}

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
            parsed_data = parse_csv(FileLocation)
            os.remove(FileLocation)
            format_output(parsed_data)
            return redirect(url_for('tracker.transactions'))
    else:
        return render_template('tracker/import.html')

@bp.route('/transactions', methods=['GET', 'POST'])
@login_required
def transactions():
    db = get_db()
    output = db.execute('SELECT * FROM transactions WHERE user_id= ?', (session['user_id'],)).fetchall()

    if request.method == 'POST':
        json_data = request.get_json()
        json_data = is_capital(json_data)

        if json_data['action'] == 'Type':
            db.execute('UPDATE transactions SET category = ? WHERE id = ?', (json_data['category'], json_data['transid']))
            db.commit()
            if has_category(json_data['category']):
                return {'response': 'received'}
            else:
                return {'response': None}

        if json_data['action'] == 'Delete':
            db.execute('DELETE FROM transactions WHERE user_id = ?', (session['user_id'],))
            db.commit()
            return {'response': 'deleted'}
    else:
        return render_template('tracker/transactions.html', output=output)

@bp.route('/summary')
@login_required
def summary():
    db = get_db()
    user_id = session['user_id']

    monthly_data = db.execute("""
        SELECT 
            strftime('%Y-%m', date) AS month,
            SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) AS income,
            SUM(CASE WHEN amount < 0 THEN -amount ELSE 0 END) AS expense
        FROM transactions
        WHERE user_id = ?
        GROUP BY month
        ORDER BY month
    """, (user_id,)).fetchall()

    return render_template('tracker/summary.html', monthly_data=monthly_data)

@bp.route('/chart-data')
@login_required
def chart_data():
    db = get_db()
    user_id = session['user_id']

    data = db.execute("""
        SELECT 
            strftime('%Y-%m', date) AS month,
            SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) AS income,
            SUM(CASE WHEN amount < 0 THEN -amount ELSE 0 END) AS expense
        FROM transactions
        WHERE user_id = ?
        GROUP BY month
        ORDER BY month
    """, (user_id,)).fetchall()

    chart_data = {
        'labels': [row['month'] for row in data],
        'income': [row['income'] for row in data],
        'expense': [row['expense'] for row in data],
    }

    return jsonify(chart_data)

from flaskr.db import get_db

def get_summary_data(user_id):
    db = get_db()
    summary = db.execute("""
        SELECT 
            category,
            SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) AS income,
            SUM(CASE WHEN amount < 0 THEN -amount ELSE 0 END) AS expense
        FROM transactions
        WHERE user_id = ?
        GROUP BY category
    """, (user_id,)).fetchall()

    # Return a simple dictionary for prompting GPT
    return {row['category']: {"income": row['income'], "expense": row['expense']} for row in summary}
