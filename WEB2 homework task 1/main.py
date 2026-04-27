from flask import Flask, render_template, redirect

app = Flask(__name__)


@app.route('/')
@app.route('/index/<title>')
def index(title="Главная"):
    return render_template('base.html', title=title)


@app.route('/distribution')
def distribution():
    astronauts = [
        "Вася Пупкин",
        "Наруто Петров",
        "Саске Сергеев",
        "Хацуне Мику"
    ]

    return render_template('distribution.html', astronauts=astronauts)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
