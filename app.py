from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/followers', methods=['POST'])
def get_followers():
    try:
        username = request.json.get('username')
        logger.info(f"Received request for username: {username}")

        if not username:
            return jsonify({'error': 'Username is required'}), 400

        cdn_url = f'https://cdn.syndication.twimg.com/widgets/followbutton/info.json?screen_names={username}'
        logger.info(f"Making request to: {cdn_url}")
        
        response = requests.get(cdn_url)
        logger.info(f"CDN Response Status: {response.status_code}")
        logger.info(f"CDN Response Content: {response.text}")

        if response.status_code == 200:
            data = response.json()
            logger.info(f"Parsed data: {data}")
            
            if data and len(data) > 0:
                follower_count = data[0]['followers_count']
                logger.info(f"Found follower count: {follower_count}")
                return jsonify({'followers_count': follower_count})
            
        logger.error(f"Failed to fetch follower count. Status: {response.status_code}")
        return jsonify({'error': 'Failed to fetch follower count'}), response.status_code

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)