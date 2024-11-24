from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    return jsonify({'status': 'API is running'})

@app.route('/followers', methods=['POST'])
def get_followers():
    try:
        username = request.json.get('username')
        logger.info(f"Received request for username: {username}")

        if not username:
            return jsonify({'error': 'Username is required'}), 400

        # Use shields.io API instead of Twitter CDN
        shields_url = f'https://img.shields.io/twitter/follow/{username}?label=Followers'
        logger.info(f"Making request to: {shields_url}")
        
        response = requests.get(shields_url)
        logger.info(f"Shields.io Response Status: {response.status_code}")
        
        if response.status_code == 200:
            # Extract follower count from shields.io response
            try:
                # The response contains SVG with follower count
                content = response.text
                # Extract number from response
                import re
                follower_count = re.search(r'>(\d+)<', content)
                if follower_count:
                    count = int(follower_count.group(1))
                    logger.info(f"Found follower count: {count}")
                    return jsonify({'followers_count': count})
            except Exception as e:
                logger.error(f"Error parsing shields.io response: {str(e)}")
                
        return jsonify({'error': 'Failed to fetch follower count'}), response.status_code

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)