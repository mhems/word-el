from collections import namedtuple as nt
from enum import IntEnum
from db import acceptable

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

def score(guess: str, answer: str) -> (Score, Score, Score, Score, Score):
    '''
    >>> score('hello', 'world')
    (<Score.ABSENT: 0>, <Score.ABSENT: 0>, <Score.PRESENT: 1>, <Score.CORRECT: 2>, <Score.PRESENT: 1>)
    '''
    if len(guess) != 5:
        raise ValueError('guess must be 5 letters')
    if len(answer) != 5:
        raise ValueError('answer must be 5 letters')
    if not acceptable(guess.lower()):
        raise ValueError('illegal guess')
    letters = set(answer.lower())
    def inner(guess_letter: str, answer_letter: str) -> Score:
        if guess_letter == answer_letter:
            return Score.CORRECT
        return Score.PRESENT if guess_letter in letters else Score.ABSENT
    return tuple(inner(g, a) for g, a in zip(guess.lower(), answer.lower()))

def correct(guess: str, answer: str) -> bool:
    return all(Score.CORRECT == s for s in score(guess, answer))

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    #play()
