# -*- coding: utf-8 -*-
from termcolor import colored
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm ,Manyforms, UploadForm, PostForm #Импортирование форм
from app.models import User, Post #импортирование таблиц
from werkzeug.urls import url_parse
from datetime import datetime
from flask_login import current_user, login_user, logout_user, login_required
import os
from werkzeug.utils import secure_filename

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    print(colored('Загружается страница Index','yellow', attrs=['bold']))
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Райз май сан (или о чудо пост опубликовался)')
        return redirect(url_for('index'))

    page = request.args.get('page', 1, type=int) # считывает с  адресной строки значение page=
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, app.config['POST_PER_PAGE'], False)
    # posts делает запрос в базу с учетом пагинации и числа считаного с адресной строки
    if posts.has_next: #Тру если  в нашей поагинации есть следующая страница
        next_url = url_for('index', page=posts.next_num) #добавить в урл значение page= номер следующей строаници
    else: next_url=None
    if posts.has_prev:
        prev_url = url_for('index', page=posts.prev_num)
    else: prev_url=None
    
    return render_template("index.html", title='Index page', form=form,  posts=posts.items,next_url=next_url, prev_url=prev_url)

@app.route('/index2',  methods=['GET', 'POST'])
def index2(): #название функции любое, оно нужно чтобы декоратор роутерс  стройкой вышерендрил именно эту функцию)
    print(colored('Загружается страница Index2','yellow', attrs=['bold']))
    form= Manyforms()
    if form.validate_on_submit():
        value=form.tablename.data
        value2=form.Radio_choose.data
        value3=form.Listfield.data
        value4=form.Tafform.data
       
    else:
        value,value2,value3,value4='none','none','none','none'
    
    value5=form.Cheboxfield1.data
    value6=form.Cheboxfield2.data
    value7=form.Cheboxfield3.data
    #далее считывание со страницы и обработка  форм
    checkbox_list=['number1','number2','number3'] #для динамического создания чекбоксов по кол-ву элементов
    if request.method == 'POST':
        for checkbox_value in request.form: #создает список всех форм которые применены на странице
        #в список попадают формы которые были применены ( Например если чекбокс не нажат или в текстовое поле 
        # не введена инфа то  данная форма в список не попадет как будто ее нет на странице)
            temp=checkbox_value + '---->' +(request.form[checkbox_value])
            #выше строка выдует значение "value" формы, которая задействована на странице, соответств есть в списке)
            print(temp)

    return render_template('index2.html', user="Юзерок-фраерок",form=form, value=value,value2=value2,
        value3=value3,value4=value4,value5=value5,value6=value6,value7=value7,checkbox_list=checkbox_list)    

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
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(page, app.config['POST_PER_PAGE'], False)
    if posts.has_next: #описание работы пагинации в функции индекс
        next_url = url_for('user', username=user.username, page=posts.next_num) 
        '''в данном коде в адресную строку передается username и page, это нужно чтобы при нажатии на ссылки 
         next_url,  prev_url на страницу ЮЗЕР в строку адреса передавался текущий юзер и номер страници пагинации, по нему происходит
         переданное имя юера сравнивается с  данными в таблице юзер выше, если есть такой функция продолжает работу)
        также имя юзера передается на базовой страниеце в ссылке, чтобы на данную странице мог зайти только залогиненый юзер
        запись о котором есть в таблице юзер
    '''
    else: next_url=None
    if posts.has_prev:
        prev_url = url_for('user',username=user.username, page=posts.prev_num)
    else: prev_url=None
    return render_template('user.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)
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
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Изменения профайла были  сохранены')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/table')
def table(): #
    print(colored('Загружается страница table','yellow', attrs=['bold']))
    inf_for_table=User.for_table()
    table=[[ getattr(i,j) for j in inf_for_table['public']] for i in User.query.all()]
    for_thead=inf_for_table['public']
    service_tab=inf_for_table['service']

    return render_template( 'table.html', user="Юзерок-фраерок",title='Таблица',
        table=table,for_thead=for_thead,service_tab=service_tab)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    print(colored('Запускается функция upload','yellow', attrs=['bold']))
    form = UploadForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            file = form.fupload.data #присваеваем переменной содержимое файла кажись
            '''Если размер загружаемого файла больше чем задано в конфиге в переменной 'MAX_CONTENT_LENGTH'
            Приложение выдает ошибку 413. Можно сделать сравнение типа:       
            if len(file.read())<="число меньше чем в 'MAX_CONTENT_LENGTH" тогда отрабатывать, если нет , то писать уведомление пользователю о привышении.''' 
            filename = file.filename #изымаем имя файла из формы
            filename = secure_filename(filename) #если имя файла некорекное (спец символы) сохраняет без спец символов
            print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                
    return render_template('upload.html', title='Upload/Download',form=form)


@app.route('/forcss')
def for_css():
    print(colored('Загружается страница forcss','yellow', attrs=['bold']))
    return render_template('forcss.html', title='CSS exp')