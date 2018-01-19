# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'MegBegb+'}
    posts = [
        {
            'author': {'username': 'Евгений'},
            'body': 'Beautiful day in Port!'
        },
        {
            'author': {'username': 'Стас'},
            'body': 'The Avengers movie was!'
        }, 
        {
            'author': {'username': 'Дмитрий'},
            'body': 'Какая гадость эта ваша заливная ыба!!'
        }
    ]
    return render_template('index.html', title='Homer', user=user, posts=posts)

@app.route('/index2')
def index2(): #название функции любое, оно нужно чтобы декоратор роутерс  стройкой вышерендрил именно эту функцию)
    user = {'username': 'MegBegb+'}
    return render_template('index2.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Сообщение после логирования для юзера {}, Поле "запоснить пасс" заполнено ? = {}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Логырование', form=form)