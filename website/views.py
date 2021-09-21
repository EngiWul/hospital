from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import pyodbc
from website import connStr
views = Blueprint('views', __name__)
items = [
        {'doc':'кардиолог','docfio':'АБВ','diagnoz':'герпес','zhaloby':'боль','date':'28.02.2021'},
        {'doc':'кардиолог','docfio':'АБВ','diagnoz':'герпес','zhaloby':'боль','date':'28.02.2021'}
    ]
conn = pyodbc.connect(connStr)
cursor = conn.cursor()


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        doc = request.form.get('doc')
        docfio = request.form.get('docfio')
        diagnoz = request.form.get('diagnoz')
        zhaloby = request.form.get('zhaloby')
        date = request.form.get('date')

        if len(doc) < 1:
            flash('Запись слишком короткая!', category='error')
        else:
            new_note = Note(doc = doc, docfio = docfio,
                            diagnoz = diagnoz, zhaloby = zhaloby,
                            date = date, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Запись добавлена!', category='success')
    cursor.execute("""
    select
      [doc]
      ,[docfio]
      ,[diagnoz]
      ,[zhaloby]
      ,[date]
      FROM [efc].[dbo].[note]
    """)
    items = cursor.fetchall()
    print(items)
    return render_template("home.html", user=current_user, items=items)

@views.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    # if request.method == 'POST':
    #     note = request.form.get('note')

    #     if len(note) < 1:
    #         flash('Запись слишком короткая!', category='error')
    #     else:
    #         new_note = Note(data=note, user_id=current_user.id)
    #         db.session.add(new_note)
    #         db.session.commit()
    #         flash('Запись добавлена!', category='success')
    cursor.execute("""select
      [email]
      ,[first_name]
      ,[second_name]
      ,[third_name]
      ,[iin]
      ,[address]
      ,[phone_num]
    FROM [efc].[dbo].[user]""")
    data = cursor.fetchall()
    return render_template("search.html", user=current_user, data=data)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
