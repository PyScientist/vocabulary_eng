from app import app
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from urllib.parse import urlsplit
import sqlalchemy as sa

from app import db
from app.forms import SubmitWordForm, LoginForm, RegistrationForm, MassUploadWordsForm
from app.models import Users, Words

from vocabulary_backend.DbHandlers import DbTextAnalyser

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home Page')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user_reg = Users(name=form.username.data, nickname=form.username.data,
                         email=form.email.data, password_hash=form.password.data)
        user_reg.set_password(form.password.data)
        db.session.add(user_reg)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Registration', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user_to_login = db.session.scalar(sa.select(Users).where(Users.nickname == form.username.data))
        if user_to_login is None or not user_to_login.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user_to_login, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<username>')
@login_required
def user(username):
    page_owner = db.first_or_404(sa.select(Users).where(Users.nickname == username))
    page_owner_words = db.session.scalars(sa.select(Words).where(Words.user_id == page_owner.id))
    return render_template('user.html', user=page_owner, words=page_owner_words)


@app.route('/vocabulary_table')
@login_required
def vocabulary_table():
    words = [
        {'name': 'first word'},
        {'name': 'second word'}
    ]
    return render_template('vocabulary_table.html', words=words)


@app.route('/submit_word', methods=['GET', 'POST'])
@login_required
def submit_word():
    form = SubmitWordForm()
    if form.validate_on_submit():
        flash(f'The following word is given {form.name.data}')
        return redirect(url_for('index'))
    return render_template('submit_word.html', form=form)


@app.route('/mass_upload_words', methods=['GET', 'POST'])
@login_required
def mass_upload_words():
    form = MassUploadWordsForm()
    if form.validate_on_submit():
        words = []
        for word in words:
            w = Words(name=word[1], speach_part=word[2], translations=word[3],
                      definition=word[4], importance=word[5], topic=word[6], user_id=current_user.id)
            db.session.add(w)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('mass_upload_words.html', form=form)

@app.route('/test')
def test():
    return render_template('test.html')
