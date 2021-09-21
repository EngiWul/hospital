from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import pyodbc
import sqlite3
from flask import g
import re
from datetime import datetime
from website import connStr
from website import DB_NAME
views = Blueprint('views', __name__)
items = [
        {'doc':'кардиолог','docfio':'АБВ','diagnoz':'герпес','zhaloby':'боль','date':'28.02.2021'},
        {'doc':'кардиолог','docfio':'АБВ','diagnoz':'герпес','zhaloby':'боль','date':'28.02.2021'}
    ]
# conn = pyodbc.connect(connStr)
# cursor = conn.cursor()
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('website/'+DB_NAME)
    return db
format = "%Y-%m-%d"
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        doc = request.form.get('doc')
        docfio = request.form.get('docfio')
        diagnoz = request.form.get('diagnoz')
        zhaloby = request.form.get('zhaloby')
        date = request.form.get('date')
        print(datetime.strptime(date, format),datetime.now(),int(date.split('-')[0]))
        if len(doc) < 1:
            flash('Выберите специалиста!', category='error')
        elif len(docfio) < 2 or bool(re.search('[^a-zA-Zа-яА-Я\s]', docfio)):
            flash('Некорректное ФИО!', category='error')
        elif len(diagnoz) < 1:
            flash('Введите диагноз!', category='error')
        elif len(zhaloby) < 1:
            flash('Введите жалобу пациента!', category='error')
        elif len(date) < 1:
            flash('Выберите дату!', category='error')
        elif datetime.strptime(date, format) > datetime.now() or int(date.split('-')[0])<2000:
            flash('Выберите корректную дату!', category='error')
        else:
            new_note = Note(doc = doc, docfio = docfio,
                            diagnoz = diagnoz, zhaloby = zhaloby,
                            date = date, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Запись добавлена!', category='success')
    cursor = get_db().cursor()
    cursor.execute('''select
      [doc]
      ,[docfio]
      ,[diagnoz]
      ,[zhaloby]
      ,[date]
      FROM note
    ''')
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
    cursor = get_db().cursor()
    cursor.execute("""select
      [first_name]
      ,[second_name]
      ,[third_name]
      ,[email]
      ,[iin]
      ,[address]
      ,[phone_num]
    FROM user""")
    data = cursor.fetchall()    

    search = request.args.get('search')
    data1 = []
    for d in data:
        if search.isalpha():
            if d[0].startswith(search) or d[1].startswith(search) or d[2].startswith(search):
                data1.append(d)
            else:
                flash('Нет совпадений по ФИО!', category='error')
        elif search.isnumeric():
            if d[4].startswith(search):
                data1.append(d)
            else:
                flash('Нет совпадений по ИИН!', category='error')
        else:
            flash('Некорректный запрос поиска!', category='error')


            
    return render_template("search.html", user=current_user, data=data1)

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
