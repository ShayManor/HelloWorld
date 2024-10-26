from flask import Flask

from Backend.main import solver

app = Flask(__name__)


@app.route('/solve', methods=['PUT'])
def solve(problem, solution):
    return solver(problem, solution)


@app.route('/ping', methods=['GET'])
def ping():
    state = 1
    return state


@app.route('/answer', methods=['GET'])
def answer():
    return 'youtube.com'


if __name__ == '__main__':
    app.run(debug=True)
