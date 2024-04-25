from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, BooleanField, DateField, SelectField, DecimalField
from wtforms.validators import DataRequired
from wtforms import validators


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    description = TextAreaField("Немного о себе")
    submit = SubmitField('Войти')


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class JobCloseForm(FlaskForm):
    submit = SubmitField('Закрыть задачу')


class JobCreateForm(FlaskForm):
    title = StringField('Заголовок задания')
    description = TextAreaField('Описание задания')
    start_date = DateField('Дата начала')
    end_date = DateField('Дата окончания')
    user_id = SelectField('ID Пользователя', choices=[0], coerce=int)
    submit = SubmitField('Создать')


class UserRedactLowLevelForm(FlaskForm):
    name = StringField('Имя')
    description = StringField('Описание', [validators.length(max=100)])
    email = StringField('Почта')
    submit = SubmitField('Сохранить')


class UserRedactHightLevelForm(FlaskForm):
    name = StringField('Имя')
    description = StringField('Описание', [validators.length(max=100)])
    email = StringField('Почта')
    command_id = SelectField('Команда', choices=[0], coerce=int)
    status_id = SelectField('Статус', choices=[0], coerce=int)
    submit = SubmitField('Сохранить')


class UserDeleteAccountForm(FlaskForm):
    submit = SubmitField('Удалить аккаунт')
