import sqlite3
import click
from datetime import date as Date
from datetime import timedelta as td
import requests
from flask import current_app, g
from werkzeug.security import generate_password_hash

DB = 'db/db.sqlite'
SCHEMA = 'db/schema.sql'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB,
                               detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db

@click.command('init-db')
def init_db():
    db = get_db()
    with current_app.open_resource(SCHEMA) as fp:
        db.executescript(fp.read().decode('utf8'))

def close_db(e = None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def add_puzzle(puzzle, commit: bool = False):
    named = '(:id, :solution, :print_date, :days_since_launch, :editor)'
    unnamed = '(?, ?, ?, ?, ?)'
    INSERT_STMT = '''INSERT INTO puzzle
                       (id, solution, print_date, days_since_launch, editor) 
                       VALUES''' + (named if isinstance(puzzle, dict) else unnamed)
    db = get_db()
    db.execute(INSERT_STMT, puzzle)
    if commit:
        db.commit()

def add_word(word: str):
    db = get_db()
    db.execute('INSERT INTO acceptable (word) VALUES (:word)', [word])

def acceptable(word: str):
    db = get_db()
    return db.execute('SELECT * FROM acceptable WHERE word = ?', [word]).fetchone() is not None

@click.command('seed-db')
def seed_db():
    db = get_db()
    with open('db/puzzles.csv', 'r') as fp:
        for line in fp.readlines():
            tokens = line.strip().split(',')
            if len(tokens) < 5:
                tokens.append('')
            add_puzzle(tokens)
    db.commit()

@click.command('seed-accepted')
def seed_accepted():
    with open('db/accepted.txt', 'r') as fp:
        for line in fp.readlines():
            add_word(line.strip())
    db = get_db()
    db.commit()

def add_user(username: str, password: str):
    db = get_db()
    if get_user_by_name(username) is not None:
        return f'User {username} already exists'
    db.execute('INSERT INTO user (username, password) VALUES (?, ?)',
        [username, password])
    db.commit()
    return None

def get_user_by_name(username: str):
    db = get_db()
    return db.execute('SELECT * FROM user WHERE username == ?', [username]).fetchone()

def get_user_by_id(id_: int):
    db = get_db()
    return db.execute('SELECT * FROM user WHERE id == ?', [id_]).fetchone()

def get_puzzle_by_id(id_: int):
    db = get_db()
    return db.execute('SELECT * FROM puzzle WHERE id == ?', [id_]).fetchone()

def date_to_str(date: Date) -> str:
    return date.strftime("%Y-%m-%d")

def get_puzzle_by_date(date: Date):
    db = get_db()
    date_string = date_to_str(date)
    return db.execute('SELECT * FROM puzzle WHERE print_date == ?',[date_string]).fetchone()

def add_solve(user_id: int, date: Date, solved: bool, attempts: [str]):
    db = get_db()
    puzzle_id = get_puzzle_by_date(date)['id']
    num_attempts = len(attempts)
    values = [user_id, puzzle_id, int(solved), num_attempts]
    values.extend(attempts)
    values.extend([''] * (6 - num_attempts))
    db.execute('INSERT into solve' +
               '(user_id, puzzle_id, solved, num_attempts, ' +
                'attempt1, attempt2, attempt3, attempt4, attempt5, attempt6) VALUES' +
               '(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
               values)
    db.commit()

def get_solves():
    db = get_db()
    return db.execute('SELECT ' + 
                        'username, print_date, solution, solved, num_attempts, ' +
                        'attempt1, attempt2, attempt3, attempt4, attempt5, attempt6 ' +
                      'FROM solve INNER JOIN user ON solve.user_id = user.id ' +
                      'INNER JOIN puzzle ON solve.puzzle_id = puzzle.id').fetchall()

def get(date: Date = None) -> dict:
    URL = 'https://www.nytimes.com/svc/wordle/v2/{}.json'
    if date is None:
        date = Date.today()
    stamp = date.strftime('%Y-%m-%d')
    url = URL.format(stamp)
    response = requests.get(url)
    return response.json()

@click.command('sync-db')
def sync_db():
    LAST_PRINT_DATE_QUERY = 'SELECT print_date FROM puzzle ORDER BY print_date DESC'
    today = Date.today()
    db = get_db()
    last_db_date = db.execute(LAST_PRINT_DATE_QUERY).fetchone()['print_date']
    one_day = td(days = 1)
    cur = Date.fromisoformat(last_db_date) + one_day
    while cur <= today:
        puzzle = get(cur)
        print(puzzle)
        add_puzzle(puzzle)
        cur += one_day
    db.commit()

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db)
    app.cli.add_command(seed_db)
    app.cli.add_command(sync_db)
    app.cli.add_command(seed_accepted)