from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_follower_count_from_twitter(username):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        url = f'https://twitter.com/{username}'
        response = requests.get(url, headers=headers)
        logger.info(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Look for follower count in the HTML
            follower_element = soup.find('span', {'data-testid': 'UserFollowers'})
            if follower_element:
                count_text = follower_element.text
                # Convert text like "1.5M" or "500K" to numbers
                count = parse_follower_count(count_text)
                logger.info(f"Found follower count text: {count_text}")
                return count
            else:
                logger.error("Follower element not found in HTML")
        return 0
    except Exception as e:
        logger.error(f"Error getting follower count: {str(e)}")
        return 0

def parse_follower_count(count_text):
    try:
        # Remove commas and spaces
        count_text = count_text.replace(',', '').replace(' ', '')
        
        # Handle K, M, B suffixes
        if 'K' in count_text:
            return int(float(count_text.replace('K', '')) * 1000)
        elif 'M' in count_text:
            return int(float(count_text.replace('M', '')) * 1000000)
        elif 'B' in count_text:
            return int(float(count_text.replace('B', '')) * 1000000000)
        else:
            return int(count_text)
    except:
        return 0

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