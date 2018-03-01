import os
from termcolor import colored

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	print(colored('Запущен файл Конфига и создан класс Config','red', attrs=['bold']))

	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you not shell passadena'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False

		#ALLOWED_EXTENSIONS = set(['py'])
	UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or os.path.join(basedir,'app/uploads/')
	MAX_CONTENT_LENGTH = os.environ.get('MAX_CONTENT_LENGTH') or (5 * 1024 * 1024) #Задает размер саксимального объема данных которых фласк может загрузить