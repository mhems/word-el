from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)
from db import (
    init_app,
    get,
    acceptable
)
from wordle import (
    score,
    Score,
)

from datetime import date as Date
from datetime import datetime as dt
from itertools import takewhile

empty_guesses = [[''] * 5 for _ in range(6)]
default_key_rows = [{chr(i): 'default' for i in range(ord('a'), ord('z') + 1)}] * 6
default_keys = {chr(i): 'default' for i in range(ord('a'), ord('z') + 1)}
classes = {Score.PRESENT: 'present', Score.ABSENT: 'absent', Score.CORRECT: 'correct'}

app = Flask('word-el')
app.config['SECRET_KEY'] = 'dev'
init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

def get_words(inputs: {str: str}):
    return [''.join(inputs['r%d-%d' % (row, col)].upper() for col in range(5)) for row in range(6)]

@app.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == 'POST':
        date = Date(*map(int, request.form['date'].split('-')))
        answer = get(date)['solution']
        guesses = get_words(request.form)
        filled_in = list(takewhile(lambda x: len(x) == 5, guesses))
        row = len(filled_in) - 1
        guess = filled_in[-1] if filled_in else None
        
        if guess and not acceptable(guess.lower()):
            filled_in.pop()
            guesses[row] = '' * 5
            row = max(0, row - 1)
            flash('Invalid guess')
        
        if guess:
            rows_keys = [dict(d) for d in default_key_rows]
            keys = dict(default_keys)
            results = None
            for i, guess in enumerate(filled_in):
                results = score(guess, answer)
                for letter, result in zip(guess, results):
                    rows_keys[i][letter.lower()] = keys[letter.lower()] = classes[result]
            if results and all(s == Score.CORRECT for s in results):
                row = 7
                flash('Well done!')
            elif row < 5:
                row += 1
            else:
                flash('Answer = ' + answer.upper())
                row = 7

            session['keys'] = keys
            session['row_keys'] = rows_keys
            session['current_row'] = row
            session['guesses'] = [list(guess.lower()) for guess in guesses]
            session['date'] = request.form['date']
        return redirect(url_for('game'))
        
    keys = session.pop('keys', default_keys)
    rows_keys = session.pop('row_keys', default_key_rows)
    current_row = session.pop('current_row', 0)
    guesses = session.pop('guesses', empty_guesses)
    date = session.pop('date', today())
    return render_template('game.html', keys=keys, row_keys=rows_keys, current_row=current_row, guesses=guesses, date=date)

def today():
    return dt.now().isoformat()[:10]

@app.route('/user/<username>')
def show_user_profile(username):
    pass

if __name__ == '__main__':
    app.run()

