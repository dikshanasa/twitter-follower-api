from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
# Configure CORS to allow requests from Twitter/X
CORS(app, resources={
    r"/*": {
        "origins": ["https://twitter.com", "https://x.com"],
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

@app.route('/followers', methods=['POST'])
def get_followers():
    try:
        username = request.json.get('username')
        if not username:
            return jsonify({'error': 'Username is required'}), 400
            
        # For now, returning dummy data
        return jsonify({'followers_count': 1000})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)