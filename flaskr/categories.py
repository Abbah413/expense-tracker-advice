from flask import session
from flaskr.db import get_db

def format_output(transactions, bank_name="Unknown"):
    formatted = []
    for t in transactions:
        formatted.append({
            "bank": bank_name,
            "date": t["date"],
            "description": t["description"],
            "amount": t["deposit"] if t["deposit"] > 0 else -t["withdrawal"],
            "category": "",  # to be filled in later
        })
    return formatted




def category_totals(cat_list):
    """
    Returns totals and budgets for each category in the list or a single category dict.
    """
    db = get_db()
    user_id = session['user_id']
    totals = []

    categories = (
        [item['category'] for item in cat_list] if isinstance(cat_list, list)
        else [cat_list['category']]
    )

    for category in categories:
        amount_row = db.execute(
            """
            SELECT ROUND(SUM(amount), 2) AS total_amount
            FROM transactions
            WHERE category = ? AND user_id = ?
            """,
            (category, user_id)
        ).fetchone()

        budget_row = db.execute(
            """
            SELECT ROUND(budget, 2) AS budget
            FROM categories
            WHERE category = ? AND user_id = ?
            """,
            (category, user_id)
        ).fetchone()

        totals.append({
            'category': category,
            'budget': budget_row['budget'] if budget_row else None,
            'amount': amount_row['total_amount'] if amount_row else 0
        })

    return totals

def is_capital(obj):
    """
    Capitalizes strings in str, dict, or list.
    """
    if isinstance(obj, str):
        return obj.capitalize()

    if isinstance(obj, dict):
        return {k: (v.capitalize() if isinstance(v, str) else v) for k, v in obj.items()}

    if isinstance(obj, list):
        return [item.capitalize() if isinstance(item, str) else item for item in obj]

    return obj

def has_category(category: str) -> bool:
    """
    Checks if category exists for the current user.
    """
    db = get_db()
    user_id = session['user_id']

    result = db.execute(
        """
        SELECT 1 FROM categories
        WHERE category = ? AND user_id = ?
        """,
        (category, user_id)
    ).fetchone()

    return result is not None
