from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from termcolor import colored

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app) #представление базы данных
migrate = Migrate(app, db) #представление механизма миграции
login = LoginManager(app) # инициализация механизма логирования
login.login_view = 'login' #активация функции только зарегеные пользователи могут просмотреть  какието страницы
from app import routes, models #models - определяет структуру базы данных
