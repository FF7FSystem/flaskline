from termcolor import colored
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, RadioField, SelectField
from flask_wtf.file import FileField,FileRequired, FileAllowed
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    print(colored('Создается класс Login','blue', attrs=['bold']))
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня на всегда )')
    submit = SubmitField('Вход')


class RegistrationForm(FlaskForm):
	#Форма Регистрации пользователей
    print(colored('Создается класс Registration','blue', attrs=['bold']))
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    #Поле password2 проверяет валидность пароля и сравнивает с полем password с помощью функции EaulTo

    def validate_username(self, username): # проверка в таблице User если введеный ник уже существует
        print(colored('Запущена функция проверки Валидации и наличия введеного ИМЕНИ в таблице User ','blue', attrs=['bold']))
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email): # Проверка в таблице User если такой емэил уже вводили
        print(colored('Запущена функция проверки Валидации и наличия введеного ЕМЭЙЛА в таблице User ','blue', attrs=['bold']))
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditProfileForm(FlaskForm):
    print(colored('Создается класс EditProfileForm','blue', attrs=['bold']))
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs): #ДАнный конструктор говорит что класс EditProfileForm не только наследуется от FlaskForm
        super(EditProfileForm, self).__init__(*args, **kwargs) # он так же наследует от себя новый метод так что при вызове self.original_username
        self.original_username = original_username # будет выводится original_username которое передавалось в данный класс 
                                        #например  form = EditProfileForm(current_user.username)  будет выдавать имя  вошедшего в систему пользователя  
    def validate_username(self, username): 
        if username.data != self.original_username: #Проверка что введеное в форму имя не равно тому пользователю который вошл в систему ( меняет совй ник на текущий = не меняет)
            user = User.query.filter_by(username=self.username.data).first() # поиск введеного в  форму имени в базе данных
            if user is not None: # если мы пытаемся изменить имя пользователя на такое как есть в базе данных то....
                raise ValidationError('Please use a different username.')

class Manyforms(FlaskForm):
    print(colored('Создается класс Manyforms','blue', attrs=['bold']))
    tablename = StringField('Сюда вводить текст', validators=[DataRequired()])
    Radio_choose = RadioField('Выбрать Таблицу', choices = 
        [('User', 'table User'),('Post', 'table Post'),('Empty','No table')])
    Listfield = SelectField('Список, выбрать тут:',choices = 
        [('none',''),('aria', 'Aria'), ('kipelov', 'Kipelov'), ('epidemia','Epidemia'),('master','Master')])
    Tafform = TextAreaField('Поле ввода текста ', validators=[Length(min=0, max=25),DataRequired()])
    Cheboxfield1 = BooleanField('чекбокс1', default=False)
    Cheboxfield2 = BooleanField('чекбокс2', default=False)
    Cheboxfield3 = BooleanField('чекбокс3', default=False)
    submit = SubmitField('Enter ')

class UploadForm(FlaskForm):
    print(colored('Создается класс UploadForm','blue', attrs=['bold']))
    fupload = FileField('Загрузка Файлов', validators=[
    FileRequired(),FileAllowed(['jpg','gif','ico'], 'онли jpg, gif,ico!')]) 
    #Проверка что форма не пустая, проверка расширения файла (из списка)
    submit = SubmitField('Загрузить ')
    
    