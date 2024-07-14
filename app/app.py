from flask import (
    Flask,
    render_template,
)
from . import db

app = Flask('word-el')
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game')
def game():
    return render_template('game.html')

@app.route('/user/<username>')
def show_user_profile(username):
    pass

if __name__ == '__main__':
    app.run()

