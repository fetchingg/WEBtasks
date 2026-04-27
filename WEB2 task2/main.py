from flask import Flask, render_template, redirect

app = Flask(__name__)


@app.route('/')
@app.route('/index/<title>')
def index(title="Главная"):
    return render_template('base.html', title=title)

@app.route('/training/<prof>')
def training(prof):
    if 'инженер' in prof:
        title = "Инженерные тренажёры"
        image = "img/rocket.jpg"

    elif 'строитель' in prof:
        title = "Научные симуляторы"
        image = "img/science.jpg"
    elif 'строитель' or 'инженер' not in prof:
        title = "введите другой заголовок пж"
        image = "img/fish.jpg"

    return render_template('training.html', title=title, image=image)



if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
