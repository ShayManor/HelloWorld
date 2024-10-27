from flask import Flask, request
from flask_cors import CORS

from Backend.main import solver

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json()
    problem = data.get('problem')
    return solver(problem).upload()


if __name__ == '__main__':
    app.run(debug=True)
