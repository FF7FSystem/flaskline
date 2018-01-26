from termcolor import colored
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    print(colored('Создается класс Login','blue', attrs=['bold']))
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

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