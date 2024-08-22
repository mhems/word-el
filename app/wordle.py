from collections import namedtuple as nt
from collections import defaultdict
from enum import IntEnum
from db import acceptable
from collections import Counter

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

class WordleRegex:    
    def __init__(self, answer: str):
        self.answer = answer
        self.exclude = set()
        self.include = set()
        self.correct = []
    def add_guess(self, guess: str):
        result = score(guess, self.answer)
        


def build_regex(answer: str, guesses: [str]) -> WordleRegex:
    pass

def foo(answer: str, guesses: [str], wordlist: {str}):
    pass

def score(guess: str, answer: str) -> (Score, Score, Score, Score, Score):
    '''
    >>> score('hello', 'world')
    (<Score.ABSENT: 0>, <Score.ABSENT: 0>, <Score.ABSENT: 0>, <Score.CORRECT: 2>, <Score.PRESENT: 1>)
    >>> score('salad', 'inlay')
    (<Score.ABSENT: 0>, <Score.ABSENT: 0>, <Score.CORRECT: 2>, <Score.CORRECT: 2>, <Score.ABSENT: 0>)
    >>> score('sands', 'sissy')
    (<Score.CORRECT: 2>, <Score.ABSENT: 0>, <Score.ABSENT: 0>, <Score.ABSENT: 0>, <Score.PRESENT: 1>)
    >>> score('sands', 'aspic')
    (<Score.PRESENT: 1>, <Score.PRESENT: 1>, <Score.ABSENT: 0>, <Score.ABSENT: 0>, <Score.ABSENT: 0>)
    '''
    if len(guess) != 5:
        raise ValueError('guess must be 5 letters')
    if len(answer) != 5:
        raise ValueError('answer must be 5 letters')
    #if not acceptable(guess.lower()):
    #    raise ValueError('illegal guess')
    answer = answer.lower()
    guess = guess.lower()
    counter = Counter(answer)
    corrects = set()
    presents = defaultdict(int)
    response = [None] * 5
    count = 0
    for i, (g, a) in enumerate(zip(guess, answer)):
        if g == a:
            response[i] = Score.CORRECT
            corrects.add(g)
        elif g not in counter:
            response[i] = Score.ABSENT
        else:
            continue
        count += 1
    if count < 5:
        for i, (r, g, a) in enumerate(zip(response, guess, answer)):
            if not r:
                if g in counter and counter[g] > presents[g] and (g not in corrects or counter[g] > 1):
                    response[i] = Score.PRESENT
                    presents[g] += 1
                else:
                    response[i] = Score.ABSENT
                
    
    return tuple(response)

def correct(guess: str, answer: str) -> bool:
    return all(Score.CORRECT == s for s in score(guess, answer))

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    #play()
