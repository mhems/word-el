from flask import Flask

app = Flask('word-el')

@app.route('/')
def main():
    return 'hi!'
