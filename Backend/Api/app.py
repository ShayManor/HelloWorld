from flask import Flask, jsonify, request
from flask_cors import CORS

from Backend.main import solver

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/solve', methods=['POST'])
def solve():
    data = request.get_json()
    problem = data.get('problem')
    return solver(problem).upload()
    # return {'url': 'https://manors-videos-bucket.s3.us-east-2.amazonaws.com/5fe9c166-93f0-11ef-803a-c6ac684d68cbvideo.mp4'}, 200


if __name__ == '__main__':
    app.run(debug=True)

#     AWS access portal URL: https://d-9067d96b68.awsapps.com/start, Username: shay, One-time password: b/m-yG7ne&M@sz
