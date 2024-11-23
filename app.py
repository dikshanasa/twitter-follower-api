from flask import Flask, jsonify, request
from flask_cors import CORS  # To handle CORS issues

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/followers', methods=['POST'])
def get_followers():
    username = request.json.get('username')
    # Add your Twitter API logic here
    # Return dummy data for now
    return jsonify({'followers_count': 1000})

if __name__ == '__main__':
    app.run(debug=True)