import random
from flask import Flask, jsonify, request, session, send_from_directory
import os

app = Flask(__name__)
app.secret_key = 'change-this-in-production'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

MAX_ATTEMPTS = 7


@app.route('/new', methods=['POST'])
def new_game():
    session['secret'] = random.randint(1, 100)
    session['attempts'] = 0
    return jsonify({'message': f'You have {MAX_ATTEMPTS} attempts. Good luck!'})


@app.route('/guess', methods=['POST'])
def guess():
    if 'secret' not in session:
        return jsonify({'error': 'No active game. Start a new game first.'}), 400

    data = request.get_json()
    guess_val = data.get('guess')

    if not isinstance(guess_val, int) or not (1 <= guess_val <= 100):
        return jsonify({'error': 'Invalid guess. Must be between 1 and 100.'}), 400

    secret   = session['secret']
    session['attempts'] = session.get('attempts', 0) + 1
    attempts = session['attempts']

    if guess_val == secret:
        session.pop('secret', None)
        return jsonify({
            'status': 'win',
            'result_label': '✅ Correct!',
            'message': f'🎉 Correct! The number was {secret}. You got it in {attempts} attempt{"s" if attempts > 1 else ""}!',
            'attempts': attempts,
        })

    if attempts >= MAX_ATTEMPTS:
        session.pop('secret', None)
        return jsonify({
            'status': 'lose',
            'result_label': '💀 Out of attempts',
            'message': f'💀 Game over! The number was {secret}. Better luck next time!',
            'attempts': attempts,
        })

    if guess_val < secret:
        return jsonify({
            'status': 'too-low',
            'result_label': '📉 Too low',
            'message': '📉 Too low! Try higher.',
            'attempts': attempts,
        })
    else:
        return jsonify({
            'status': 'too-high',
            'result_label': '📈 Too high',
            'message': '📈 Too high! Try lower.',
            'attempts': attempts,
        })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
