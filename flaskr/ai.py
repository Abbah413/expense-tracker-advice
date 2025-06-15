from datetime import date
from flask import Blueprint, g, render_template
from flaskr.auth import login_required
from flaskr.db import get_db
from flaskr.tracker import get_summary_data
from openai import OpenAI
import os

bp = Blueprint('ai', __name__, url_prefix='/ai')

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@bp.route('/advice')
@login_required
def advice():
    db = get_db()
    user_id = g.user['user_id']

    today = date.today()
    row = db.execute(
        "SELECT content FROM advice WHERE user_id = ? AND DATE(created) = ?",
        (user_id, today)
    ).fetchone()

    if row:
        advice_content = row['content']
    else:
        summary = get_summary_data(user_id)
        prompt = f"Here is the user's category-wise spending: {summary}. Give clear financial advice to help them save more or improve their budgeting."

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful financial assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        advice_content = response.choices[0].message.content

        db.execute(
            "INSERT INTO advice (user_id, content) VALUES (?, ?)",
            (user_id, advice_content)
        )
        db.commit()

    return render_template('ai/advice.html', advice=advice_content)
