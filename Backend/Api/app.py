from flask import Flask, jsonify, request

from Backend.main import solver

app = Flask(__name__)


@app.route('/solve', methods=['PUT'])
def solve():
    data = request.get_json()
    problem = data.get('problem')
    solution = data.get('solution')
    upload = False
    return solver(problem, solution).upload(upload).to_json()


if __name__ == '__main__':
    app.run(debug=True)

#     AWS access portal URL: https://d-9067d96b68.awsapps.com/start, Username: shay, One-time password: b/m-yG7ne&M@sz
