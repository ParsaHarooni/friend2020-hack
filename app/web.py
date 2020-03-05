from flask import Flask, jsonify, render_template, request
from friend2020.results import FriendResult

app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def main():
    return render_template("main.html")

@app.route('/result')
def show_answers():
    code = request.args.get("code")
    quiz_result = FriendResult(code).get_answers()
    resp = dict(status=True, data=quiz_result)
    if quiz_result is None:
        resp = dict(status=False, message="Quiz with this code was not found")
    return jsonify(resp)

@app.route('/api/results/<int:code>')
def get_results(code):
    quiz_result = FriendResult(code).get_answers()
    resp = dict(status=True, data=quiz_result)
    if quiz_result is None:
        resp = dict(status=False, message="Quiz with this code was not found")
    return jsonify(resp)

app.run(debug=True)
