from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Успешный логин!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Неверный пароль, попробуйте снова.', category='error')
        else:
            flash('Email не существует.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        second_name = request.form.get('secondName')
        third_name = request.form.get('thirdName')
        iin = request.form.get('iin')
        address = request.form.get('address')
        phone_num = request.form.get('phone')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email уже существует.', category='error')
        elif len(email) < 4:
            flash('Email должен иметь больше 3 символов.', category='error')
        elif len(first_name) < 2:
            flash('Имя должно содержать больше 1 символа.', category='error')
        elif password1 != password2:
            flash('Пароли не совпадают.', category='error')
        elif len(password1) < 7:
            flash('Пароль должен состоять минимум из 7 символов.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, 
            second_name=second_name, third_name=third_name, 
            iin=iin, address=address, phone_num=phone_num,
            password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Аккаунт создан!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
