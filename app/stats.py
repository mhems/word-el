from flask import (
    Blueprint, render_template
)
from datetime import date as Date

from db import get_solves

stats_bp = Blueprint('stats', __name__, url_prefix='/stats')
fields = ['username', 'print_date', 'solution', 'solved', 'num_attempts', 'attempt1', 'attempt2', 'attempt3', 'attempt4', 'attempt5', 'attempt6']
cols = ['User Name', 'Print Date', 'Answer', 'Won', 'Score', 'Attempt 1', 'Attempt 2', 'Attempt 3', 'Attempt 4', 'Attempt 5', 'Attempt 6']

@stats_bp.route('/')
def stats():
    solves = get_solves()
    translated = []
    for solve in solves:
        entry = {}
        for field, col in zip(fields, cols):
            entry[col] = solve[field]
        entry['Won'] = 'Yes' if entry['Won'] else 'No'
        entry['Print Date'] = Date(*map(int, entry['Print Date'].split('-'))).strftime('%m/%d/%Y')
        translated.append(entry)
    return render_template('stats.html', columns=cols, solves=translated)
