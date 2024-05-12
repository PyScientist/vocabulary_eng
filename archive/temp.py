from flask import Flask
from flask import render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vocabulary.db'
db = SQLAlchemy(app)





@app.route('/<username>')
def show_user_profile(username):
  return f'User {username}'


@app.route('/hello/<name>')
def hello(name):
  comments = [1, 2, 3]
  return render_template('main.html', name=name, comment=comments)


@app.route('/submit_form_to', methods=['POST'])
def submit():
  name = request.form['word']
  translation = request.form['translation']
  comments = [1,2,3]
  return render_template('main.html', name=name, comment=comments)


if __name__ == '__main__':
  app.run(debug=True, port=8000)

