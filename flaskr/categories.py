import csv
from flask import session
from flaskr.db import get_db
from datetime import datetime

fieldnames = ['date', 'bank', 'amount', 'description', 'type', 'id']

def format_output(filename):
    db = get_db()

    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        for row in reader:
            db.execute(
                'INSERT INTO transactions (transacted, uploaded, bank, amount, description, category, user_id)'
                'VALUES (?, ?, ?, ?, ?, ?, ?)',
                (row['date'], datetime.now(), row['bank'], row['amount'], row['description'], row['type'], session['user_id'])
                )
            db.commit()

            


