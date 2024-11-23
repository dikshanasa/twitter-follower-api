from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/followers', methods=['POST'])
def get_followers():
    username = request.json.get('username')
    return jsonify({'followers_count': 1000})

if __name__ == '__main__':
    app.run(debug=True)