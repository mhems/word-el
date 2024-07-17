from flask import (
    Flask,
    render_template,
    request,
    g
)
from db import (
    init_app        
)

from itertools import takewhile

app = Flask('word-el')
init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

def get_last_word(inputs: {str: str}):
    rows = [(row, ''.join(inputs['r%d-%d' % (row, col)].upper() for col in range(5))) for row in range(5)]
    return list(takewhile(lambda x: len(x[1]) == 5, rows))[-1]

@app.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == 'POST':
        row, word = get_last_word(request.form)
        app.logger.debug(str(row) + " " + word)
        g.keys = dict()
        g.keys['a'] = 'present'
        g.keys['z'] = 'absent'
        g.keys['l'] = 'correct'
    return render_template('game.html')

@app.route('/user/<username>')
def show_user_profile(username):
    pass

if __name__ == '__main__':
    app.run()

