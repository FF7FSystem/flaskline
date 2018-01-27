# -*- coding: utf-8 -*-
from termcolor import colored
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm
from app.models import User
from werkzeug.urls import url_parse
from datetime import datetime
from flask_login import current_user, login_user, logout_user, login_required

@app.route('/')
@app.route('/index')
@login_required
def index():
    print(colored('Загружается страница Index','yellow', attrs=['bold']))
    posts = [
        {   'author': {'username': 'Евгений'}, 'body': 'Beautiful day in Port!'},
        {   'author': {'username': 'Стас'},    'body': 'The Avengers movie was!'}, 
        {   'author': {'username': 'Дмитрий'}, 'body': 'Какая гадость эта ваша заливная ыба!!'}
            ]
    return render_template('index.html', title='Homer', posts=posts)

@app.route('/index2')
def index2(): #название функции любое, оно нужно чтобы декоратор роутерс  стройкой вышерендрил именно эту функцию)
    print(colored('Загружается страница Index2','yellow', attrs=['bold']))
    return render_template('index2.html', user="Юзерок-фраерок")

@app.route('/login', methods=['GET', 'POST'])
def login():
    print(colored('Загружается страница Login','yellow', attrs=['bold']))
    print(colored('Переменная - current_user равна = ','yellow', attrs=['bold']), current_user)


    if current_user.is_authenticated: # проверка, может пользователь уже авторизирован
        print(colored('Юзер уже авторизирован как - ','yellow', attrs=['bold']),current_user)
        return redirect(url_for('index'))

    form = LoginForm()
    print(colored('в переменной form - ','yellow', attrs=['bold']),form)
    if form.validate_on_submit():
        print(colored('Валидация полей логин-пароль пройдена','yellow', attrs=['bold']))
        user = User.query.filter_by(username=form.username.data).first()
        print(colored('В переменной user  - ','yellow', attrs=['bold']), user)
        if user is None or not user.check_password(form.password.data):
            flash('НЕверный логин или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        print(colored('В переменной next_page','yellow', attrs=['bold']),next_page)
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Логырование', form=form)

@app.route('/logout')
def logout():
    print(colored('Запущена функция logout','yellow', attrs=['bold']))
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    print(colored('Загружается страница Register','yellow', attrs=['bold']))
    if current_user.is_authenticated:
        print(colored('Если пользователь уже вошел в систему его кинет на страницу Idex','yellow', attrs=['bold']))
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user) # Добавление в таблицу данных пользователь-мыло-пароль
        db.session.commit() # Сохранение данных в таблице
        print(colored('считывание полей из формы прошли успешно и записаны в таблицу User','yellow', attrs=['bold']))
        flash('Поздравяем вы зарегались...Вас кинет на  строницу Логин ?')
        return redirect(url_for('login'))
    print(colored('Введеные данные в форму Регистрации не валидны, кидаем опять на страницу register.html','yellow', attrs=['bold']))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    print(colored('Загружается страница User (просмотр профиля)','yellow', attrs=['bold']))
    user = User.query.filter_by(username=username).first_or_404()
    print(colored('В переменной User (просмотр профиля)','yellow', attrs=['bold']), user)
    #в таблице User ищется зерегистрированый юзер  (глупость полная, мы же зарегались)
    # но ссылка динамичная потом видимо в ЮЗЕРНЕЙ будет передавться другие имена  для просмотра чужих станиц
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
            ]
    return render_template('user.html', user=user, posts=posts)
    #Открывается страница пользователя который вошел в систему потому что его данные передаются на входную функцию в ХТМЛ форме

@app.before_request
def before_request():
    print(colored('Запускается функция before_request','yellow', attrs=['bold']))
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    print(colored('Запускается функция edit_profile','yellow', attrs=['bold']))
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Изменения профайла были  сохранены')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)