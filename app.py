from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_follower_count_from_twitter(username):
    try:
        curl_command = f"curl https://twitter.com/{username} | grep 'data-count=\"' | awk -F '\"' '{{print $2}}'"
        process = subprocess.Popen(
            curl_command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output, error = process.communicate()
        follower_count = output.decode('utf-8').strip()
        logger.info(f"Raw follower count for {username}: {follower_count}")
        return int(follower_count) if follower_count.isdigit() else 0
    except Exception as e:
        logger.error(f"Error getting follower count: {str(e)}")
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