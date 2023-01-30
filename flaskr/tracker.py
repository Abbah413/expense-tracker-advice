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

            import_file(FileLocation)
            format_output(FileLocation)
            os.remove(FileLocation)

            return redirect(url_for('tracker.categories'))


    else:
        return render_template('tracker/import.html')

@bp.route('/categories', methods=['GET', 'POST'])
@login_required
def categories():
    db = get_db()
    output = db.execute('SELECT * FROM transactions WHERE user_id= ?', (session['user_id'],)).fetchall()
    #json_data = []
    if request.method == 'POST':
        json_data = request.get_json()
        print(json_data)
        db.execute('UPDATE transactions SET category = ? WHERE id = ?', (json_data['type'], json_data['id']))
        db.commit()
        return {'response': 'received'}

    else:
        return render_template('tracker/categories.html', output=output)
