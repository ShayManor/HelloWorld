from flask import Flask, jsonify, request

from Backend.main import solver

app = Flask(__name__)


@app.route('/solve', methods=['PUT'])
def solve():
    data = request.get_json()
    problem = data.get('problem')
    solution = data.get('solution')
    upload = False
    result = solver(problem, solution).upload(upload).to_json()
    # return result

# @app.route('/ping', methods=['GET'])
# def ping():
#     if s == None:
#         return "Error: solve has not been started"
#     return s.state


if __name__ == '__main__':
    app.run(debug=True)
