from flask import (
    Flask,
    render_template,
    request
)
from db import (
    init_app        
)

app = Flask('word-el')
init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == 'POST':
        app.logger.info(request.form)
    return render_template('game.html')

@app.route('/user/<username>')
def show_user_profile(username):
    pass

if __name__ == '__main__':
    app.run()

