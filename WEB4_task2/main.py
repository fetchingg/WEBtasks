from flask import Flask, render_template, redirect, abort, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import datetime

from data import db_session
from data.users import User
from data.news import News
from forms.user import RegisterForm
from forms.loginform import LoginForm
from forms.news import NewsForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route("/")
def index():
    db_sess = db_session.create_session()

    if current_user.is_authenticated:
        news = db_sess.query(News).filter(
            (News.user == current_user) |
            (News.is_private != True)
        )
    else:
        news = db_sess.query(News).filter(
            News.is_private != True
        )

    return render_template(
        "index.html",
        title="Главная",
        news=news
    )


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():

        if form.password.data != form.password_again.data:
            return render_template(
                'register.html',
                form=form,
                message="Пароли не совпадают"
            )

        db_sess = db_session.create_session()

        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template(
                'register.html',
                form=form,
                message="Такой пользователь уже есть"
            )

        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )

        user.set_password(form.password.data)

        db_sess.add(user)
        db_sess.commit()

        return redirect('/login')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

def main():
    db_session.global_init("db/blogs.db")
    app.run(port=8080)


if __name__ == '__main__':
    main()