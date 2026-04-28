from flask import Flask, render_template, redirect

app = Flask(__name__)


@app.route('/')
@app.route('/index/<title>')
def index(title="Главная"):
    return render_template('base.html', title=title)


@app.route('/table/<gender>/<age>')
def table(gender, age):
    age = int(age)

    if gender == "male" and age < 21:
        img = "img/malekid.jpg"
        img_color = "img/pink1.png"
    elif gender == "male" and age >= 21:
        img = "img/maleadult.jpg"
        img_color = "img/green1.png"
    elif gender == "female" and age < 21:
        img = "img/femalekid.jpg"
        img_color = "img/blue1.jpg"
    elif gender == "female" and age >= 21:
        img = "img/femaleadult.jpg"
        img_color = "img/idk1.jpg"
    else:
        img = ""
        img_color = ""

    return render_template('table.html', img=img, img_color=img_color)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
