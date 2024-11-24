from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import requests
import json

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_follower_count_from_twitter(username):
    try:
        headers = {
            'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs=1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'x-guest-token': get_guest_token()
        }
        
        url = f'https://api.twitter.com/graphql/SAMkL5y_N7rFLrb8WCbOtw/UserByScreenName?variables=%7B%22screen_name%22%3A%22{username}%22%2C%22withSafetyModeUserFields%22%3Atrue%7D'
        
        response = requests.get(url, headers=headers)
        logger.info(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and 'user' in data['data']:
                followers = data['data']['user']['legacy']['followers_count']
                logger.info(f"Found followers: {followers}")
                return followers
        return 0
    except Exception as e:
        logger.error(f"Error getting follower count: {str(e)}")
        return 0

def get_guest_token():
    try:
        response = requests.post(
            'https://api.twitter.com/1.1/guest/activate.json',
            headers={
                'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs=1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'
            }
        )
        return response.json()['guest_token']
    except Exception as e:
        logger.error(f"Error getting guest token: {str(e)}")
        return None

@app.route('/followers', methods=['POST'])
def get_followers():
    try:
        username = request.json.get('username')
        logger.info(f"Received request for username: {username}")

        if not username:
            return jsonify({'error': 'Username required'}), 400

        follower_count = get_follower_count_from_twitter(username)
        logger.info(f"Found follower count for {username}: {follower_count}")
        
        return jsonify({'followers_count': follower_count})

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)