from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import tweepy

app = Flask(__name__)
CORS(app)

# Twitter API v2 credentials
CLIENT_ID = 'BK3pCwZ4Yy2fSNzY0opq3AMZw'
CLIENT_SECRET = 'hisdCz0jSKlS0fER6X2x7pedY2WiXq44B64aqxzRcu7VxSIm3f'
ACCESS_TOKEN = '1859789979171385344-JbRXVDEFKgE9D5ONORO01pF7xlJvdi'
ACCESS_SECRET = '2yomWTSiA3d75CGfxb2R3LQIKBLXyzBKF38YqEyTAWOU4'

@app.route('/followers', methods=['POST'])
def get_followers():
    try:
        username = request.json.get('username')
        if not username:
            return jsonify({'error': 'Username is required'}), 400

        # Initialize Tweepy client
        client = tweepy.Client(
            consumer_key=CLIENT_ID,
            consumer_secret=CLIENT_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_SECRET
        )

        # Get user information
        user = client.get_user(username=username, user_fields=['public_metrics'])
        
        if user.data:
            follower_count = user.data.public_metrics['followers_count']
            print(f"Found follower count for {username}: {follower_count}")
            return jsonify({'followers_count': follower_count})
        
        return jsonify({'error': 'User not found'}), 404

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)