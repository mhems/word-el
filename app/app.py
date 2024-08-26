from flask import (
    Flask,
    render_template,
)
from db import init_app
from auth import auth_bp
from stats import stats_bp
from game import game_bp

app = Flask('word-el')
app.config['SECRET_KEY'] = 'dev'
init_app(app)
app.register_blueprint(auth_bp)
app.register_blueprint(stats_bp)
app.register_blueprint(game_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
