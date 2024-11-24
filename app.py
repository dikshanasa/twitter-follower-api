from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Twitter API configuration
TWITTER_BEARER_TOKEN = 'YOUR_TWITTER_BEARER_TOKEN'  # From your config.js

@app.route('/followers', methods=['POST'])
def get_followers():
    try:
        username = request.json.get('username')
        if not username:
            return jsonify({'error': 'Username is required'}), 400

        # Twitter API v2 endpoint for user lookup
        url = f'https://api.twitter.com/2/users/by/username/{username}?user.fields=public_metrics'
        headers = {
            'Authorization': f'Bearer {TWITTER_BEARER_TOKEN}'
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            follower_count = data['data']['public_metrics']['followers_count']
            return jsonify({'followers_count': follower_count})
        else:
            return jsonify({'error': 'Failed to fetch follower count'}), response.status_code

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)