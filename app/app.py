from flask import (
    Flask,
    render_template,
    request,
    g,
    redirect,
    url_for,
    session
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

from itertools import takewhile

empty_guesses = [[''] * 5 for _ in range(6)]
default_key_rows = [{chr(i): 'default' for i in range(ord('a'), ord('z') + 1)}] * 6
default_keys = {chr(i): 'default' for i in range(ord('a'), ord('z') + 1)}

app = Flask('word-el')
app.config['SECRET_KEY'] = 'dev'
init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

def get_words(inputs: {str: str}):
    rows = [''.join(inputs['r%d-%d' % (row, col)].upper() for col in range(5)) for row in range(6)]
    app.logger.debug('rows: '+ ', '.join(rows))
    return rows

@app.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == 'POST':
        answer = get()['solution']
        guesses = get_words(request.form)
        filled_in = list(takewhile(lambda x: len(x) == 5, guesses))
        row = len(filled_in) - 1
        guess = filled_in[-1] if filled_in else None
        app.logger.debug(f'row {row}, guess {guess}')
        if not acceptable(guess.lower()):
            return 'illegal guess: ' + guess
        if guess:
            rows_keys = [dict(d) for d in default_key_rows]
            keys = dict(default_keys)
            for i, guess in enumerate(filled_in):
                results = score(guess, answer)
                for letter, result in zip(guess, results):
                    rows_keys[i][letter.lower()] = {Score.PRESENT: 'present', Score.ABSENT: 'absent', Score.CORRECT: 'correct'}[result]
                    keys[letter.lower()] = {Score.PRESENT: 'present', Score.ABSENT: 'absent', Score.CORRECT: 'correct'}[result]
            app.logger.debug('keys: ' + str(keys))
            if all(s == Score.CORRECT for s in results):
                return 'You win!!!'
            if row < 5:
                app.logger.debug('row is now ' + str(row + 1))
                row += 1
            else:
                return 'You lose!!!'
            app.logger.debug(f'putting {keys} in session')
            app.logger.debug(f'putting {row} in session')
            app.logger.debug(f'putting {rows_keys} in session')
            app.logger.debug(f'putting {guesses} in session')
            session['keys'] = keys
            session['row_keys'] = rows_keys
            session['current_row'] = row
            session['guesses'] = [list(guess.lower()) for guess in guesses]
            return redirect(url_for('game'))
    keys = session.pop('keys', default_keys)
    rows_keys = session.pop('row_keys', default_key_rows)
    current_row = session.pop('current_row', 0)
    guesses = session.pop('guesses', empty_guesses)
    app.logger.debug('guesses: ' + '; '.join(','.join(row) for row in guesses))
    app.logger.debug('row:' + str(current_row))
    app.logger.debug('keys: ' + str(keys))
    app.logger.debug('row_keys: ' + '\n'.join(str(d) for d in rows_keys))
    return render_template('game.html', keys=keys, row_keys=rows_keys, current_row=current_row, guesses=guesses)

@app.route('/user/<username>')
def show_user_profile(username):
    pass

if __name__ == '__main__':
    app.run()

