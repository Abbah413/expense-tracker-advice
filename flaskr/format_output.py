from flaskr.db import get_db
from flask import session

def format_output(parsed_data):
    db = get_db()

    for row in parsed_data:
        # Ensure required fields exist
        date = row.get('date')
        description = row.get('description', '')
        amount = row.get('amount', 0.0)
        category = row.get('category', 'Uncategorized')

        # Insert into DB
        db.execute(
            '''
            INSERT INTO transactions (user_id, date, description, amount, category)
            VALUES (?, ?, ?, ?, ?)
            ''',
            (session['user_id'], date, description, amount, category)
        )
    
    db.commit()
    print(f"Inserted {len(parsed_data)} transactions for user {session['user_id']}")
