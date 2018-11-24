from termcolor import colored
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, RadioField, SelectField
from flask_wtf.file import FileField,FileRequired, FileAllowed
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    print(colored('Создается класс Login','blue', attrs=['bold']))
    username = StringField('User name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')

    submit = SubmitField('Enter')


class RegistrationForm(FlaskForm):
	#Форма Регистрации пользователей
    print(colored('Создается класс Registration','blue', attrs=['bold']))
    username = StringField('User name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    recaptcha = RecaptchaField ()
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
    username = StringField('Имя пользователя:', validators=[DataRequired()])
    about_me = TextAreaField('О себе:', validators=[Length(min=0, max=140)])
    submit = SubmitField('Применить')

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
        [('1', 'Проедете перекресток первым'),
        ('2', 'Проедете перекресток одновременно со встречным автомобилем до проезда мотоцикла'),
        ('3','Проедете перекресток последним')])
    Listfield = SelectField('Форма "список",используется для выбора значения из представленных вариантов:',choices = 
        [('Яблоко','Яблоко'),('Мячик', 'Мячик'), ('Синхрофазатрон', 'Синхрофазатрон'), ('Груша','Груша'),('Апельсин','Апельсин')])
    Tafform = TextAreaField('Форма "ввод текста", на данном сайте применяется для заполнения и публикации  сообщений на  главной странице ', validators=[Length(min=0, max=250),DataRequired()])
    Cheboxfield1 = BooleanField('Лох-несское чудовище', default=False)
    Cheboxfield2 = BooleanField('Кот', default=False)
    Cheboxfield3 = BooleanField('Королева банши "Сильвана Ветрокрылая"', default=False)
    Cheboxfield4 = BooleanField('Единорог', default=False)
    Cheboxfield5 = BooleanField('Скотч-терьер', default=False)
    submit = SubmitField('Enter ')

class UploadForm(FlaskForm):
    print(colored('Создается класс UploadForm','blue', attrs=['bold']))
    fupload = FileField('', validators=[
    FileRequired(),FileAllowed(['jpg','gif','ico'], 'Загружать можно  файлы только с расширением jpg, gif, ico!')]) 
    #Проверка что форма не пустая, проверка расширения файла (из списка)
    submit = SubmitField('Загрузить')
    
class PostForm(FlaskForm):
    post = TextAreaField('Заполнив форму, вы можете оставить запись на стене', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Оставить запись ')
    