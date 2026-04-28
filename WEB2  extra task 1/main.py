from flask import Flask, render_template, redirect, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'static/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
@app.route('/index/<title>')
def index(title="Главная"):
    return render_template('base.html', title=title)


@app.route('/gallery', methods=['GET', 'POST'])
def gallery():
    if request.method == 'POST':
        file = request.files['file']

        if file and file.filename != "":
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

        return redirect('/gallery')

    images = os.listdir(UPLOAD_FOLDER)

    return render_template('gallery.html', images=images)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
