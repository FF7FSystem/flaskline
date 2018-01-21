# -*- coding: utf-8 -*-
from termcolor import colored
from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
@login_required
def index():
    print(colored('Загружается страница Index','cyan', attrs=['bold']))
    posts = [
        {   'author': {'username': 'Евгений'}, 'body': 'Beautiful day in Port!'},
        {   'author': {'username': 'Стас'},    'body': 'The Avengers movie was!'}, 
        {   'author': {'username': 'Дмитрий'}, 'body': 'Какая гадость эта ваша заливная ыба!!'}
            ]
    return render_template('index.html', title='Homer', posts=posts)

@app.route('/index2')
def index2(): #название функции любое, оно нужно чтобы декоратор роутерс  стройкой вышерендрил именно эту функцию)
    print(colored('Загружается страница Index2','cyan', attrs=['bold']))
    return render_template('index2.html', user="Юзерок-фраерок")

@app.route('/login', methods=['GET', 'POST'])
def login():
    print(colored('Загружается страница Login','cyan', attrs=['bold']))
    print(colored('Переменная - current_user равна = ','cyan', attrs=['bold']), current_user)


    if current_user.is_authenticated: # проверка, может пользователь уже авторизирован
        print(colored('Юзер уже авторизирован как - ','cyan', attrs=['bold']),current_user)
        return redirect(url_for('index'))

    form = LoginForm()
    print(colored('в переменной form - ','cyan', attrs=['bold']),form)
    if form.validate_on_submit():
        print(colored('Валидация полей логин-пароль пройдена','cyan', attrs=['bold']))
        user = User.query.filter_by(username=form.username.data).first()
        print(colored('В переменной user  - ','cyan', attrs=['bold']), user)
        if user is None or not user.check_password(form.password.data):
            flash('НЕверный логин или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        print(colored('В переменной next_page','cyan', attrs=['bold']),next_page)
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Логырование', form=form)

@app.route('/logout')
def logout():
    print(colored('Запущена функция logout','cyan', attrs=['bold']))
    logout_user()
    return redirect(url_for('index'))