from datetime import date as Date
from datetime import timedelta as td
import requests
from collections import namedtuple as nt
from enum import IntEnum

Puzzle = nt('Puzzle',
            ['id', 
             'solution',
             'print_date',
             'days_since_launch',
             'editor'])

class Score(IntEnum):
    ABSENT = 0
    PRESENT = 1
    CORRECT = 2
    
    def __str__(self) -> str:
        return 'X?!'[self]

def _load(filename: str) -> [str]:
    with open(filename) as fp:
        return set(line.strip() for line in fp.readlines())

URL = 'https://www.nytimes.com/svc/wordle/v2/{}.json'
ACCEPTED = _load('accepted.txt')
ANSWERS = _load('answers.txt')
FIRST = Date(2021, 6, 19)

def get(date: Date = None) -> Puzzle:
    try:
        if date is None:
            date = Date.today()
        stamp = date.strftime('%Y-%m-%d')
        url = URL.format(stamp)
        response = requests.get(url)
        d = response.json()
        args = [d.get(field, '') for field in Puzzle._fields]
        return Puzzle(*args)
    except:
        return Puzzle(0, '', '', 0, '')

def collect(days: int = None):
    one_day = td(days=1)
    end = Date.today() + one_day if days is None else FIRST + td(days=days)
    cur = FIRST

    with open('puzzles.csv', 'w') as fp:
        while cur != end:
            puzzle = get(cur)
            fp.write(','.join(str(e) for e in puzzle) + '\n')
            fp.flush()
            cur += one_day

def acceptable(guess: str) -> bool:
    return guess in ACCEPTED

def score(guess: str, answer: str) -> (Score, Score, Score, Score, Score):
    '''
    >>> score('hello', 'world')
    (<Score.ABSENT: 0>, <Score.ABSENT: 0>, <Score.PRESENT: 1>, <Score.CORRECT: 2>, <Score.PRESENT: 1>)
    '''
    if len(guess) != 5:
        raise ValueError('guess must be 5 letters')
    if len(answer) != 5:
        raise ValueError('answer must be 5 letters')
    if guess not in ACCEPTED:
        raise ValueError('illegal guess')
    if answer not in ANSWERS:
        raise ValueError('illegal answer')
    letters = set(answer)
    def inner(guess_letter: str, answer_letter: str) -> Score:
        if guess_letter == answer_letter:
            return Score.CORRECT
        return Score.PRESENT if guess_letter in letters else Score.ABSENT
    return tuple(inner(g, a) for g, a in zip(guess, answer))

def correct(guess: str, answer: str) -> bool:
    return all(Score.CORRECT == s for s in score(guess, answer))

def play(limit: int = 6) -> int:
    answer = get().solution
    round = 0
    while round < limit:
        guess = input('Guess: ')
        s = score(guess, answer)
        print(' '.join(map(str, s)))
        if all(Score.CORRECT == e for e in s):
            return round + 1
        round += 1
    return -1

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    #play()
