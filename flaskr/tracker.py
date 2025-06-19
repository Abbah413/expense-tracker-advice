import os
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Blueprint, redirect, render_template, request, url_for, session, jsonify
from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.parse_csv import parse_csv
from flaskr.categories import format_output, category_totals, is_capital, has_category
from dateutil.parser import parse as parse_date

ALLOWED_EXTENSIONS = {'csv'}
UPLOAD_FOLDER = 'uploads'

bp = Blueprint('tracker', __name__)

# Check if uploaded file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# === ROUTES ===

@bp.route('/')
@login_required
def index():
    db = get_db()
    categories = db.execute(
        'SELECT category FROM categories WHERE user_id = ?', 
        (session['user_id'],)
    ).fetchall()
    
    totals = category_totals(categories)
    return render_template('tracker/index.html', categories=totals)

@bp.route('/', methods=['POST'])
@login_required
def append_summary():
    db = get_db()
    json_data = request.get_json()

    if not json_data or 'action' not in json_data or 'category' not in json_data:
        return jsonify({'response': 'invalid request'}), 400

    json_data = is_capital(json_data)
    category = json_data['category']

    if json_data['action'] == 'add':
        if not has_category(category):
            db.execute(
                'INSERT INTO categories (category, user_id) VALUES (?, ?)',
                (category, session['user_id'])
            )
            db.commit()
            total = category_totals(json_data)
            return jsonify({'category': category, 'amount': total[0]['amount'] if total else None})
        return jsonify({'response': 'already exists'})

    elif json_data['action'] == 'remove':
        db.execute(
            'DELETE FROM categories WHERE category = ? AND user_id = ?',
            (category, session['user_id'])
        )
        db.commit()
        return jsonify({'response': 'removed'})

    elif json_data['action'] == 'budget' and 'budget' in json_data:
        if has_category(category):
            db.execute(
                'UPDATE categories SET budget = ? WHERE category = ? AND user_id = ?',
                (json_data['budget'], category, session['user_id'])
            )
            db.commit()
            return jsonify({'response': 'budget updated'})
        return jsonify({'response': 'category not found'})

    return jsonify({'response': 'unknown action'}), 400

@bp.route('/transactions', methods=['GET', 'POST'])
@login_required
def transactions():
    db = get_db()

    if request.method == 'POST':
        json_data = request.get_json()
        if not json_data or 'action' not in json_data:
            return jsonify({'response': 'invalid request'}), 400

        json_data = is_capital(json_data)

        if json_data['action'] == 'Type' and 'category' in json_data and 'transid' in json_data:
            db.execute(
                'UPDATE transactions SET category = ? WHERE id = ? AND user_id = ?',
                (json_data['category'], json_data['transid'], session['user_id'])
            )
            db.commit()
            return jsonify({'response': 'updated'})

        elif json_data['action'] == 'Delete':
            db.execute('DELETE FROM transactions WHERE user_id = ?', (session['user_id'],))
            db.commit()
            return jsonify({'response': 'deleted'})

        elif json_data['action'] == 'Insert' and 'transactions' in json_data:
            inserted_count = 0
            for row in json_data['transactions']:
                amount = 0.0
                if row.get('deposit', 0) > 0:
                    amount = row['deposit']
                elif row.get('withdrawal', 0) > 0:
                    amount = -row['withdrawal']

                if amount == 0:
                    continue

                category = row.get('category', 'Uncategorized')
                date = row.get('date', '')
                desc = row.get('description', '')

                db.execute(
                    'INSERT INTO transactions (user_id, category, amount, date, description) VALUES (?, ?, ?, ?, ?)',
                    (session['user_id'], category, amount, date, desc)
                )
                inserted_count += 1

            db.commit()
            return jsonify({'response': f'inserted {inserted_count} transactions'})

        return jsonify({'response': 'unknown action'}), 400

    output = db.execute(
        'SELECT * FROM transactions WHERE user_id = ?',
        (session['user_id'],)
    ).fetchall()

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

    return jsonify({
        'labels': [row['month'] for row in data],
        'income': [row['income'] for row in data],
        'expense': [row['expense'] for row in data],
    })

@bp.route('/import', methods=['GET', 'POST'])
@login_required
def import_csv():
    if request.method == 'POST':
        file = request.files.get('file')
        if file and allowed_file(file.filename):
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            transactions = parse_csv(filepath)

            db = get_db()
            inserted_count = 0
            for row in transactions:
                amount = 0.0
                if row.get('deposit', 0) > 0:
                    amount = row['deposit']
                elif row.get('withdrawal', 0) > 0:
                    amount = -row['withdrawal']

                if amount == 0:
                    continue

                category = row.get('category', 'Uncategorized')
                date = row.get('date', '')
                desc = row.get('description', '')

                db.execute(
                    'INSERT INTO transactions (user_id, category, amount, date, description) VALUES (?, ?, ?, ?, ?)',
                    (session['user_id'], category, amount, date, desc)
                )
                inserted_count += 1

            db.commit()
            return redirect(url_for('tracker.transactions'))

        return "Invalid file type", 400

    return render_template('tracker/import.html')

# Helper
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

    return {
        row['category']: {"income": row['income'], "expense": row['expense']}
        for row in summary
    }
