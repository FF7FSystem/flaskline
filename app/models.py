from termcolor import colored
from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id):
	print(colored('Запустилась функция load_user','green', attrs=['bold']))
	return User.query.get(int(id))

class User(UserMixin, db.Model):
	print(colored('Описаниетаблицы User','green', attrs=['bold']))
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	posts = db.relationship('Post', backref='author', lazy='dynamic')

	def __repr__(self):
		return '<User {}>'.format(self.username)

	def set_password(self, password):
		print(colored('Генерация ХЭШ пароля','green', attrs=['bold']))
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		print(colored('Проверка хыша пароля и введеного пароля','green', attrs=['bold']))
		return check_password_hash(self.password_hash, password)

class Post(db.Model):
	print(colored('Описание таблицы Post','green', attrs=['bold']))
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Post {}>'.format(self.body)

