from app import app
from flask import render_template, request


@app.route('/')
@app.route('/index')
@app.route('/index/<name>')
def hello(name):
    comments = [1, 2, 3]
    return render_template('main.html', name=name, comment=comments)


@app.route('/submit_form_to', methods=['POST'])
def submit():
    name = request.form['word']
    translation = request.form['translation']
    comments = [
        {'comment': 'first comment'},
        {'comment': 'second comment'}
    ]
    return render_template('main.html', name=name, comments=comments, translation=translation)
