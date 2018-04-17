from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from termcolor import colored
import logging
from logging.handlers import RotatingFileHandler
import os
from flask_bootstrap import Bootstrap
from flask_moment import Moment

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app) #представление базы данных
migrate = Migrate(app, db) #представление механизма миграции
login = LoginManager(app) # инициализация механизма логирования
bootstrap = Bootstrap(app) # инициализация НТМЛ фреймворка
moment = Moment(app)
login.login_view = 'login' #активация функции только зарегеные пользователи могут просмотреть  какието страницы
login.login_message = "Пожалуйста, зайдите под своим логином, чтобы открыть эту страницу." # Замена стандартного сообщения своим
from app import routes, models, errors # подключает к нашему приложению библиотеки (файлы которе мы создали)
'''
routes - отвечает за маршрутизацию и рендринг страниц
models - определяет структуру базы данных
errors - отрабатывает нащи оибки 404 и 500
'''
print(colored('Запущен файл __init__, пошли импорты','red', attrs=['bold']))
if not app.debug: #Модуль логирования  собятий с  уровня произшествий ИНФО
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')