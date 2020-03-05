from flask import Flask, jsonify
from friend2020.results import FriendResult

app = Flask(__name__)


@app.route('/api/results/<int:code>')
def get_results(code):
    quiz_result = FriendResult(code).get_answers()
    resp = dict(status=True, data=quiz_result)
    if quiz_result is None:
        resp = dict(status=False, message="Quiz with this code was not found")
    return jsonify(resp)


