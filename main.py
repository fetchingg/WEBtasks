
from flask import Flask, render_template, redirect, abort, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import datetime

from data import db_session
from pymorphy3 import MorphAnalyzer
morph = MorphAnalyzer()

def change_city_name(city):

    words = city.split()
    changed_words = []

    for word in words:

        parsed = morph.parse(word)[0]

        changed = parsed.inflect({'loct'})

        if changed:
            changed_words.append(changed.word.title())
        else:
            changed_words.append(word)

    return " ".join(changed_words)


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

    city = request.args.get("city", "Москва")
    event_type = request.args.get("type", "Все события")

    city_changed = change_city_name(city)

    return render_template(
        "index.html",
        city=city,
        city_changed=city_changed,
        event_type=event_type
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