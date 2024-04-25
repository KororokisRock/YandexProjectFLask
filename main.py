from flask import Flask
from flask import render_template
from flask import redirect

from flask_restful import Api

from data import db_session
from data import jobs_resource
from data import users_resource
from data.user import User

from forms.user import RegisterForm
from forms.user import LoginForm

from flask_login import LoginManager
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    return user


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            db_sess.close()
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            description=form.description.data,
            status_id=0,
            command_id=0
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        db_sess.close()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            db_sess.close()
            return redirect(f"/api/v2/users/{user.id}")
        db_sess.close()
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


def main():
    db_session.global_init("db/blogs.db")
    api.add_resource(jobs_resource.JobListResource, '/api/v2/jobs')
    api.add_resource(jobs_resource.JobResource, '/api/v2/jobs/<int:job_id>')
    api.add_resource(jobs_resource.JobCreateResource, '/api/v2/jobs_create')
    api.add_resource(users_resource.UserListResource, '/api/v2/users')
    api.add_resource(users_resource.UserResource, '/api/v2/users/<int:user_id>')
    api.add_resource(users_resource.UserRedactResource, '/api/v2/user_redact/<int:user_id>')
    app.run()


if __name__ == '__main__':
    main()
